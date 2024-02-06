from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .pipeline import Pipeline


class Step(Base):
    name: Mapped[str]
    queue_name: Mapped[str]
    pipelines: Mapped[list['Pipeline']] = relationship(
        secondary="pipeline_step_association",
        back_populates="steps"
    )
