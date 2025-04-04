from collections.abc import Iterable

from alchemynger import AsyncManager
from sqlalchemy import insert, select, update

from .models import Answer, Chapter, User


class DatabaseService:
    __slots__ = ("_manager",)

    def __init__(self, manager: AsyncManager) -> None:
        self._manager: AsyncManager = manager

    async def is_user_created(self, user_id: int) -> bool:
        stmt = self._manager[User].select.where(User.telegram_id == user_id)
        result: User | None = await self._manager.execute(stmt)
        return bool(result)

    async def create_user(self, user_id: int, name: str, contact: str) -> None:
        stmt = self._manager[User].insert.values(telegram_id=user_id, name=name, contact=contact)
        await self._manager.execute(stmt, commit=True)

    async def create_answer(self, user_id: int, text_answer: str, video_answer_id: str) -> None:
        stmt = self._manager[Answer].insert.values(
            user_id=user_id,
            text_answer=text_answer,
            video_answer_id=video_answer_id,
        )
        await self._manager.execute(stmt, commit=True)

    async def get_unapproved_answers(self) -> list[Answer]:
        stmt = self._manager[Answer].select.where(Answer.is_approved.is_(False))
        return await self._manager.execute(stmt)  # type: ignore[no-any-return]

    async def get_user(self, telegram_id: int) -> User | None:
        stmt = self._manager[User].select.where(User.telegram_id == telegram_id)
        result: list[User] = await self._manager.execute(stmt)
        if not result:
            return None
        return result[0]

    async def get_answer(self, answer_id: int) -> Answer | None:
        stmt = self._manager[Answer].select.where(Answer.id == answer_id)
        result: list[Answer] = await self._manager.execute(stmt)
        if not result:
            return None
        return result[0]

    async def approve_answer(self, answer_id: int) -> None:
        stmt = self._manager[Answer].update.where(Answer.id == answer_id).values(is_approved=True)
        await self._manager.execute(stmt, commit=True)

    async def reject_answer(self, answer_id: int) -> None:
        stmt = self._manager[Answer].delete.where(Answer.id == answer_id)
        await self._manager.execute(stmt, commit=True)

    # async def get_user_tasks_statuses(self, telegram_id: int) -> list[tuple[Task, bool | None]]:
    #     subquery = (
    #         select(UserToTask.task_id, UserToTask.status)
    #         .where(UserToTask.user_id == telegram_id)
    #         .subquery()
    #     )
    #     stmt = (
    #         select(Task, subquery.c.status)
    #         .join(
    #             subquery,
    #             Task.id == subquery.c.task_id,
    #             isouter=True,
    #         )
    #         .order_by(Task.id)
    #     )
    #     async with self._manager.get_session() as session:
    #         results = await session.execute(statement=stmt)
    #     return results.all()  # type: ignore[no-any-return]

    async def migrate_chapters(self, chapters_names: Iterable[str]) -> None:
        async with self._manager.get_session() as session:
            db_chapters: int | None = (await session.execute(select(Chapter.id))).scalars().first()
            if db_chapters is not None:
                await session.execute(
                    update(Chapter),
                    [{"id": id_, "name": name} for id_, name in enumerate(chapters_names, start=1)],
                )
            else:
                await session.execute(
                    insert(Chapter),
                    [{"id": id_, "name": name} for id_, name in enumerate(chapters_names, start=1)],
                )
            await session.commit()
