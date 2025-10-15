# Pipecat Arabic Voice Agent (Sara)

An intelligent Arabic voice agent built with [Pipecat](https://github.com/pipecat-ai/pipecat) for real-time conversational AI. This agent demonstrates a restaurant ordering scenario with multi-speaker support, speaker diarization, and high-quality Arabic speech processing.

## Features

- **Arabic Speech Recognition**: Powered by [Speechmatics](https://www.speechmatics.com/) with real-time Modern Standard Arabic (MSA) transcription
- **Speaker Diarization**: Automatically detects and labels multiple speakers in conversations (e.g., `<S1>`, `<S2>`)
- **Conversational AI**: Uses OpenAI GPT-4 with excellent Arabic language understanding
- **Natural Arabic Voice**: High-quality text-to-speech using [ElevenLabs](https://elevenlabs.io/)
- **RTVI Protocol**: Built on the Real-Time Voice Inference protocol for standardized voice interactions
- **Multi-Speaker Support**: Handles complex scenarios with multiple customers ordering simultaneously

## Use Case: Sara - Restaurant Burger Ordering Agent

Sara is a friendly restaurant receptionist who:
- Takes burger orders from customers in Arabic
- Tracks multiple customers and their individual orders
- Suggests menu items including vegetarian options
- Confirms orders with prices
- Provides total cost calculation

### Sample Menu
- Classic Burger (25 SAR)
- Double Burger (35 SAR)
- Vegetarian Falafel Burger (22 SAR)
- Grilled Vegetable Burger (24 SAR)
- Fries: Small (8 SAR) / Large (12 SAR)
- Drinks: Cola, Sprite, Orange Juice (7 SAR)
- Milkshakes: Vanilla or Chocolate (15 SAR)

## Architecture

```
┌─────────────────┐
│  Audio Input    │
│   (Microphone)  │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│  Speechmatics STT               │
│  - Arabic Recognition           │
│  - Speaker Diarization          │
│  - VAD (Voice Activity Detect)  │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│  OpenAI GPT-4                   │
│  - Arabic Language Processing   │
│  - Context Management           │
│  - Order Logic                  │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│  ElevenLabs TTS                 │
│  - Arabic Voice Synthesis       │
│  - Natural Intonation           │
└────────┬────────────────────────┘
         │
         v
┌─────────────────┐
│  Audio Output   │
│   (Speakers)    │
└─────────────────┘
```

## Prerequisites

- Python 3.10 or higher
- API keys for:
  - [Speechmatics](https://www.speechmatics.com/)
  - [OpenAI](https://platform.openai.com/)
  - [ElevenLabs](https://elevenlabs.io/)
  - (Optional) [Daily](https://www.daily.co/) for Daily transport

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Pipecat-Arabic-Agent-Sara.git
cd Pipecat-Arabic-Agent-Sara
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Required API Keys
SPEECHMATICS_API_KEY=your_speechmatics_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional: Customize models and voices
OPENAI_MODEL=gpt-4o
ELEVENLABS_VOICE_ID=tavIIPLplRB883FzWU0V
ELEVENLABS_MODEL=eleven_multilingual_v2
```

## Usage

### Running the Agent Locally

**Recommended:** Use local WebRTC transport for testing with Pipecat Playground:

```bash
python agent.py --transport webrtc --port 7860
```

The agent will be available at `http://localhost:7860`

### Connect to Pipecat Playground

1. **Run the Agent**: Start the agent with the command above
2. **Open Your Browser**: Navigate to `http://localhost:7860`
3. **Start Speaking**: Allow microphone access and start speaking in Arabic!

The Pipecat WebRTC client interface will load automatically at the default port.

### Transport Options

Pipecat supports multiple transport options:

#### 1. WebRTC Transport (Recommended)
**Best for:** Local testing, Pipecat Playground integration, no cloud dependencies

```bash
python agent.py --transport webrtc --port 7860
```

- Runs completely locally on your machine
- No Daily account or room setup needed
- Perfect for development and testing
- Built-in WebRTC client at `http://localhost:7860`

#### 2. Daily Transport
**Best for:** Production deployments, cloud-based voice chat

```bash
python agent.py --transport daily --port 7860
```

- Creates Daily.co WebRTC rooms automatically
- Requires `DAILY_API_KEY` in `.env`
- Great for production voice applications

#### 3. Twilio Transport
**Best for:** Phone call integrations

```bash
python agent.py --transport twilio --port 7860
```

### Command Line Arguments

```bash
python agent.py [OPTIONS]

Options:
  --transport TYPE          Transport type (daily, twilio, webrtc)
  --config-url URL         Configuration URL for transport
  --idle-timeout SECONDS   Pipeline idle timeout (default: 300)
  --help                   Show help message
```

## API Key Setup

### Speechmatics
1. Sign up at [speechmatics.com](https://www.speechmatics.com/)
2. Navigate to API Keys section
3. Generate a new API key
4. Add to `.env` as `SPEECHMATICS_API_KEY`

### OpenAI
1. Sign up at [platform.openai.com](https://platform.openai.com/)
2. Go to API Keys section
3. Create a new secret key
4. Add to `.env` as `OPENAI_API_KEY`
5. Recommended model: `gpt-4o` for best Arabic performance

### ElevenLabs
1. Sign up at [elevenlabs.io](https://elevenlabs.io/)
2. Go to Profile → API Keys
3. Generate a new API key
4. Add to `.env` as `ELEVENLABS_API_KEY`
5. Browse [Voice Library](https://elevenlabs.io/voice-library) for Arabic voices
6. Copy your preferred voice ID to `ELEVENLABS_VOICE_ID`

### Daily (Optional)
1. Sign up at [daily.co](https://www.daily.co/)
2. Get your API key from the dashboard
3. Create a room and get the room URL
4. Add both to `.env` as `DAILY_API_KEY` and `DAILY_ROOM_URL`

## Customization

### Modify the System Prompt

Edit the `messages` list in `agent.py` (lines 141-173) to customize Sara's behavior, personality, or menu items.

### Change Voice Settings

Adjust ElevenLabs TTS parameters in `agent.py` (lines 134-137):

```python
params=ElevenLabsTTSService.InputParams(
    stability=0.65,        # 0-1: Lower = more variation
    similarity_boost=0.60, # 0-1: Higher = closer to original voice
)
```

### Adjust Speaker Diarization

Modify Speechmatics STT settings in `agent.py` (lines 108-118):

```python
params=SpeechmaticsSTTService.InputParams(
    language=Language.AR,
    enable_diarization=True,
    speaker_active_format="<{speaker_id}>{text}</{speaker_id}>",
    operating_point="enhanced",  # Options: standard, enhanced
)
```

## Troubleshooting

### Common Issues

**Issue**: "API key not found" error
- **Solution**: Verify `.env` file exists and contains valid API keys
- **Solution**: Ensure environment variables are loaded (check `load_dotenv()` is called)

**Issue**: Poor Arabic recognition quality
- **Solution**: Ensure you're using `Language.AR` for Speechmatics
- **Solution**: Check microphone audio quality and sampling rate
- **Solution**: Try `operating_point="enhanced"` for better accuracy

**Issue**: Speaker diarization not working
- **Solution**: Verify `enable_diarization=True` in Speechmatics params
- **Solution**: Ensure clear audio with distinct speakers
- **Solution**: Check `speaker_active_format` is set correctly

**Issue**: Agent responds in English instead of Arabic
- **Solution**: Verify system prompt starts with "ONLY ever respond using Modern Standard Arabic"
- **Solution**: Check OpenAI model supports Arabic (GPT-4 recommended)

**Issue**: No audio output
- **Solution**: Check transport configuration (audio_out_enabled=True)
- **Solution**: Verify ElevenLabs API key and voice ID are valid
- **Solution**: Test audio output device

### Debugging

Enable verbose logging by setting the log level:

```python
from loguru import logger
logger.level = "DEBUG"
```

Check transcription logs to see recognized speech:

```
INFO: Transcription: <S1>مرحبا، أريد برجر كلاسيك</S1>
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the BSD 2-Clause License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Pipecat Documentation](https://docs.pipecat.ai/)
- [Speechmatics API Docs](https://docs.speechmatics.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)
- [RTVI Protocol](https://docs.pipecat.ai/guides/rtvi/)

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Pipecat-Arabic-Agent-Sara/issues)
- **Pipecat Community**: [Discord](https://discord.gg/pipecat)

## Acknowledgments

- Built with [Pipecat](https://github.com/pipecat-ai/pipecat) by Daily
- Speech recognition by Speechmatics
- AI powered by OpenAI
- Voice synthesis by ElevenLabs

---

Made with ❤️ for the Arabic-speaking community
