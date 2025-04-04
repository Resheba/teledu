from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    contact: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.telegram_id}, name={self.name!r}, contact={self.contact!r})"


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id, ondelete="CASCADE"),
        nullable=False,
    )
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey(Chapter.id, ondelete="CASCADE"),
    )
    is_approved: Mapped[bool | None] = mapped_column(Boolean, default=None, nullable=True)

    videos: Mapped[list["AnswerVideo"]] = relationship()

    def __repr__(self) -> str:
        return f"Answer(id={self.id}, is_approved={self.is_approved})"  # 1391069512


class AnswerVideo(Base):
    __tablename__ = "answer_video"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(
        ForeignKey(Answer.id, ondelete="CASCADE"),
        nullable=False,
    )
    video_id: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"AnswerVideo(id={self.id}, answer_id={self.answer_id}, video_id={self.video_id!r})"
