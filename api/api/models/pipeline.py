from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .step import Step
    from .result_task import ResultTask


class Pipeline(Base):
    name: Mapped[str]
    description: Mapped[str] = mapped_column(String(100), nullable=True,
                                             default='', server_default='', )
    steps: Mapped[list["Step"]] = relationship(
        secondary="pipeline_step_association",
        back_populates="pipelines"
    )
    # result_tusks: Mapped[list["ResultTask"]] = relationship(back_populates="pipeline")
    result_tasks = relationship("ResultTask", back_populates="pipeline")

