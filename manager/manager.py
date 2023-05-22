# manager.py - The Manager component of the SecondBrain application.

from langchain import OpenAI
import logging
import pyttsx3
from researcher import Researcher

class Manager:
    def __init__(self):
        # Create an object to record the conversation
        self.conversation = []

        # Use TTS? - Currently windows only
        self.use_tts = True

        # How many chat iterations should we do?
        self.max_chats = 10

        # Create first editor object
        self.agent_one = Researcher(name="AgentOne")

        # Create second editor to converse with
        self.agent_two = Researcher(name="AgentTwo")

        # Create a local LLM for adjudication
        self.judge_llm = OpenAI(temperature=0.5)

        # Set up logging
        logging.basicConfig(filename = 'manager.log', level=logging.INFO)
        logging.info("Initialised a manager")

    def record_message(self, message, type = "SystemMessage") -> None:
        msg_id = len(self.conversation) + 1
        self.conversation.append(
            {
                "ID" : msg_id,
                "Type" : type,
                "Message" : message
            }
        )

        logging.info("New message from {agent}: {message}".format(agent=type, message=message))
        print("{agent}: {message}\n".format(agent=type, message=message))
        if self.use_tts:
            # Select a TTS voice
            if type == "AgentOne":
                voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
            else:
                voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
            # Speak the message using local TTS
            engine = pyttsx3.init();
            engine.setProperty('voice', voice_id)
            engine.setProperty('rate', 220)
            engine.say(message, type);
            engine.runAndWait() ;

    def create_chat_history(self, depth):
        # Assemble a history of the last chats
        history = []
        if len(self.conversation) > depth:
            depth = len(self.conversation) - 1
        for log in self.conversation[-depth:]:
            history.append("{agent}: {message}".format(agent=log["Type"], message=log["Message"]))
        history = "\n".join(history)
        return history

    def conversation_concluded(self):
        # Check if we have reached max chats
        if len(self.conversation) > self.max_chats:
            return True
        else:
            return False

    def run(self, request = None):
        # This function receives the initial user request
        if not request:
            topic = input("Suggest an initial topic of conversation: ")
            print("\n")

        # Set up the conversation loop and initial prompt from Actor 1
        conversation_continue = True
        self.record_message(message=topic)

        # Start the conversation
        response = None
        while conversation_continue:
            # Ask Actor 1 for a response and record it
            prompt = """
            You are an AI called {name}. You are having a conversation with AgentTwo. Answer any questions it asks, or ask questions about the topic.
            
            The topic of conversation is: {topic}

            Chat History:
            {history}
            
            What is your question, answer or response to the other AI:
            """.format(name=self.agent_one.name, topic=topic, history=self.create_chat_history(3))
            response1 = self.agent_one.run(prompt)
            self.record_message(message=response1, type=self.agent_one.name)

            # Ask Actor 2 for another response and record it
            prompt = """
            You are an AI called {name}. You are having a conversation with another AI. Ask it creative questions about related topics or new topics that progress the conversation.
            
            Chat History:
            {history}
            
            What is your question, answer or response to the other AI:
            """.format(name=self.agent_two.name, topic=topic, history=self.create_chat_history(5))
            response2 = self.agent_two.run(prompt)
            self.record_message(message=response2, type=self.agent_two.name)

            if self.conversation_concluded():
                conversation_continue = False
                self.record_message(message="Conversation ended.")
            else:
                response = response2
        
        finale = "Save our conversation to Confluence:\n{history}".format(history=self.create_chat_history(7))
        response = self.agent_one.run(finale)
        self.record_message(message=response, type=self.agent_one.name)