from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PipelineStepAssociation(Base):
    __tablename__ = "pipeline_step_association"
    __table_args__ = (
        UniqueConstraint(
            "pipeline_id",
            "step_id",
            name="idx_unique_pipeline_step",
        ),
    )
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("steps.id"))
