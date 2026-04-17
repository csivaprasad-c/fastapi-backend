from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class BaseService(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def _create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity: T) -> T:
        return await self._create(entity)

    async def _delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.commit()
