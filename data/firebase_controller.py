from data.firebase_init import get_db, get_auth

db = get_db()
auth = get_auth()

# def add_data():
#     doc_ref = db.collection(u'users').document(u'alovelace')
#     doc_ref.set({
#         u'first': u'Ada',
#         u'last': u'Lovelace',
#         u'born': 1815
#     })

#     doc_ref = db.collection(u'users').document(u'aturing')
#     doc_ref.set({
#         u'first': u'Alan',
#         u'middle': u'Mathison',
#         u'last': u'Turing',
#         u'born': 1912
#     })

# def get_data():
#     users_ref = db.collection(u'users')
#     docs = users_ref.stream()

#     for doc in docs:
#         print(f'{doc.id} => {doc.to_dict()}')


def create_user(email, password):
    auth.create_user_with_email_and_password(email, password)
    print(f'Sucessfully created new user.')

def get_user(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    uid = user['idToken']
    print(f'Successfully fetched user data: {uid}')
    print(user)
    if not user['registered']:
        print(f'Email not verified. Sending verification email.')
        auth.send_email_verification(uid)
    return user

def reset_password(email):
    auth.send_password_reset_email(email)
    print(f'Successfully sent password reset email.')

if __name__ == '__main__':
    # add_data()
    # get_data()

    get_user('saptak.das625@gmail.com', 'password')
    