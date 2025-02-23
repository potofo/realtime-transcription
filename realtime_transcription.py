# Sample code for transcribing audio from a microphone in near real time using the Azure OpenAI Whisper API
# LICENSE: MIT License

import os
import time
import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai
import pyaudio
import wave
import queue

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("AZURE_OPENAI_API_HOST")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

class RealtimeTranscriber:
    def __init__(self):
        # Recording settings
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        
        # Calculate chunk size from seconds
        chunk_seconds = float(os.getenv("AUDIO_CHUNK_SECONDS", "25"))  # Default 25 seconds
        self.CHUNK = int(self.RATE * chunk_seconds)  # Sampling Rate × Seconds
        
        self.is_recording = False
        self.audio_queue = queue.Queue()
        
        # Create directories for saving files
        self.audio_dir = Path("audio")
        self.transcription_dir = Path("transcription")
        self.audio_dir.mkdir(exist_ok=True)
        self.transcription_dir.mkdir(exist_ok=True)
        self.chunk_counter = 0

    def save_transcription(self, text, audio_filename):
        """Save transcription results to a file"""
        try:
            # Save with the same name as the audio file (change extension to txt)
            txt_filename = self.transcription_dir / Path(audio_filename).stem
            filepath = txt_filename.with_suffix('.txt')
            
            # Ensure the output directory exists
            self.transcription_dir.mkdir(exist_ok=True)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            
            # Display results in a readable format
            print("\n" + "="*50)
            print(f"🎤 Speech Recognition Result ({Path(audio_filename).name})")
            print("="*50)
            print(text)
            print("="*50)
            print(f"✅ Saved: {filepath}\n")
            
        except Exception as e:
            print(f"\n❌ Error occurred while saving transcription results: {e}")
            print(f"Text: {text}")

    def save_audio_chunk(self, audio_data):
        """Save audio chunk as WAV file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.audio_dir / f"chunk_{timestamp}_{self.chunk_counter:04d}.wav"
        
        # Save as WAV file
        with wave.open(str(filename), 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
        
        self.chunk_counter += 1
        return filename

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Add audio data to queue, save as WAV file, and send to audio stream"""
        if self.is_recording:
            self.audio_queue.put(in_data)
            filename = self.save_audio_chunk(in_data)
            print(f"✅ Audio chunk saved: {filename}")
            
            # Send audio data to Azure Speech SDK stream
            if hasattr(self, 'audio_stream'):
                try:
                    self.audio_stream.write(in_data)
                except Exception as e:
                    print(f"⚠️ Error while sending audio stream: {e}")
        
        return (in_data, pyaudio.paContinue)

    def get_default_input_device_index(self):
        """Get the index of the default input device"""
        audio = pyaudio.PyAudio()
        default_device_index = audio.get_default_input_device_info()['index']
        audio.terminate()
        return default_device_index

    def transcribe_audio(self, audio_file):
        """Transcribe WAV file using Whisper model"""
        try:
            with open(audio_file, "rb") as audio:
                result = openai.Audio.transcribe(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model="whisper-1",
                    deployment_id=os.getenv("AZURE_DEPLOYMENT_ID"),
                    file=audio,
                    language="ja"
                )
                return result["text"].strip()
        except Exception as e:
            print(f"\n❌ Error occurred during transcription: {e}")
            return None

    def process_audio(self):
        """Process audio data and transcribe"""
        audio = pyaudio.PyAudio()
        default_device_index = self.get_default_input_device_index()
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=default_device_index,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )

        print("\n🎙️ Starting recording...")
        print("Recognizing audio... (Press Ctrl+C to stop)\n")
        self.is_recording = True
        stream.start_stream()

        try:
            chunk_seconds = float(os.getenv("AUDIO_CHUNK_SECONDS", "10"))
            print(f"\n⏱️ Audio chunk size: {chunk_seconds} seconds")
            
            while self.is_recording:
                # Record audio chunk
                time.sleep(chunk_seconds)
                
                # Get the latest audio file and transcribe
                try:
                    latest_audio_file = sorted(self.audio_dir.glob("*.wav"))[-1]
                    print(f"\n🎯 Transcribing audio file: {latest_audio_file}")
                    
                    text = self.transcribe_audio(str(latest_audio_file))
                    if text:
                        self.save_transcription(text, str(latest_audio_file))
                except IndexError:
                    print("\n⚠️ No audio files found")
                except Exception as e:
                    print(f"\n❌ Error occurred during processing: {e}")

        except KeyboardInterrupt:
            print("\n⏹️ Stopping recording...")
            self.is_recording = False

        finally:
            # PyAudio cleanup
            try:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                print("✅ Recording resources released")
            except Exception as e:
                print(f"⚠️ Error while releasing recording resources: {e}")

def main():
    transcriber = RealtimeTranscriber()
    try:
        transcriber.process_audio()
    except KeyboardInterrupt:
        print("\n👋 Exiting program...")

if __name__ == "__main__":
    main()