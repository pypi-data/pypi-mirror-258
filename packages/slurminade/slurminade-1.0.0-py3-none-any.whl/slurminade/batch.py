"""
Contains code for bundling function calls together.
"""
import logging
import typing
from collections import defaultdict

from .dispatcher import (
    Dispatcher,
    FunctionCall,
    get_dispatcher,
    set_dispatcher,
)
from .function import SlurmFunction
from .guard import BatchGuard
from .options import SlurmOptions


class TaskBuffer:
    """
    A simple container to buffer all the tasks by their options.
    We can only bundle tasks with the same slurm options.
    """

    def __init__(self):
        self._tasks = defaultdict(list)

    def add(self, task: FunctionCall, options: SlurmOptions) -> int:
        self._tasks[options].append(task)
        return len(self._tasks[options])

    def items(self):
        for opt, tasks in self._tasks.items():
            if tasks:
                yield opt, tasks

    def get(self, options: SlurmOptions) -> typing.List[FunctionCall]:
        return self._tasks[options]

    def clear(self):
        self._tasks.clear()


class Batch(Dispatcher):
    """
    The logic to buffer the function calls. It wraps the original dispatcher.

    You can use::

        with slurminade.Batch(max_size=20) as batch:  # automatically bundles up to 20 tasks
            # run 100x f
            for i in range(100):
                f.distribute(i)

    to automatically bundle up to 20 tasks and distribute them.
    """

    def __init__(self, max_size: int):
        """
        :param max_size: Bundle up to this many calls.
        """
        super().__init__()
        self.max_size = max_size
        self.subdispatcher = get_dispatcher()
        self._tasks = TaskBuffer()
        self._batch_guard = BatchGuard()

    def flush(self, options: typing.Optional[SlurmOptions] = None) -> typing.List[int]:
        """
        Distribute all buffered tasks. Return the job ids used.
        This method is called automatically when the context is exited.
        However, you may want to call it manually to get the job ids,
        for example to use them for dependency management with ``wait_for``.
        :param options: Only flush tasks with specific options.
        :return: A list of job ids.
        """
        job_ids = []
        if options is None:
            for opt, tasks in self._tasks.items():
                while tasks:
                    job_id = self.subdispatcher(tasks[: self.max_size], opt)
                    job_ids.append(job_id)
                    tasks = tasks[self.max_size :]

        else:
            tasks = self._tasks.get(options)
            self._batch_guard.report_flush(len(tasks))
            while len(tasks) > self.max_size:
                job_id = self.subdispatcher(tasks[: self.max_size], options)
                job_ids.append(job_id)
                tasks = tasks[: self.max_size]
        self._tasks.clear()
        return job_ids

    def add(self, func: SlurmFunction, *args, **kwargs):
        """
        You can also add a task using `add` instead of `distribute`.
        :param func: The function to call
        :param args: The positional arguments
        :param kwargs: The keywords arguments.
        :return: None
        """
        self._dispatch(
            [FunctionCall(func.func_id, args, kwargs)], func.special_slurm_opts
        )

    def _dispatch(
        self, funcs: typing.Iterable[FunctionCall], options: SlurmOptions
    ) -> int:
        for func in funcs:
            self._tasks.add(func, options)
        return -1

    def srun(
        self,
        command: str,
        conf: typing.Optional[typing.Dict] = None,
        simple_slurm_kwargs: typing.Optional[typing.Dict] = None,
    ):
        return self.subdispatcher.srun(command, conf, simple_slurm_kwargs)

    def sbatch(
        self,
        command: str,
        conf: typing.Optional[typing.Dict] = None,
        simple_slurm_kwargs: typing.Optional[typing.Dict] = None,
    ):
        return self.subdispatcher.sbatch(command, conf, simple_slurm_kwargs)

    def __enter__(self):
        self.subdispatcher = get_dispatcher()
        set_dispatcher(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logging.getLogger("slurminade").error("Aborted due to exception.")
            return
        self.flush()
        set_dispatcher(self.subdispatcher)

    def _log_dispatch(self, funcs: typing.List[FunctionCall], options: SlurmOptions):
        if len(funcs) == 1:
            logging.getLogger("slurminade").info(
                f"Adding task to batch with options {options}: {funcs[0]}"
            )
        else:
            logging.getLogger("slurminade").info(
                f"Adding {len(funcs)} tasks to batch with options {options}: {', '.join([str(f) for f in funcs])}"
            )

    def __del__(self):
        self.flush()

    def is_sequential(self):
        return self.subdispatcher.is_sequential()
