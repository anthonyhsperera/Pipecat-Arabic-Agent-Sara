#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import os

from dotenv import load_dotenv
from loguru import logger

from pipecat.frames.frames import (
    Frame,
    OutputTransportMessageFrame,
    TranscriptionFrame,
    TTSStoppedFrame,
    TTSTextFrame,
)
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContext,
    OpenAILLMContextFrame,
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.processors.frameworks.rtvi import (
    RTVIConfig,
    RTVIObserver,
    RTVIProcessor,
    RTVIBotTranscriptionMessage,
    RTVITextMessageData,
    RTVIUserTranscriptionMessage,
    RTVIUserTranscriptionMessageData,
)
from pipecat.processors.transcript_processor import TranscriptProcessor
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.speechmatics.stt import SpeechmaticsSTTService
from pipecat.transcriptions.language import Language
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.daily.transport import DailyParams
from pipecat.transports.websocket.fastapi import FastAPIWebsocketParams
from pipecat.utils.time import time_now_iso8601

load_dotenv(override=True)


class TranscriptionLogger(FrameProcessor):
    """Logs transcriptions with speaker diarization information."""

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, TranscriptionFrame):
            logger.info(f"Transcription: {frame.text}")
            # If diarization is enabled, the text will include speaker tags like:
            # <S1>مرحبا، كيف حالك؟</S1>

        # Push all frames through
        await self.push_frame(frame, direction)


