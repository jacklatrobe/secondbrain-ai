# manager.py - The Manager component of the SecondBrain application.

from langchain import OpenAI
import logging
from researcher import Researcher

class Manager:
    def __init__(self):
        # Create an object to record the conversation
        self.conversation = []

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
            You are an AI called {name}. You are having a conversation with another AI. The topic or goal is: {topic}
            
            Chat History:
            {history}
            
            Provide a response to the other AI that responds to them and poses challenges or follow-up questions that further explore the topic or goal:
            """.format(name=self.agent_one.name, topic=topic, history=self.create_chat_history(5))
            response1 = self.agent_one.run(prompt)
            self.record_message(message=response1, type=self.agent_one.name)

            # Ask Actor 2 for another response and record it
            prompt = """
            You are an AI called {name}. You are having a conversation with another AI. The topic or goal is: {topic}
            
            Chat History:
            {history}
            
            Provide a response to the other AI that responds to them and poses challenges or follow-up questions that further explore the topic or goal:
            """.format(name=self.agent_two.name, topic=topic, history=self.create_chat_history(5))
            response2 = self.agent_two.run(prompt)
            self.record_message(message=response2, type=self.agent_two.name)

            if self.conversation_concluded():
                conversation_continue = False
                self.record_message(message="Conversation ended.")
            else:
                response = response2
        
        finale = "Save a summary of our conversation to Confluence which includes this chat history:\n{history}".format(history=self.create_chat_history(5))
        response = self.agent_one.run(finale)
        self.record_message(message=response, type=self.agent_one.name)