import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDKBXoncvcNoKu0eEpD_SnKom_S5nE16vE",
    "authDomain": "investify-d81b6.firebaseapp.com",
    "projectId": "investify-d81b6",
    "databaseURL": "https://investify-d81b6-default-rtdb.firebaseio.com/",
    "storageBucket": "investify-d81b6.appspot.com",
    "messagingSenderId": "54354486522",
    "appId": "1:54354486522:web:4e9afeeb91b1fa24a8d543",
    "measurementId": "G-VJGXTY6JC5"
}

pb = pyrebase.initialize_app(firebaseConfig)

db = pb.database()

auth = pb.auth()

def get_pb():
    return pb

def get_db():
    return db

def get_auth():
    return auth

print('Initialized Pyrebase.')