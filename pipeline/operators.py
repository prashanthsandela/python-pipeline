import os
from abc import ABCMeta, abstractmethod
from typing import Any, List, Union
from queue import Queue


class Operator(metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self.input = Queue()
        self.output = Queue()

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def emit(self, data: Union[Any, List[Any]]):
        """Store emitted tuples.

        Args:
            tuple ([Any]): Tuple to store.
        """
        if not isinstance(data, List):
            data = [data]

        [self.output.put_nowait(d) for d in data]


class InputOutputOperator(Operator, metaclass=ABCMeta):
    def emitTuple(self) -> None:
        while True:
            data = self.process(self.input.get())
            self.emit(data)


class InputOperator(Operator, metaclass=ABCMeta):
    @abstractmethod
    def emitTuple(self) -> None:
        pass


class OutputOperator(Operator, metaclass=ABCMeta):
    def emitTuple(self) -> None:
        while True:
            self.process(self.input.get())


class FileInputOperator(InputOperator):
    """Read all files from a directory."""

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def emitTuple(self) -> None:
        # Get files in dir.
        files = [f"{self.path}/{f}" for f in os.listdir(self.path)]
        for f in files:
            with open(f, "r") as fd:
                self.emit(fd.readlines())

    def process(self):
        pass
