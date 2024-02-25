import inspect
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

from .base_async import BaseAsyncWorker


class ClassicAsyncWorker(BaseAsyncWorker):
    """
    Сlassic async worker, where the task is a tuple: (task_id, task_data).
    task_data is a dictionary with keys "function", "args" and "kwargs".
    Arguments "args" and "kwargs" are optional.

    Class fields:
    - task_courier - an instance of the task_courier.
      Specified when the class is initialized.
    - queue_name - The name of the queue from which tasks are read.
    - after_iteration_sleep_time - Downtime in seconds after each task is
      completed (e.g. 0.1). Default is 1 millisecond.
    - return_task_result - True if needs to return the result of the
      task execution, or False otherwise.
    """

    max_tasks_per_iteration = 1

    def __init__(self, *args, **kwargs):
        self.thread_executor = ThreadPoolExecutor(
            max_workers=self.max_simultaneous_tasks)
        return super().__init__(*args, **kwargs)

    async def perform_single_task(self, task):
        task_id, task_data = task
        assert isinstance(task_data, dict), \
            "task_data must be a dict instance."
        assert "function" in task_data.keys(), \
            "task_data must have a \"function\" key."
        function = task_data["function"]
        function_args = task_data.get("args", tuple())
        function_kwargs = task_data.get("kwargs", dict())

        if inspect.iscoroutinefunction(function):
            return await function(*function_args, **function_kwargs)
        else:
            function_with_data = functools.partial(
                function, *function_args, **function_kwargs)
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.thread_executor, function_with_data)
