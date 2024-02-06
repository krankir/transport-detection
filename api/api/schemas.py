from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    file_name: str
    top_left_x: Optional[int] = None
    top_left_y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    conf: Optional[int] = None
    label: Optional[int] = None
    pipeline_id: int


class WorkflowTask(BaseModel):
    task_id: str
    task_status: str


class WorkflowTaskResult(BaseModel):
    task_id: str
    task_status: str
    outcome: str
