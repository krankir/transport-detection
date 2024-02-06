from fastapi import APIRouter, File, Form, Path, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from .models import db_helper
from .schemas import WorkflowTask, WorkflowTaskResult
from .tasks import process_workflow
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
import json
import base64
from . import crud

router_tasks = APIRouter()


@router_tasks.get('/')
def touch():
    return 'API is running'


@router_tasks.post('/process_image', response_model=WorkflowTask)
async def start_workflow_task(
        # file_bytes_: bytes = File(),
        file_bytes_: UploadFile,
        pipeline_id: int = Form(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    # Запрос в базу и получил шаги
    name_queue_steps = await crud.get_steps_with_pipeline(session, pipeline_id)
    next_step = name_queue_steps.pop(0)
    file_name = file_bytes_.filename

    file_bytes = base64.b64encode(file_bytes_.file.read()).decode('utf-8')
    payload = {
        'steps': name_queue_steps,
        'payload': file_bytes
    }

    payload_json = json.dumps(payload)

    task_id = process_workflow.delay(next_step,
                                     payload_json,
                                     file_name,
                                     pipeline_id,
                                     )

    return {'task_id': str(task_id),
            'task_status': 'Processing'}


@router_tasks.get('/result/{task_id}', response_model=WorkflowTaskResult, status_code=202,
                  responses={202: {'model': WorkflowTask, 'description': 'Accepted: Not Ready'}})
async def workflow_task_result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202,
                            content={'task_id': str(task_id),
                                     'task_status': 'Processing'})
    result = task.get()
    return {'task_id': task_id,
            'task_status': 'SUCCESS',
            'outcome': str(result)}
