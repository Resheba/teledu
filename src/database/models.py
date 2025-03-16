from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(AsyncAttrs, DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    telegram_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.telegram_id}, name={self.name!r}, email={self.email!r})"


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.telegram_id, ondelete="CASCADE"), nullable=False)
    text_answer = Column(String, nullable=False)
    video_answer_id = Column(String, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)

    user: Mapped[User] = relationship(
        lazy="selectin",
        foreign_keys=[user_id],
    )

    def __repr__(self) -> str:
        return (
            f"Answer(id={self.id}, text_answer={self.text_answer!r},"
            f" video_answer_id={self.video_answer_id!r})"
        )


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    video_id = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, text={self.text!r}, video_id={self.video_id!r})"


class UserToTask(Base):
    __tablename__ = "user_to_task"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey(User.telegram_id, ondelete="CASCADE"))
    task_id = Column(Integer, ForeignKey(Task.id, ondelete="CASCADE"))
    status = Column(Boolean, default=None, nullable=True)

    # user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])
    task: Mapped[Task] = relationship(lazy="selectin", foreign_keys=[task_id])
