"""
Microphone listening and speech recognition module.
"""

import speech_recognition as sr


class Listener:
    """Handles microphone input and speech-to-text conversion."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise once at initialization
        with self.microphone as source:
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
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
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            # Timeout - no speech detected
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
