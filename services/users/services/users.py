from services.users.repositories.users import UserRepository
from schemas.users import User, UserValidate, UserUpdate
from services.devices.utils.jwt_worker import encode_data, decode_data


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User):
        self.repository.create_user(user)
        return encode_data({"e_mail": user.e_mail, "hash_password": user.hash_password})

    def validate_user(self, user: UserValidate) -> bool:
        if self.repository.validate_user(user):
            return encode_data({"e_mail": user.e_mail, "hash_password": user.hash_password})
        else:
            return ''

    def validate_email(self, e_mail: str) -> bool:
        return self.repository.validate_email(e_mail)

    def delete_user(self, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        self.repository.delete_user(data['e_mail'])
        return True

    def update_user(self, user: UserUpdate, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        self.repository.update_user(user, data['e_mail'])
        return True

    def get_user(self, token: str):
        token = decode_data(token)
        data = self.repository.get_user_name_and_surname(token['e_mail'], token['hash_password'])
        if data is None:
            return {}
        else:
            return {
                "name": data[0],
                "surname": data[1]
            }
