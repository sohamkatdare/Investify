from data.firebase_init import get_db
from data.firebase_controller import create_user, get_user, reset_password

db = get_db()

class User:
    """
    User Data Model. Stores ChatGPT conversation information for each user.
    """

    def __init__(self, user_id):
        """
        Initializes a new User object.
        
        :param user_id: User ID
        """
        self.user_id = user_id
        self.conversation = []

    def add_to_conversation(self, utterance):
        self.conversation.append(utterance)

    def get_last_utterance(self):
        return self.conversation[-1]

    def get_conversation(self):
        return self.conversation

    def clear_conversation(self):
        self.conversation = []

    @staticmethod
    def create_user(email, password):
        """
        Creates a new user in the database.
        
        :param email: Email of the user
        :param password: Password of the user
        :return: User object
        """
        uid = create_user(email, password)
    
    @staticmethod
    def get_user(email, password):
        """
        Login a user and create User Object.
        
        :param email: Email of the user
        :return: User object
        """
        uid = get_user(email, password)
        return User(uid)
    
    @staticmethod
    def reset_password(email):
        """
        Reset password of a user.
        
        :param email: Email of the user
        :return: User object
        """
        reset_password(email)
    

    