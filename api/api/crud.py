from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# from .models import Pipeline, Step
from .models import db_helper, ResultTask, Pipeline, Step


async def get_steps_with_pipeline(session: AsyncSession, pipeline_id: int):
    stmt = (
        select(Step)
        .options(
            selectinload(Step.pipelines),
        )
        .join(Step.pipelines)  # Присоединение связи M2M
        .where(Pipeline.id == pipeline_id)  # Фильтрация по pipeline_id
        .order_by(Step.id)
    )
    steps = await session.execute(stmt)
    return [step.queue_name for step in steps.scalars().all()]


def insert_task_data(task_in):
    with db_helper.sync_session_factory() as session:
        result_tusk = ResultTask(**task_in)
        session.add(result_tusk)
        session.commit()
