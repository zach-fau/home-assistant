"""Echo bot pipeline orchestration using Pipecat.

This module implements a complete voice pipeline that echoes back what the user says,
validating the entire STT -> TTS pipeline with proper audio I/O, interruption handling,
and latency measurement.
"""

import asyncio
import sys
import time
from typing import Optional

try:
    from pipecat.frames.frames import (
        Frame,
        TextFrame,
        TranscriptionFrame,
        StartFrame,
        EndFrame,
    )
    from pipecat.pipeline.pipeline import Pipeline
    from pipecat.pipeline.runner import PipelineRunner
    from pipecat.pipeline.task import PipelineTask, PipelineParams
    from pipecat.processors.frame_processor import FrameProcessor
except ImportError:
    print("Error: pipecat-ai is not installed.", file=sys.stderr)
    print("Please install with: pip install 'pipecat-ai[local,deepgram,cartesia]'", file=sys.stderr)
    sys.exit(1)

from src.config import AppConfig
from src.logger import get_logger
from src.pipeline.audio_transport import create_local_audio_transport
from src.pipeline.deepgram_stt import create_deepgram_stt_service
from src.pipeline.cartesia_tts import create_cartesia_tts_service

logger = get_logger(__name__)


class EchoProcessor(FrameProcessor):
    """Process transcription frames and echo them back as text for TTS.

    This processor:
    - Receives transcription frames from STT
    - Measures latency
    - Echoes the text back for TTS
    - Logs the conversation flow
    """

    def __init__(self):
        """Initialize the echo processor."""
        super().__init__()
        self._transcription_start_time: Optional[float] = None
        self._message_count = 0

    async def process_frame(self, frame: Frame, direction):
        """Process frames passing through the pipeline.

        Args:
            frame: The frame to process
            direction: Direction of frame flow
        """
        # Always call parent first to initialize properly
        await super().process_frame(frame, direction)

        # Handle transcription frames (from STT)
        if isinstance(frame, TranscriptionFrame):
            text = frame.text.strip()

            # Only process non-empty final transcriptions
            if text and not getattr(frame, "is_interim", False):
                self._message_count += 1

                # Calculate latency if we have a start time
                latency = None
                if self._transcription_start_time:
                    latency = time.time() - self._transcription_start_time

                logger.info(
                    "Received transcription",
                    text=text,
                    message_num=self._message_count,
                    latency_ms=int(latency * 1000) if latency else None,
                )

                # Echo the text back
                echo_text = f"You said: {text}"
                logger.info("Echoing back", echo_text=echo_text)

                # Create and push text frame for TTS
                text_frame = TextFrame(echo_text)
                await self.push_frame(text_frame)

                # Reset start time for next transcription
                self._transcription_start_time = time.time()

                # Don't push the original transcription frame
                return

        # Handle start frame
        elif isinstance(frame, StartFrame):
            self._transcription_start_time = time.time()
            logger.info("Echo processor started")

        # Handle end frame
        elif isinstance(frame, EndFrame):
            logger.info(
                "Echo processor ended",
                total_messages=self._message_count,
            )

        # Push all other frames through
        await self.push_frame(frame, direction)


class LatencyMonitor(FrameProcessor):
    """Monitor and log pipeline latency metrics."""

    def __init__(self):
        """Initialize the latency monitor."""
        super().__init__()
        self._stt_start_time: Optional[float] = None
        self._tts_start_time: Optional[float] = None

    async def process_frame(self, frame: Frame, direction):
        """Monitor frame timing for latency measurement.

        Args:
            frame: The frame to monitor
            direction: Direction of frame flow
        """
        await super().process_frame(frame, direction)

        # Measure STT latency
        if isinstance(frame, TranscriptionFrame):
            if self._stt_start_time and not getattr(frame, "is_interim", False):
                stt_latency = time.time() - self._stt_start_time
                logger.debug(
                    "STT latency",
                    latency_ms=int(stt_latency * 1000),
                )
                self._stt_start_time = None

        # Measure TTS latency
        elif isinstance(frame, TextFrame):
            self._tts_start_time = time.time()
            logger.debug("TTS processing started")

        await self.push_frame(frame, direction)


async def run_echo_bot(config: AppConfig, duration: Optional[int] = None):
    """Run the echo bot pipeline.

    Args:
        config: Application configuration
        duration: Optional duration to run in seconds (None = run until interrupted)

    Raises:
        RuntimeError: If pipeline setup or execution fails
    """
    logger.info("Starting echo bot pipeline")

    try:
        # Create transport
        transport = create_local_audio_transport(config.audio)

        # Create STT service
        stt_service = create_deepgram_stt_service(
            config.api_keys,
            config.pipeline,
        )

        # Create TTS service
        tts_service = create_cartesia_tts_service(
            config.api_keys,
            config.pipeline,
        )

        # Create echo processor
        echo_processor = EchoProcessor()

        # Create latency monitor
        latency_monitor = LatencyMonitor()

        # Create pipeline: audio in -> STT -> echo -> TTS -> audio out
        pipeline = Pipeline([
            transport.input(),
            stt_service,
            latency_monitor,
            echo_processor,
            tts_service,
            transport.output(),
        ])

        # Configure pipeline parameters
        params = PipelineParams(
            allow_interruptions=config.pipeline.enable_interruptions,
            audio_in_sample_rate=config.audio.sample_rate,
            audio_out_sample_rate=config.audio.sample_rate,
        )

        # Create pipeline task
        task = PipelineTask(
            pipeline,
            params=params,
        )

        # Add event handlers
        @task.event_handler("on_pipeline_started")
        async def on_started(task, frame: StartFrame):
            logger.info(
                "Pipeline started",
                interruptions_enabled=config.pipeline.enable_interruptions,
                sample_rate=config.audio.sample_rate,
            )

        @task.event_handler("on_pipeline_stopped")
        async def on_stopped(task):
            logger.info("Pipeline stopped")

        # Create and run pipeline runner
        runner = PipelineRunner()

        # If duration specified, run with timeout
        if duration:
            logger.info(f"Running echo bot for {duration} seconds...")
            try:
                await asyncio.wait_for(runner.run(task), timeout=duration)
            except asyncio.TimeoutError:
                logger.info(f"Echo bot duration of {duration} seconds completed")
        else:
            logger.info("Running echo bot (press Ctrl+C to stop)...")
            await runner.run(task)

    except KeyboardInterrupt:
        logger.info("Echo bot interrupted by user")
    except Exception as e:
        logger.exception(f"Echo bot pipeline failed: {e}")
        raise RuntimeError(f"Echo bot execution failed: {e}") from e
    finally:
        logger.info("Echo bot shutdown complete")


async def main():
    """Main entry point for standalone echo bot execution."""
    from src.config import get_config

    try:
        config = get_config()
        await run_echo_bot(config)
    except Exception as e:
        logger.exception(f"Failed to run echo bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
