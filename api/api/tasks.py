from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# from .crud import insert_task_data
from .worker import app
from .backend.event_producer import EventProducer
from celery.utils.log import get_task_logger
import json


celery_log = get_task_logger(__name__)

db_engine = ync_engine = create_engine(
    url=f"postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)
Session = sessionmaker(bind=db_engine)


@app.task(name='api.process_workflow')
def process_workflow(next_step, data, file_name, pipeline_id):
    queue_name = next_step
    event_producer = EventProducer()
    response = event_producer.call(queue_name, data)
    response_json = json.loads(response)
    response_json = json.loads(response_json)
    print(type(response_json))
    print(f'{response_json=}')
    if response_json['steps'] and response_json['steps'][0] == 'save_in_database':
        task_in = {
            'file_name': file_name,
            'top_left_x': response_json['payload'][0] if 0 <= 0 < len(
                response_json['payload']) else None,
            'top_left_y': response_json['payload'][1] if 0 <= 1 < len(
                response_json['payload']) else None,
            'width': response_json['payload'][2] if 0 <= 2 < len(
                response_json['payload']) else None,
            'height': response_json['payload'][3] if 0 <= 3 < len(
                response_json['payload']) else None,
            'conf': response_json['payload'][4] if 0 <= 4 < len(
                response_json['payload']) else None,
            'label': response_json['payload'][5] if 0 <= 5 < len(
                response_json['payload']) else None,
            'pipeline_id': pipeline_id
        }
        session = Session()
        insert_query = text("""
            INSERT INTO resulttasks (file_name, top_left_x, top_left_y, width, height, conf, label, pipeline_id)
            VALUES (:file_name, :top_left_x, :top_left_y, :width, :height, :conf, :label, :pipeline_id)
            RETURNING resulttasks.id
        """)
        session.execute(insert_query, task_in)
        session.commit()
        session.close()

    celery_log.info(next_step + " task completed")
    return response_json
