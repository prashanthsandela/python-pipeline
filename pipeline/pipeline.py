import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
from typing import List, Tuple, Union

from pipeline.exception import PipelineException
from pipeline.operators import InputOperator, Operator

logger = logging.getLogger(__name__)


class Pipeline:
    pass


class Stream:
    def __init__(
        self,
        name: str,
        operator: Operator,
        workers: int = 1,
        threadType: Union[ThreadPoolExecutor, ProcessPoolExecutor] = ThreadPoolExecutor,
    ) -> None:
        """Create a stream to process.

        Args:
            name (str): Name of the stream operator.
            operator (Operator): Operator object.
            workers (int, optional): Number of workers. Defaults to 1.
            threadType (Union[ThreadPoolExecutor, ProcessPoolExecutor], optional):
                Type of thread executor. Defaults to ThreadPoolExecutor. Not implemented.
        """
        self.name = name
        self.operator = operator
        self.workers = workers
        self.executor: Union[ThreadPoolExecutor, ProcessPoolExecutor] = threadType

    def validate(self):
        """Validate if current object is a valid stream.

        Raises:
            PipelineException: [description]
        """
        if not isinstance(self.operator, Operator):
            raise PipelineException(
                f"The object {self.name} is not of type {Operator}."
            )

    def start(self):
        Thread(name=self.name, target=self.operator.emitTuple).start()


class Pipeline:
    def __init__(self, *streams: Tuple[Stream]) -> None:
        """Initialize a pipeline."""
        self.streams: List[Stream] = [stream for stream in streams]
        self._t = []

    def add_stream(self, stream: Stream) -> None:
        """Add stream to existing pipeline streams.

        Args:
            stream (Stream): New stream to add.
        """
        self.streams.append(stream)

    def start(self) -> None:
        self.validate()

        # Join streams.
        for s1, s2 in zip(self.streams[:-1], self.streams[1:]):
            s2.operator.input = s1.operator.output

        [s.start() for s in self.streams]

        while True:
            pass

    def validate(self):
        """List of all valid pipelines.

        Raises:
            PipelineException: [description]
        """
        stream_names = {s.name for s in self.streams}
        if len(stream_names) != len(self.streams):
            raise PipelineException("Name of streams in pipeline should be unique.")

        if len(self.streams) < 2:
            raise PipelineException(
                f"At least 2 streams are required to start a pipeline."
            )

        # Validate input stream.
        input_stream = self.streams[0]
        if not isinstance(input_stream.operator, InputOperator):
            raise PipelineException(f"First stream should be {InputOperator}")

        # Validate rest of the streams.
        for stream in self.streams[1:]:
            stream.validate()
