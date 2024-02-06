from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .pipeline import Pipeline


class ResultTask(Base):
    file_name: Mapped[str]
    top_left_x: Mapped[Optional[int]]
    top_left_y: Mapped[Optional[int]]
    width: Mapped[Optional[int]]
    height: Mapped[Optional[int]]
    conf: Mapped[Optional[int]]
    label: Mapped[Optional[int]]
    pipeline_id: Mapped[int] = mapped_column(
        ForeignKey("pipelines.id"),
    )
    pipeline: Mapped["Pipeline"] = relationship(back_populates="result_tasks")

