"""
Text-to-speech module.
"""

import subprocess
import platform


class TextToSpeech:
    """Handles text-to-speech conversion."""
    
    def __init__(self):
        self.system = platform.system()
    
    def speak(self, text):
        """
        Convert text to speech.
        
        Args:
            text: Text to speak
        """
        print(f"Assistant: {text}")
        
        try:
            if self.system == "Darwin":  # macOS
                subprocess.run(["say", text], check=True)
            elif self.system == "Windows":
                # Windows için PowerShell ile konuşma
                ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
                subprocess.run(["powershell", "-Command", ps_command], check=True)
            else:  # Linux
                # espeak veya festival kullanabilir
                subprocess.run(["espeak", text], check=True)
        except FileNotFoundError:
            print("(TTS not available - text output only)")
        except Exception as e:
            print(f"(TTS error: {e})")
