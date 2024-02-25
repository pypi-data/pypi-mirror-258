from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from uuid import UUID
from credici.exception import (
    AmountNegativeError,
    InsufficientFundsError,
    UserDoesNotExistError,
)
from credici.async_.async_storage.async_storage import AsyncStorage
from credici.sync_.credit_transaction import CreditTransaction
from pydantic import ConfigDict


class AsyncLedger(BaseModel):
    """The ledger class for managing credit transactions asynchronously."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    transactions: List[CreditTransaction] = []
    storage: AsyncStorage

    async def add(self, user_id: UUID, amount: int, expire_days: int) -> None:
        """Add credits for a user.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The amount of credits to add to the user's balance.
            expire_at (datetime): The expiration date of the credits.

        """
        if amount < 0:
            raise AmountNegativeError(amount)

        if await self.storage.get_user_by_id(user_id) is None:
            raise UserDoesNotExistError(user_id)

        expire_at = datetime.now().replace(hour=23, minute=59) + timedelta(
            days=expire_days
        )

        await self.storage.add_transaction(user_id, amount, expire_at)

    async def subtract(self, user_id: UUID, amount: int) -> None:
        """Subtract credits from a user.

        Args:
            user_id (UUID): The unique identifier of the user.
            amount (int): The amount of credits to subtract from the user's balance.
        """
        if amount < 0:
            raise AmountNegativeError(amount)

        if await self.storage.get_user_by_id(user_id) is None:
            raise UserDoesNotExistError(user_id)

        active_ledger = await self.storage.get_active_ledger(user_id)
        active_balance = sum([entry.amount for entry in active_ledger])
        if active_balance < amount:
            raise InsufficientFundsError(user_id, active_balance, amount)

        transaction_by_expiration = {}
        for entry in active_ledger:
            if entry.expire_at not in transaction_by_expiration:
                transaction_by_expiration[entry.expire_at] = []
            transaction_by_expiration[entry.expire_at].append(entry.amount)

        for expire_at, t_amounts in transaction_by_expiration.items():
            if sum(t_amounts) >= amount:
                await self.storage.add_transaction(user_id, -amount, expire_at)
                break
            elif sum(t_amounts) < amount and sum(t_amounts) > 0:
                amount -= sum(t_amounts)
                await self.storage.add_transaction(user_id, -sum(t_amounts), expire_at)
        return

    async def get_user_transactions_for_period(
        self, user_id: UUID, from_: datetime, to_: datetime
    ) -> List[CreditTransaction]:
        """Get all transactions for a user within a given period.

        Args:
            user_id (UUID): The unique identifier of the user.
            from_ (datetime): The start of the period.
            to_ (datetime): The end of the period.

        Returns:
            List[CreditTransaction]: A list of all transactions for the user within the given period.
        """
        if await self.storage.get_user_by_id(user_id) is None:
            raise UserDoesNotExistError(user_id)

        transactions = await self.storage.get_user_transactions_for_period(
            user_id, from_, to_
        )
        self.transactions = [
            CreditTransaction(
                transaction_id=transaction.transaction_id,
                user_id=transaction.user_id,
                amount=transaction.amount,
                created_at=transaction.created_at,
                expire_at=transaction.expire_at,
            )
            for transaction in transactions
        ]
        return self.transactions

    async def get_all_user_transactions(self, user_id: UUID) -> List[CreditTransaction]:
        """Get all transactions for a user.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            List[CreditTransaction]: A list of all transactions for the user.
        """
        if await self.storage.get_user_by_id(user_id) is None:
            raise UserDoesNotExistError(user_id)

        transactions = await self.storage.get_all_user_transactions(user_id)
        self.transactions = [
            CreditTransaction(
                transaction_id=transaction.transaction_id,
                user_id=transaction.user_id,
                amount=transaction.amount,
                created_at=transaction.created_at,
                expire_at=transaction.expire_at,
            )
            for transaction in transactions
        ]
        return self.transactions

    async def get_active_balance(self, user_id: UUID) -> int:
        """Get the active balance for a user.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            int: The active balance for the user.
        """
        if await self.storage.get_user_by_id(user_id) is None:
            raise UserDoesNotExistError(user_id)
        try:
            active_ledger = await self.storage.get_active_ledger(user_id)
            active_balance = 0
            for transaction in active_ledger:
                active_balance += transaction.amount
            return active_balance
        except Exception:
            raise
