import pyrebase
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firestore DB
cred = credentials.Certificate('investify-d81b6-firebase-adminsdk-nwh3q-8ce381cf50.json')
default_app = initialize_app(cred)
db = firestore.client()

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

auth = pb.auth()

def get_pb():
    return pb

def get_db():
    return db

def get_auth():
    return auth

print('Initialized Pyrebase.')

if __name__ == '__main__':
    db = get_db()
    print(db)

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'cities').document(u'LA').set({
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    })