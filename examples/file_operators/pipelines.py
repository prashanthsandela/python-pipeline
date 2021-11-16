from pipeline import Pipeline, Stream
from pipeline.operators import FileInputOperator, InputOutputOperator, OutputOperator


class ForwardInputOutputOperator(InputOutputOperator):
    def process(self, data: str) -> str:
        return data


class FileOutputOperator(OutputOperator):
    def __init__(self) -> None:
        self.file = "examples/file_operators/resources/outputs/output.txt"

    def process(self, data: str) -> None:
        with open(self.file, "a+") as fd:
            fd.write(data + "\n")


pipeline = Pipeline(
    Stream(
        "read_lines", FileInputOperator(path="examples/file_operators/resources/files")
    ),
    Stream("forward", ForwardInputOutputOperator()),
    Stream("output_lines", FileOutputOperator()),
).start()
