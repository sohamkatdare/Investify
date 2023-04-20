from data.firebase_init import db
from data.firebase_controller import create_user, get_user, reset_password

class User:
    """
    User Data Model. Stores ChatGPT conversation information for each user.
    """

    def __init__(self, user_id, email, user_data={}, games = [], stocks=[]):
        """
        Initializes a new User object.
        
        :param user_id: User ID
        """
        self.user_id = user_id
        self.email = email
        self.user_data = user_data
        self.conversation = []
        self.games = games
        self.stocks = stocks

    def add_to_conversation(self, utterance):
        self.conversation.append(utterance)

    def get_last_utterance(self):
        return self.conversation[-1]

    def get_conversation(self):
        return self.conversation

    def clear_conversation(self):
        self.conversation = []

    def add_game(self, game):
        self.games.append(game)
    
    def get_games(self):
        return self.games
    
    def add_stock(self, stock):
        self.stocks.append(stock)

    def get_stocks(self):
        return self.stocks
    
    def delete_stock(self, stock):
        return self.stocks.remove(stock)

    @staticmethod
    def create_user(email, password):
        """
        Creates a new user in the database.
        
        :param email: Email of the user
        :param password: Password of the user
        :return: User object
        """
        create_user(email, password)

    
    @staticmethod
    def get_user(email, password):
        """
        Login a user and create User Object.
        
        :param email: Email of the user
        :return: User object
        """
        user, user_data = get_user(email, password)
        print(user_data)
        return User(user['idToken'], email, user_data=user, games=user_data['games'])
    
    @staticmethod
    def reset_password(email):
        """
        Reset password of a user.
        
        :param email: Email of the user
        :return: User object
        """
        reset_password(email)

    @staticmethod
    def get_user_by_email(email):
        """
        Get a user by email.
        
        :param email: Email of the user
        :return: User object
        """
        user_data = db.collection(u'users').document(email).get().to_dict()
        return User(user_data['user_id'], email, user_data=user_data)
    
    
    def to_dict(self):
        """
        Converts User object to a dictionary.
        
        :return: Dictionary of User object
        """
        return {
            'user_id': self.user_id,
            'email': self.email,
            'conversation': self.conversation,
            'games': self.games
        }