class ElevenLabsTTSTranscriptService(ElevenLabsTTSService):
    """ElevenLabs TTS that also emits TTSTextFrame transcripts."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Enable TTSTextFrame emission
        self._push_text_frames = True


# We store functions so objects don't get instantiated.
# The function will be called when the desired transport gets selected.
transport_params = {
    "daily": lambda: DailyParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        video_out_enabled=False,
    ),
    "twilio": lambda: FastAPIWebsocketParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
}


async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    """Run Arabic voice agent with Speechmatics STT, OpenAI LLM, and ElevenLabs TTS.

    This agent uses:
    - Speechmatics for Arabic speech-to-text with speaker diarization
    - OpenAI GPT-4 for conversational intelligence (strong Arabic support)
    - ElevenLabs for high-quality Arabic text-to-speech
    - RTVI protocol for proper transcript handling

    Diarization will output speaker tags like: <S1>text</S1>, <S2>text</S2>
    """
    logger.info("Starting Arabic Voice Agent with RTVI Support")

    # Configure Speechmatics STT for Arabic with diarization
    stt = SpeechmaticsSTTService(
        api_key=os.getenv("SPEECHMATICS_API_KEY"),
        params=SpeechmaticsSTTService.InputParams(
            language=Language.AR,  # Modern Standard Arabic
            enable_vad=True,
            end_of_utterance_silence_trigger=0.5,
            enable_diarization=True,
            speaker_active_format="<{speaker_id}>{text}</{speaker_id}>",
            operating_point="enhanced",
            speaker_sensitivity=0.7,
        ),
    )

    # Transcription logger to see who said what
    transcription_logger = TranscriptionLogger()

    # Configure OpenAI LLM (GPT-4 recommended for Arabic)
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    )

    # Configure ElevenLabs TTS for Arabic with text frame emission enabled
    tts = ElevenLabsTTSTranscriptService(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        voice_id=os.getenv("ELEVENLABS_VOICE_ID", "tavIIPLplRB883FzWU0V"),
        model=os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
        params=ElevenLabsTTSService.InputParams(
            stability=0.65,
            similarity_boost=0.60,
        ),
    )

    # System prompt for the Arabic agent
    messages = [
    {
        "role": "system",
        "content": (
            "The user will be speaking Arabic. ONLY ever respond using Modern Standard Arabic (MSA). Assume the speaker is male unless they have told you otherwise.\n\n"
            "أنت موظف استقبال ودود في مطعم برجر. اسمك سارة. "
            "هدفك هو أخذ الطلبات بطريقة سريعة وواضحة ومساعدة العملاء في اختيار وجباتهم. "
            "مخرجاتك ستتحول إلى صوت لذا لا تستخدم رموزًا خاصة أو إيموجي في إجاباتك. "
            "استخدم علامات الترقيم دائمًا في ردودك. "
            "قدم ردودًا قصيرة ومباشرة - لا تطيل إلا إذا لزم الأمر. "
            "\n\n"
            "قائمة الطعام:\n"
            "- برجر كلاسيك (٢٥ ريال)\n"
            "- برجر دبل (٣٥ ريال)\n"
            "- برجر نباتي فلافل (٢٢ ريال)\n"
            "- برجر خضار مشوي (٢٤ ريال)\n"
            "- بطاطس مقلية صغيرة (٨ ريال) أو كبيرة (١٢ ريال)\n"
            "- مشروبات: كولا، سبرايت، عصير برتقال (٧ ريال)\n"
            "- ميلك شيك فانيليا أو شوكولاتة (١٥ ريال)\n"
            "\n"
            "عند أخذ الطلب:\n"
            "١. رحب بالعميل واسأله عن طلبه\n"
            "٢. استخدم علامات `<S1/>` `<S2/>` `<S3/>` لتمييز المتحدثين المختلفين - لا تستخدم هذه العلامات في ردودك أبدًا\n"
            "٣. سجل من طلب ماذا بوضوح (مثال: الشخص الأول طلب برجر كلاسيك)\n"
            "٤. اقترح الخيارات النباتية إذا سأل العميل أو بدا مهتمًا\n"
            "٥. اسأل عن الإضافات: بطاطس ومشروبات\n"
            "٦. أكد الطلب الكامل مع الأسعار قبل الإنهاء\n"
            "٧. اذكر المجموع النهائي\n"
            "\n"
            "كن ودودًا وصبورًا ومساعدًا. إذا كان هناك عدة أشخاص يطلبون، تأكد من تتبع طلب كل شخص بدقة."
        ),
    },
    ]
    # Create RTVI processor with configuration
    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    # Create transcript processor
    transcripts = TranscriptProcessor()

    # Create shared OpenAI LLM context and aggregators for user/assistant messages
    context = OpenAILLMContext.from_messages(messages)
    context_aggregators = llm.create_context_aggregator(context)
    user_response = context_aggregators.user()
    assistant_response = context_aggregators.assistant()

    user_transcript = transcripts.user()
    assistant_transcript = transcripts.assistant()

    # Build the conversational pipeline with RTVI support
    pipeline = Pipeline(
        [
            transport.input(),  # Audio input
            rtvi,  # RTVI processor for handling client-server messages
            stt,  # Speech-to-text (Arabic, with diarization)
            transcription_logger,  # Log transcriptions with speaker info (for debugging)
            user_transcript,  # Process user transcripts (with diarization tags)
            user_response,  # Aggregate user messages
            llm,  # LLM processing
            tts,  # Text-to-speech (Arabic) - emits TTSTextFrames
            transport.output(),  # Audio output
            assistant_transcript,  # Process assistant transcripts (uses TTSTextFrames)
            assistant_response,  # Aggregate assistant messages
        ]
    )

    # Create and configure the task with RTVI observer
    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
        ),
        observers=[RTVIObserver(rtvi)],  # Add RTVI observer for message handling
        idle_timeout_secs=runner_args.pipeline_idle_timeout_secs,
    )

    # Event handler for when first participant joins
    @transport.event_handler("on_first_participant_joined")
    async def on_first_participant_joined(transport, participant):
        logger.info(f"First participant joined: {participant.get('identity', 'unknown')}")
        # Initialize the conversation with the system prompt
        await task.queue_frames([OpenAILLMContextFrame(context)])

    # Event handler for RTVI client ready
    @rtvi.event_handler("on_client_ready")
    async def on_client_ready(rtvi):
        logger.info("RTVI client ready")
        # Signal bot is ready to receive messages
        await rtvi.set_bot_ready()

    # Event handler for client disconnection
    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    # Run the pipeline
    runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """Main bot entry point compatible with Pipecat Cloud."""
    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()