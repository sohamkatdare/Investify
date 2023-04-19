from data.firebase_controller import create_game # get_game, get_owner, update_game, delete_game

# Create a multiplayer game where players can trade stocks and compete for the highest portfolio value using the PaperTrader module
class PaperTraderGame:
    def __init__(self, players=[], name, starting_amount, owner):
        self.players = players
        self.name = name
        self.starting_amount = starting_amount
        self.owner = owner

    def update_game(self):
        pass
    
    def end_game(self):
        pass

    def to_dict(self):
        return {
            'players': self.players,
            'name': self.name,
            'starting_amount': self.starting_amount,
            'owner': self.owner
        }
    
