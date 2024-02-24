import logging
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from ....types import convert_str_args
from ....celery import CeleryMonitor, get_task_by_name, is_broker_connected

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument('name_and_args', nargs='+', help="Name (and optional args) of the task to execute.")
        parser.add_argument('-d', '--delay', type=float, help="Delay in seconds.")
        parser.add_argument('-s', '--sync', action='store_true', help="Run the task synchronously.")
    
    def handle(self, name_and_args: list[str], delay: float = None, sync: bool = False, **options):
        name = name_and_args[0]
        args = name_and_args[1:]

        task = get_task_by_name(name)
        args, kwargs = convert_str_args(task.run, *args)

        msg = f"run task {task.name}"
        if sync:
            msg += f" synchronously"
        elif delay is not None:
            msg += f" with {delay} second delay"
        if args:
            msg += f", args={args}"
        if kwargs:
            msg += f", kwargs={kwargs}"
        logger.info(msg)

        if sync:
            task(*args, **kwargs)
        else:
            if not is_broker_connected():
                return
            result = task.apply_async(args, kwargs, countdown=delay)
            logger.info(f"task id: {result.id}")            
            CeleryMonitor.get_instance().task_launched(result.id, task.name, args, kwargs)
            result.forget()
