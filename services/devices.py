from repositories.devices import DeviceRepository
from schemas.devices import DeviceCreate, DeviceDelete, DeviceUpdate
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

    def get_user_devices(self, user: UserValidate):
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return {}
        data = self.repository.get_user_devices(user_id)
        for i in range(len(data)):
            data[i] = {
                'id': data[i][0],
                'room_id': data[i][1],
                'name': data[i][2],
                'type': data[i][3],
                'state': data[i][4],
                'time': data[i][5],
                'alarm_time': data[i][6],
                'alarm_lamp': data[i][7]
            }
        return data

    def delete_device(self, device: DeviceDelete):
        user = UserValidate(e_mail=device.e_mail, hash_password=device.hash_password)
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return False
        self.repository.delete_device(device.device_id)
        return True

    def update_device(self, device: DeviceUpdate):
        user = UserValidate(e_mail=device.e_mail, hash_password=device.hash_password)
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return False
        self.repository.update_device(device)
        return True
