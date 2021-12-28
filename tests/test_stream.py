import pytest
from pipeline import Stream
from pipeline.exception import PipelineException
from pipeline.operators import (
    FileInputOperator,
    InputOperator,
    InputOutputOperator,
    Operator,
)
from pipeline.pipeline import Pipeline


def test_stream_invalid_type():
    testee = Stream(name="stream1", operator={})
    with pytest.raises(PipelineException) as ex:
        testee.validate()
    assert "is not of type" in str(ex)


def test_stream_valid_type():
    testee = Stream(name="stream1", operator=FileInputOperator(path="/foo"))
    testee.validate()


def test_pipeline_invalid1():
    pipeline = Pipeline(Stream("stream1", FileInputOperator(path="/foo")))
    with pytest.raises(PipelineException) as ex:
        pipeline.validate()
    assert "At least 2 streams are required to" in str(ex)


class FooInputOutputOperator(InputOutputOperator):
    def process(self):
        pass


def test_pipeline_invalid2():
    pipeline = Pipeline(
        Stream("stream1", FooInputOutputOperator()),
        Stream("stream2", FooInputOutputOperator()),
    )
    with pytest.raises(PipelineException) as ex:
        pipeline.validate()
    assert f"First stream should be {InputOperator}" in str(ex)


def test_pipeline_invalid3():
    pipeline = Pipeline(
        Stream("stream1", FileInputOperator(path="/foo")),
        Stream("stream1", FooInputOutputOperator()),
    )
    with pytest.raises(PipelineException) as ex:
        pipeline.validate()
    assert "Name of streams in pipeline should be unique." in str(ex)


def test_pipeline_valid():
    pipeline = Pipeline(
        Stream("stream1", FileInputOperator(path="/foo")),
        Stream("stream2", FooInputOutputOperator()),
        Stream("stream3", FooInputOutputOperator()),
    )
    pipeline.validate()
