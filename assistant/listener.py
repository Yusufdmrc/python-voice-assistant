"""
Microphone listening and speech recognition module.
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from io import BytesIO
import wave


class Listener:
    """Handles microphone input and speech-to-text conversion."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        
        print("Adjusting for ambient noise... Please wait.")
        # Calibration recording
        duration = 1
        audio_data = sd.rec(int(duration * self.sample_rate), 
                           samplerate=self.sample_rate, 
                           channels=1, 
                           dtype='int16')
        sd.wait()
        print("Ready to listen!")
    
    def listen(self, timeout=5, phrase_time_limit=5):
        """
        Listen to microphone and return recognized text.
        
        Args:
            timeout: Maximum time to wait for phrase to start
            phrase_time_limit: Maximum time for phrase
            
        Returns:
            str: Recognized text in lowercase, or None if recognition fails
        """
        try:
            print("Listening...")
            
            # Record audio using sounddevice
            duration = phrase_time_limit if phrase_time_limit else 5
            audio_data = sd.rec(int(duration * self.sample_rate), 
                               samplerate=self.sample_rate, 
                               channels=1, 
                               dtype='int16')
            sd.wait()  # Wait until recording is finished
            
            # Convert to AudioData format for speech_recognition
            audio_bytes = BytesIO()
            with wave.open(audio_bytes, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            audio_bytes.seek(0)
            
            # Create AudioData object
            with sr.AudioFile(audio_bytes) as source:
                audio = self.recognizer.record(source)
            
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
