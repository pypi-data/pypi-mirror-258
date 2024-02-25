"""
The internal datastructure to save all the slurmified functions.
Not relevant for endusers.
"""

import inspect
import json
import os
import pathlib
import subprocess
import sys
import typing


class FunctionMap:
    """
    The function map assigns functions an id and stores them to be called later.
    This id is reproducible such that the slurm node can retrieve the function
    it is supposed to call just by the id.
    """

    # Needed to save the entry point at the slurm node.
    # The slurm node just executes the file content of a script, so the file name is lost.
    # slurminade will set this value in the beginning to reconstruct it.
    entry_point: typing.Optional[str] = None
    _data = {}
    _ids = set()

    @staticmethod
    def get_id(func: typing.Callable) -> str:
        """
        Returns the unique id of a function. Necessary to slurmify it.
        Probably not needed by the enduser.
        It uses the function name and its file, which should be sufficient unless you
        do not overwrite a function (which is bad anyway).
        :param func: The function you want the id of.
        :return: The id as string.
        """
        file = inspect.getfile(func)
        if file == "<string>":  # on the slurm node, the functions in the entry point
            # are named `<string>`.
            if not FunctionMap.entry_point:
                msg = "No entry point known."
                raise RuntimeError(msg)
            file = FunctionMap.entry_point
        path = os.path.normpath(os.path.abspath(file))
        return f"{path}:{func.__name__}"

    @staticmethod
    def get_readable_name(func_id: str) -> str:
        return func_id.split(":")[-1]

    @staticmethod
    def check_compatibility(func: typing.Callable):
        """
        Throw if the function cannot be assigned an id.
        :param func: The function to be checked.
        :return: None
        """
        if (
            not func.__name__
            or func.__name__ == "<lambda>"
            or not inspect.getfile(func)
        ):
            msg = "Can only slurmify proper functions."
            raise ValueError(msg)

    @staticmethod
    def register(func: typing.Callable) -> str:
        """
        Register a function, allowing it to be called just by its id.
        :param func: The function to be stored. Needs to be a proper function.
        :return: The function's id.
        """
        FunctionMap.check_compatibility(func)
        func_id = FunctionMap.get_id(func)
        if func_id in FunctionMap._data:
            msg = "Multiple function definitions!"
            raise RuntimeError(msg)
        FunctionMap._data[func_id] = func
        return func_id

    @staticmethod
    def call(
        func_id: str, args: typing.Iterable, kwargs: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        """
        Calls a function by its id.
        :param func_id: The id of the function to be called.
        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :return: The return value of the function.
        """
        if func_id not in FunctionMap._data:
            msg = f"Function '{func_id}' unknown!"
            raise KeyError(msg)
        return FunctionMap._data[func_id](*args, **kwargs)

    @staticmethod
    def check_id(func_id: str) -> bool:
        if func_id in FunctionMap._ids:
            return True
        cmd = [
            sys.executable,
            "-m",
            "slurminade.execute",
            "--root",
            get_entry_point(),
            "--listfuncs",
        ]
        out = subprocess.check_output(cmd).decode()
        ids = json.loads(out)
        FunctionMap._ids = set(ids)
        return func_id in FunctionMap._ids

    @staticmethod
    def get_all_ids() -> typing.List[str]:
        return list(FunctionMap._data.keys())


def set_entry_point(entry_point: typing.Union[str, pathlib.Path]) -> None:
    """
    This function usually is not necessary for endusers.
    Set a manual entry point. This can allow you to use slurmify from the interactive
    interpreter.
    :param entry_point: A path to the entry point file.
    :return: None
    """
    if not os.path.isfile(entry_point) or not str(entry_point).endswith(".py"):
        msg = f"Illegal entry point ({entry_point})."
        raise ValueError(msg)
    entry_point = os.path.abspath(entry_point)
    FunctionMap.entry_point = str(entry_point)
    # SlurmFunction.dispatcher.entry_point = entry_point


def get_entry_point() -> str:
    if FunctionMap.entry_point is None:
        import __main__

        entry_point = __main__.__file__

        set_entry_point(entry_point)
    assert FunctionMap.entry_point is not None
    return FunctionMap.entry_point
