import json
import datetime
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace import set_span_in_context

from opentelemetry import propagate
from opentelemetry.propagators.textmap import DefaultSetter
from opentelemetry.propagators.textmap import DefaultGetter

from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.trace import ReadableSpan
import typing
from pathlib import Path
from os import linesep
from typing import Optional

from rich.traceback import install
from rich.logging import RichHandler
from rich import print, inspect, print_json
from rich.panel import Panel
from rich.padding import Padding

install()


class FileSpanExporter(SpanExporter):
    """
    Implementation of :class:`SpanExporter` that prints spans to a given file.
    """

    def __init__(
        self,
        file_path_getter: typing.Callable[[], str],
        service_name: Optional[str] = None,
        formatter: typing.Callable[[ReadableSpan], str] = lambda span: span.to_json()
        + linesep,
    ):
        self.file_path_getter = file_path_getter
        self.formatter = formatter
        self.service_name = service_name
        self.buffered_spans = []

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        """
        If the path returned by self.file_path_getter exists,
        writes the given spans (and any previously saved spans)
        to a file under that path.
        Else, it saves the spans in self.buffered_spans,
        in hopes that in a future call the path will have been created.
        """
        self.buffered_spans.append(spans)

        file_path = self.file_path_getter()

        if file_path is not None and Path(file_path).exists():
            with open(Path(file_path, "otlp_trace"), "a") as file:
                for bspans in self.buffered_spans:
                    for span in bspans:
                        file.write(self.formatter(span))
                file.flush()
            self.buffered_spans.clear()

        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class EventsOTLP:
    """
    Handles event tracing using OpenTelemetry
    (or the console on the user's local environment).
    """

    def __init__(self, log=None, destination=None, otlp_url=None, trace_context=None):        
        self.log = log
        self.otlp_url = otlp_url # "localhost:3417"
        self.destination = destination
        self.seq = 0

        # if the trace was started on the cluster by a different entity (e.g. the worker),
        # its context is given by an environment variable.            
        if trace_context:            
            self.otlp_context = {"traceparent": trace_context}
        else:
            self.otlp_context = None

        self.otlp_processor = None
        self.file_processor = None
        self.tracer = None

    def setup_tracer(self):
        # Service name is required for most backends
        resource = Resource(attributes={SERVICE_NAME: "citros-sim"})

        provider = TracerProvider(resource=resource)

        # the citros run dir is only created before a simulation run,
        # so it must be retrieved dynamically.
        if self.destination:
            file_exporter = FileSpanExporter(lambda: self.destination)
            file_processor = BatchSpanProcessor(file_exporter)
            provider.add_span_processor(file_processor)
            self.file_processor = file_processor

        if self.otlp_url:
            # when running in the cluster, the telop collector (k8s deamonset)
            # is allways local for the pod it is running on.
            otlp_exporter = OTLPSpanExporter(
                endpoint=self.self.otlp_url, insecure=True
            )
            otlp_processor = BatchSpanProcessor(otlp_exporter)
            provider.add_span_processor(otlp_processor)
            self.otlp_processor = otlp_processor

        trace.set_tracer_provider(provider)

        return trace.get_tracer("citros-events-tracer")

    def on_shutdown(self):
        """
        Ensures that any remaining spans in the queue are flushed and sent to the exporter.
        """
        if self.file_processor:
            self.file_processor.shutdown()
        if self.otlp_processor:
            self.otlp_processor.shutdown()

    def serialize_current_context(self):
        """
        return value is a dictionary of the form
        {'traceparent': '00-<trace_id>-<span-id>-<some other id>'}
        example:
        {'traceparent': '00-cb9cfff1dd2ba53e9b09360fedb78bb7-bcbc4396d4ae74c4-01'}
        """
        carrier = {}
        PROPAGATOR = propagate.get_global_textmap()
        PROPAGATOR.inject(carrier, setter=DefaultSetter())
        return carrier

    def deserialize_to_context(self, metadata):
        PROPAGATOR = propagate.get_global_textmap()
        return PROPAGATOR.extract(metadata, getter=DefaultGetter())

    def set_span_attributes(
        self, span, event_type, tag, message, metadata
    ):
        # span.set_attribute("batch-run-id", batch_run_id)
        # span.set_attribute("sid", sid)
        span.set_attribute("event-type", event_type)
        span.set_attribute("tag", tag)
        span.set_attribute("message", message)
        span.set_attribute("metadata", metadata)
        span.set_attribute("created", datetime.datetime.now().isoformat())
        span.set_attribute("emit-sequence", self.seq)
        self.seq = self.seq + 1


    def emit(self, event_type, tag, message, metadata):
        """
        Creates a new span and sets its attributes with the given arguments.
        If self.otlp_context has not been set, the span will be started as the root span.
        Else, the span will be started with the span in the self.otlp_context as parent.

        
        :param event: event type
        :param tag: tag - can be any string
        :param message: a message for the event
        :param metadata: some dict object containing metadata.
        """
        if self.tracer is None:
            self.tracer = self.setup_tracer()

        try:
            if isinstance(metadata, dict):
                metadata = json.dumps(metadata)
        except Exception as e:            
            if self.log:
                self.log.exception(e)
            else:
                print(e)
            metadata = None

        if metadata is None:
            metadata = ""

        if self.otlp_context is None:
            with self.tracer.start_as_current_span(event_type) as span:
                self.set_span_attributes(
                    span, event_type, tag, message, metadata
                )
                self.otlp_context = self.serialize_current_context()
        else:
            # create a new span with the current span as parent.
            context = self.deserialize_to_context(self.otlp_context)
            span = self.tracer.start_span(event_type, context=context)

            with trace.use_span(span, end_on_exit=True):
                self.set_span_attributes(
                    span, event_type, tag, message, metadata
                )
                self.otlp_context = self.serialize_current_context()

    def schedule(self, tag="", message="", metadata=None):
        """
        Sends event of type SCHEDULE to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("SCHEDULE", tag, message, metadata)

    def creating(self, tag="", message="", metadata=None):
        """
        Sends event of type CREATING to CiTROS

        
        :param tag: tag - can be any string
        :param message: a message for the event
        :param metadata: some dict object containing metadata.
        """
        self.emit("CREATING", tag, message, metadata)

    def init(self, tag="", message="", metadata=None):
        """
        Sends event of type INIT to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("INIT", tag, message, metadata)

    def starting(self, tag="", message="", metadata=None):
        """
        Sends event of type STARTING to CiTROS
        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("STARTING", tag, message, metadata)

    def running(self, tag="", message="", metadata=None):
        """
        Sends event of type RUNNING to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("RUNNING", tag, message, metadata)

    def terminating(self, tag="", message="", metadata=None):
        """
        Sends event of type TERMINATING to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("TERMINATING", tag, message, metadata)

    def stopping(self, tag="", message="", metadata=None):
        """
        Sends event of type STOPPING to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("STOPPING", tag, message, metadata)

    def done(self, tag="", message="", metadata=None):
        """
        Sends event of type DONE to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("DONE", tag, message, metadata)

    def error(self, tag="", message="", metadata=None):
        """
        Sends event of type ERROR to CiTROS

        
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit("ERROR", tag, message, metadata)
