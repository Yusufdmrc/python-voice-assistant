"""
Command parsing and execution module.
"""

import webbrowser
from datetime import datetime
import random


class CommandHandler:
    """Handles command parsing and execution."""
    
    def __init__(self):
        self.conversation_context = {
            "last_topic": None,
            "interaction_count": 0,
            "waiting_for_youtube_query": False
        }
    
    def process_command(self, command_text):
        """
        Process command and return response.
        
        Args:
            command_text: The command text to process
            
        Returns:
            str: Response text
        """
        if command_text is None:
            return "I didn't catch that. Please try again."
        
        command = command_text.lower().strip()
        
        # Check if we're waiting for YouTube search query
        if self.conversation_context["waiting_for_youtube_query"]:
            self.conversation_context["waiting_for_youtube_query"] = False
            return self._search_youtube_direct(command)
        
        # Exit commands
        if "exit" in command or "quit" in command or "stop" in command:
            return "EXIT"
        
        # Time command
        if "time" in command:
            return self._get_time()
        
        # Date command
        if "date" in command:
            return self._get_date()
        
        # Open Google
        if "open google" in command:
            return self._open_google()
        
        # YouTube search
        if "search on youtube" in command or "youtube" in command:
            return self._search_youtube(command)
        
        # Hello/Hi
        if "hello" in command or "hi" in command:
            return "Hello! How can I help you?"
        
        # How are you
        if "how are you" in command or "nasılsın" in command:
            return self._how_are_you()
        
        # Weather
        if "weather" in command or "hava" in command or "hava nasıl" in command:
            return self._get_weather()
        
        # What's your name
        if "your name" in command or "who are you" in command or "adın ne" in command:
            return "I'm your voice assistant. You can call me Assistant."
        
        # Thank you
        if "thank" in command or "thanks" in command or "teşekkür" in command:
            return "You're welcome! Happy to help."
        
        # Good morning/evening
        if "good morning" in command or "günaydın" in command:
            return "Good morning! Hope you have a great day ahead!"
        
        if "good night" in command or "good evening" in command or "iyi geceler" in command:
            return "Good evening! Have a wonderful evening!"
        
        # Default response
        return "I'm not sure how to help with that. Try asking about time, date, weather, or tell me to open Google."
    
    def _get_time(self):
        """Get current time."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    
    def _get_date(self):
        """Get current date."""
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        return f"Today is {date_str}"
    
    def _open_google(self):
        """Open Google in browser."""
        try:
            webbrowser.open("https://www.google.com")
            return "Opening Google"
        except Exception as e:
            return f"Sorry, I couldn't open Google. Error: {e}"
    
    def _search_youtube(self, command):
        """Search YouTube for keyword."""
        # Extract search term after "youtube" or "search on youtube for"
        search_term = ""
        
        if "search on youtube for" in command:
            search_term = command.split("search on youtube for")[-1].strip()
        elif "youtube for" in command:
            search_term = command.split("youtube for")[-1].strip()
        elif "search youtube" in command:
            search_term = command.split("search youtube")[-1].strip()
        
        if search_term:
            try:
                query = search_term.replace(" ", "+")
                url = f"https://www.youtube.com/results?search_query={query}"
                webbrowser.open(url)
                return f"Searching YouTube for {search_term}"
            except Exception as e:
                return f"Sorry, I couldn't search YouTube. Error: {e}"
        else:
            # Set flag to wait for search query in next turn
            self.conversation_context["waiting_for_youtube_query"] = True
            return "What would you like me to search for on YouTube?"
    
    def _search_youtube_direct(self, query):
        """Search YouTube with direct query."""
        try:
            search_term = query.replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(url)
            return f"Searching YouTube for {query}"
        except Exception as e:
            return f"Sorry, I couldn't search YouTube. Error: {e}"
    
    def _how_are_you(self):
        """Respond to 'how are you' questions."""
        responses = [
            "I'm doing great! Thanks for asking. How are you?",
            "I'm fantastic! Ready to help you with anything you need.",
            "I'm excellent! What can I do for you today?",
            "I'm doing well, thank you! How can I assist you?"
        ]
        self.conversation_context["interaction_count"] += 1
        return random.choice(responses)
    
    def _get_weather(self):
        """Respond to weather questions."""
        # Basit bir yanıt - gerçek hava durumu API'si entegre edilebilir
        now = datetime.now()
        hour = now.hour
        
        if 6 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 18:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"
        
        responses = [
            f"I don't have access to real-time weather data, but I hope it's a beautiful {time_of_day} where you are!",
            f"I can't check the weather right now, but you can ask me to open Google and search for weather.",
            f"I'm not connected to a weather service yet, but I hope the weather is nice this {time_of_day}!"
        ]
        
        return random.choice(responses)
