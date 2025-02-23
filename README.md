# Real-time Speech-to-Text Sample Code using Azure OpenAI's Whisper API

## Overview

This project is a Python application that records audio from a microphone in real-time and converts it to text using the Azure OpenAI Whisper model. The audio is automatically processed at regular intervals, and the transcription results are saved as files.

## Features

- Real-time audio recording
- Automatic audio chunk splitting and saving
- High-accuracy transcription using Azure OpenAI Whisper model
- Japanese language support
- Real-time display and automatic saving of transcription results

## Requirements

- Python 3.8 or higher
- Azure OpenAI account and API configuration
- Required Python packages:
  ```
  python-dotenv==1.0.0
  openai==0.28.1
  PyAudio==0.2.14
  ```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/potofo/realtime-transcription.git
   cd realtime-transcription
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env_template` to `.env`
   - Set the following parameters:
     ```
     OPENAI_API_TYPE=azure
     OPENAI_API_HOST=your_endpoint_here
     OPENAI_API_KEY=your_api_key_here
     OPENAI_API_VERSION=2024-06-01
     AZURE_DEPLOYMENT_ID=whisper
     
     # Audio recording settings
     AUDIO_CHUNK_SECONDS=25  # Chunk size in seconds
     ```
     Note:
       Azure OpenAI's Whisper has rate limits (3 requests per minute). Therefore, setting AUDIO_CHUNK_SECONDS to 21 seconds or less will cause the API to respond with an error.
       AUDIO_CHUNK_SECONDS = 25  # Chunk size (seconds)

## Usage

1. Launch the application:
   ```bash
   python realtime_transcription.py
   ```

2. Operation:
   - Recording starts automatically when the program launches
   - Audio is split into chunks at specified intervals (default: 25 seconds)
   - Each chunk is automatically transcribed, and results are displayed
   - Press `Ctrl+C` to exit

## File Structure

```
realtime-transcription/
├── realtime_transcription.py  # Main script
├── requirements.txt           # List of dependencies
├── .env_template             # Environment variables template
├── audio/                    # Directory for recorded audio files
└── transcription/           # Directory for transcription results
```

## Output Files

- Audio files: `audio/chunk_[timestamp]_[sequence].wav`
- Transcription results: `transcription/chunk_[timestamp]_[sequence].txt`

## Error Handling

- Audio device connection errors
- API communication errors
- File saving errors

All errors are properly handled and appropriate error messages are displayed.

## License

MIT License

## Important Notes

- Requires an adequate audio input device (microphone)
- Requires a stable internet connection
- May incur Azure OpenAI API usage fees

## Contributing

Bug reports and feature improvement suggestions are welcome through Issues or Pull Requests.

---