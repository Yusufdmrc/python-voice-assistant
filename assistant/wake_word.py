"""
Wake word detection module.
"""


class WakeWordDetector:
    """Detects wake words in recognized text."""
    
    def __init__(self, wake_words=None):
        """
        Initialize wake word detector.
        
        Args:
            wake_words: List of wake word phrases (default: ["hey assistant"])
        """
        if wake_words is None:
            wake_words = ["hey assistant", "assistant","hey"]
        
        self.wake_words = [word.lower() for word in wake_words]
    
    def detect(self, text):
        """
        Check if text contains any wake word.
        
        Args:
            text: Text to check (will be converted to lowercase)
            
        Returns:
            bool: True if wake word detected, False otherwise
        """
        if text is None:
            return False
        
        text = text.lower()
        
        for wake_word in self.wake_words:
            if wake_word in text:
                return True
        
        return False
