from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from .utils import wrap as otel_wrap, unwrap as otel_unwrap

from discord.ext import commands
from discord import TextChannel


class DiscordPyInstrumentor(BaseInstrumentor):
    """An instrumentor for discord.py

    This instrumentor automatically traces key discord.py operations, such as command processing and message sending.
    """

    _instrumented = False

    def instrumentation_dependencies(self) -> set:
        """Specify dependencies required for instrumentation"""
        # Return a set of dependencies necessary for the instrumentation.
        # For discord.py, you might not have external dependencies specifically for instrumentation,
        # so it's okay to return an empty set if that's the case.
        return set()

    def _instrument(self, **kwargs):
        """Instrument discord.py operations"""
        if self._instrumented:
            return

        # Instrument command processing
        from discord.ext.commands import Bot

        otel_wrap(
            commands.Bot,
            "process_commands",
            self._wrapper_process_commands,
        )

        # Instrument message sending
        from discord.channel import TextChannel

        # Instrument message sending
        otel_wrap(
            TextChannel,  # Correctly reference the TextChannel class
            "send",
            self._wrapper_send_message,
        )

        self._instrumented = True

    def _uninstrument(self, **kwargs):
        """Uninstrument discord.py operations"""
        if not self._instrumented:
            return

        # Uninstrument command processing
        otel_unwrap(commands.Bot, "process_commands")

        # Uninstrument message sending
        otel_unwrap(TextChannel, "send")

        self._instrumented = False

    def _wrapper_process_commands(self, original, instance, args, kwargs):
        """Wrapper for the Bot.process_commands method"""
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Bot.process_commands"):
            # Ensure original is called with its instance and the forwarded arguments
            return original(instance, *args, **kwargs)

    async def _wrapper_send_message(self, original, instance, args, kwargs):
        """Wrapper for the TextChannel.send method"""
        print("Wrapping TextChannel.send")
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("TextChannel.send") as span:
            try:
                # Optionally add more span attributes here
                # span.set_attribute("key", "value")

                result = await original(*args, **kwargs)
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
