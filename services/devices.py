from repositories.devices import DeviceRepository
from schemas.devices import DeviceCreate
from schemas.users import UserValidate


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    def create_device(self, device: DeviceCreate):
        user = UserValidate(e_mail=device.e_mail, hash_password=device.hash_password)
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return False, 0
        user_id = user_id[0]
        self.repository.create_device(device, user_id)
        device_id = self.repository.get_last_id()
        return True, device_id
