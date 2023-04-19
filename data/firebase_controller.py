from data.firebase_init import get_db, get_auth

db = get_db()
auth = get_auth()

def create_user(email, password):
    uid = auth.create_user_with_email_and_password(email, password)
    from data.user import User
    user = User(uid['idToken'], email, {})
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'users').document(email).set(user.to_dict())
    print(f'Sucessfully created new user.')

def get_user(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    uid = user['idToken']
    print(f'Successfully fetched user data: {uid}')
    print(user)
    # csrf_token = user['csrfToken']
    if not user['registered']:
        print(f'Email not verified. Sending verification email.')
        auth.send_email_verification(uid)
    # Get user data from database
    user_data = db.collection(u'users').document(email).get().to_dict()
    print('user_data: ', user_data)
    return user, user_data

def reset_password(email):
    auth.send_password_reset_email(email)
    print(f'Successfully sent password reset email.')

def create_game(game):
    db.child('games').push(game)
    print(f'Successfully created new game: {game}')

def get_portfolio(user, game):
    paper_trader = db.child('games').child(user).child(game).get()


def check_for_existing_game(game):
    pass

if __name__ == '__main__':
    # add_data()
    # get_data()

    get_user('saptak.das625@gmail.com', 'password')
    