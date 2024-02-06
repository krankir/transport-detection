from celery import Celery

app = Celery(
    'skipper_celery_api',
    broker='pyamqp://skipper:welcome1@rabbitmq//',
    backend='rpc://',
    include=['api.tasks']
)
