import pytest
import requests
import utils
import user

url = "https://favqs.com/api/"
api_key = "" # Replace with your API key

class TestUserAPI:
    # Setup
    @classmethod
    def setup_class(cls):
        cls.user = utils.generate_user()
        cls.headers = {
            'Authorization': f"Token token={api_key}",
            'User-Token': ""
        }

    @pytest.mark.order(1)
    def test_create_new_user(self):
        # Create new user
        response = requests.post(
            url + "users",
            headers=self.headers,
            json=utils.convert_user_to_json(self.user)
        ) 
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, Error: {response.text}"
        
        # Verify created user
        self.headers["User-Token"] = response.json().get("User-Token")
        response = requests.get(
            url + f"users/{self.user.login}", 
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, Error: {response.text}"
        user_data = response.json()
        assert user_data["login"] == self.user.login, f"Expected login {self.user.login}, got {user_data['login']}"
        assert user_data["account_details"]["email"] == self.user.email, f"Expected email {self.user.email}, got {user_data["account_details"]["email"]}"

    @pytest.mark.order(2)
    def test_update_user(self):
        # Setup
        new_login = utils.generate_random_string(5)
        new_email = utils.generate_random_string(5) + "@gmail.com"
        new_user = user.user(login=new_login, email=new_email, password=self.user.password)
        
        # Update user
        response = requests.put(
            url + f"users/{self.user.login}",
            headers=self.headers,
            json=utils.convert_user_to_json(new_user)
        )
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, Error: {response.text}"

        # Verify updated user
        response = requests.get(
            url + f"users/{new_login}", 
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, Error: {response.text}"
        user_data = response.json()
        assert user_data["login"] == new_user.login, f"Expected login {new_user.login}, got {user_data['login']}"
        assert user_data["account_details"]["email"] == new_user.email, f"Expected email {new_user.email}, got {user_data["account_details"]["email"]}"
