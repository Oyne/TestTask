import random
import string
import user

def generate_random_string(length=10):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_user():
    user_instance = user.user()
    user_instance.login = generate_random_string(5)
    user_instance.email = generate_random_string(5) + "@gmail.com"
    user_instance.password = generate_random_string(15)
    return user_instance

def convert_user_to_json(user_instance):
    return {
        "user": {
            "login": user_instance.login,
            "email": user_instance.email,
            "password": user_instance.password
        }
    }