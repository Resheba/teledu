from collections.abc import Iterable

from alchemynger import AsyncManager
from sqlalchemy import case, func, insert, select, text, update

from .models import Answer, AnswerVideo, Chapter, ChapterAnswerDTO, User, UserAnswersDTO


class DatabaseService:
    __slots__ = ("_manager",)
    # __last_answer_subquery = (
    #     select(func.coalesce(Answer.is_approved, "ON_ACC"))
    #     .where(
    #         Answer.chapter_id == Chapter.id,
    #         Answer.user_id == bindparam("user_id"),
    #     )
    #     .order_by(Answer.id.desc())
    #     .limit(1)
    #     .scalar_subquery()
    # )

    # __user_answers_subquery = select(
    #     Chapter.id.label("chapter_id"),
    #     Chapter.name.label("chapter_name"),
    #     __last_answer_subquery.label("is_approved"),
    # )
    __user_answers_subquery = text("""SELECT
        c.id AS chapter_id,
        c.name AS chapter_name,
        (
            SELECT COALESCE(a.is_approved, "ON_ACC")
            FROM answer a
            WHERE a.chapter_id = c.id
            AND a.user_id = :user_id
            ORDER BY a.id DESC
            LIMIT 1
        ) AS is_approved
        FROM chapter c;
        """)

    def __init__(self, manager: AsyncManager) -> None:
        self._manager: AsyncManager = manager

    async def is_user_created(self, user_id: int) -> bool:
        stmt = self._manager[User].select.where(User.telegram_id == user_id)
        result: User | None = await self._manager.execute(stmt)
        return bool(result)

    async def create_user(self, user_id: int, name: str, contact: str) -> None:
        stmt = self._manager[User].insert.values(telegram_id=user_id, name=name, contact=contact)
        await self._manager.execute(stmt, commit=True)

    async def get_user(self, telegram_id: int) -> User | None:
        stmt = self._manager[User].select.where(User.telegram_id == telegram_id)
        result: list[User] = await self._manager.execute(stmt)
        if not result:
            return None
        return result[0]

    async def create_answer(self, user_id: int, chapter_id: int, videos: list[str]) -> Answer:
        answer: Answer = Answer(user_id=user_id, chapter_id=chapter_id)
        answer.videos = [AnswerVideo(video_id=video_id) for video_id in videos]
        async with self._manager.get_session() as session:
            existed_answer_id: int | None = (
                await session.execute(
                    select(Answer.id).where(
                        Answer.user_id == user_id,
                        Answer.chapter_id == chapter_id,
                    ),
                )
            ).scalar_one_or_none()
            if existed_answer_id is not None:
                await session.execute(
                    self._manager[Answer].delete.where(Answer.id == existed_answer_id),
                )
            session.add(answer)
            await session.commit()
            await session.refresh(answer)
        return answer

    async def get_user_chapter_answers(self, user_id: int) -> list[ChapterAnswerDTO]:
        async with self._manager.get_session() as session:
            result = await session.execute(self.__user_answers_subquery, {"user_id": user_id})
            return UserAnswersDTO.validate_python(map(tuple, result.all()))

    async def is_user_completed_all_chapters(self, user_id: int) -> bool:
        cond = case(
            (func.count(Answer.id) >= 11, True),  # noqa: PLR2004
            else_=False,
        )

        stmt = self._manager[cond].select.where(
            Answer.user_id == user_id,
            Answer.is_approved == True,  # noqa: E712
        )
        async with self._manager.get_session() as session:
            result = await session.execute(stmt)
            res: bool = result.scalars().first()
            return res

    async def approve_answer(self, answer_id: int) -> None:
        stmt = self._manager[Answer].update.where(Answer.id == answer_id).values(is_approved=True)
        await self._manager.execute(stmt, commit=True)

    # async def get_answer(self, answer_id: int) -> Answer | None:
    #     stmt = self._manager[Answer].select.where(Answer.id == answer_id)
    #     result: list[Answer] = await self._manager.execute(stmt)
    #     if not result:
    #         return None
    #     return result[0]

    # async def approve_answer(self, answer_id: int) -> None:
    #     stmt = self._manager[Answer].update.where(Answer.id == answer_id).values(is_approved=True)
    #     await self._manager.execute(stmt, commit=True)

    # async def reject_answer(self, answer_id: int) -> None:
    #     stmt = self._manager[Answer].delete.where(Answer.id == answer_id)
    #     await self._manager.execute(stmt, commit=True)

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
