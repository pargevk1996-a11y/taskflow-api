from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, comment_id: int) -> Comment | None:
        return self.db.get(Comment, comment_id)

    def list_by_task(self, task_id: int) -> list[Comment]:
        return list(self.db.execute(select(Comment).where(Comment.task_id == task_id)).scalars().all())

    def create(self, *, task_id: int, author_id: int | None, body: str) -> Comment:
        comment = Comment(task_id=task_id, author_id=author_id, body=body)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment
