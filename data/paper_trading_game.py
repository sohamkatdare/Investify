from data.firebase_controller import create_game, get_all_games, get_game_detail # get_game, get_owner, update_game, delete_game

# Create a multiplayer game where players can trade stocks and compete for the highest portfolio value using the PaperTrader module
class PaperTraderGame:
    def __init__(self, name, starting_amount, owner, players=[]):
        self.name = name
        self.starting_amount = starting_amount
        self.owner = owner
        self.players = players

    def create_game(self):
        print("Creating game...")
        create_game(self.to_dict())

    def update_game(self):
        pass
    
    def end_game(self):
        pass

    @staticmethod
    def get_games(user):
        return get_all_games(user)
    
    @staticmethod
    def get_game_detail(game, user):
        return get_game_detail(game, user)

    def to_dict(self):
        return {
            'players': self.players,
            'name': self.name,
            'starting_amount': self.starting_amount,
            'owner': self.owner
        }
    
