"""
Voice Assistant with Wake Word Detection
Main application entry point
"""

from assistant.listener import Listener
from assistant.wake_word import WakeWordDetector
from assistant.commands import CommandHandler
from assistant.tts import TextToSpeech


def main():
    """Main application loop."""
    
    print("=" * 60)
    print("Voice Assistant with Wake Word Detection")
    print("=" * 60)
    print("\nInitializing...")
    
    # Initialize components
    listener = Listener()
    wake_word_detector = WakeWordDetector()
    command_handler = CommandHandler()
    tts = TextToSpeech()
    
    tts.speak("Voice assistant initialized. Say the wake word to activate me.")
    print("\n" + "=" * 60)
    print("Wake words: 'hey assistant', 'assistant'")
    print("Say 'exit' or 'quit' to stop the assistant")
    print("=" * 60 + "\n")
    
    # Main loop
    should_exit = False
    while True:
        try:
            # Listen for wake word
            print("\n[Waiting for wake word...]")
            text = listener.listen(timeout=10)
            
            if text is None:
                continue
            
            # Check for wake word
            if wake_word_detector.detect(text):
                tts.speak("Yes? How can I help you?")
                
                # Conversation loop - continue listening until user is done
                while True:
                    # Listen for command
                    command_text = listener.listen(timeout=5, phrase_time_limit=10)
                    
                    if command_text is None:
                        tts.speak("I didn't hear anything. Say something or say 'done' to finish.")
                        continue
                    
                    # Check if user wants to end conversation
                    if any(word in command_text.lower() for word in ["done", "that's all", "thanks", "thank you", "finished"]):
                        tts.speak("Alright! Let me know if you need anything else.")
                        break
                    
                    # Process command
                    response = command_handler.process_command(command_text)
                    
                    # Check for exit command
                    if response == "EXIT":
                        tts.speak("Goodbye!")
                        print("\nShutting down...")
                        should_exit = True
                        break
                    
                    # Speak response
                    tts.speak(response)
                    
                    # Check if response is a question (needs follow-up)
                    if "?" in response:
                        # Continue listening for answer
                        continue
                    else:
                        # Ask if user needs more help
                        tts.speak("Anything else?")
                        continue
            
            # Break out of main loop if exit was requested
            if should_exit:
                break
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            tts.speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            continue
    
    print("Voice assistant stopped.")


if __name__ == "__main__":
    main()
