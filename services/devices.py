from repositories.devices import DeviceRepository
from schemas.devices import DeviceCreate, DeviceUpdate, Led, ClockLamp, ClockTime, Alarm, Security
from utils.jwt_worker import decode_data
import requests


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    def create_device(self, device: DeviceCreate, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
        if user_id is None:
            return False, 0
        user_id = user_id[0]
        try:
            response = requests.get(f"http://{device.ip}/ping")
            if response.status_code != 200 and device.type != "security":
                return False, "Wrong IP address"
        except Exception:
            return False, "Wrong IP address"
        self.repository.create_device(device, user_id)
        device_id = self.repository.get_last_id()
        return True, device_id

    def get_user_devices(self, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
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

    def delete_device(self, device_id: int, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
        if user_id is None:
            return False
        self.repository.delete_device(device_id)
        return True

    def update_device(self, device: DeviceUpdate, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
        if user_id is None:
            return False
        self.repository.update_device(device)
        return True

    def manage_led(self, led: Led, token):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        ip = self.repository.get_ip(led.id)
        if ip is None:
            return False, "Not found device"
        print(ip)
        try:
            response = requests.post(f"http://{ip}/manage", json={"state": led.state, "color": led.color})
            if response.status_code != 200:
                return False, "Something went wrong"
        except Exception:
            return False, "Something went wrong"
        self.repository.manage_led(led)
        return True, "OK"

    def manage_clock_lamp(self, lamp: ClockLamp, token):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        ip = self.repository.get_ip(lamp.id)
        if ip is None:
            return False, "Not found device"
        try:
            response = requests.post(f"http://{ip}/manage", json={"state": lamp.state})
            if response.status_code != 200:
                return False, "Something went wrong"
        except Exception:
            return False, "Something went wrong"
        self.repository.manage_clock_lamp(lamp.id, lamp.state)
        return True, "OK"

    def manage_clock_time(self, alarm: ClockTime, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        ip = self.repository.get_ip(alarm.id)
        if ip is None:
            return False, "Not found device"
        try:
            response = requests.post(f"http://{ip}/manage", json={"time": alarm.time})
            if response.status_code != 200:
                return False, "Something went wrong"
        except Exception:
            return False, "Something went wrong"
        self.repository.manage_clock_time(alarm.id, alarm.time)
        return True, "OK"

    def manage_alarm(self, alarm: Alarm, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        ip = self.repository.get_ip(alarm.id)
        if ip is None:
            return False, "Not found device"
        try:
            response = requests.post(f"http://{ip}/manage", json={"state": alarm.state, "time": alarm.time})
            if response.status_code != 200:
                return False, "Something went wrong"
        except Exception:
            return False, "Something went wrong"
        self.repository.manage_alarm(alarm.id, alarm.state, alarm.time)
        return True, "OK"

    def manage_security(self, device: Security, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, "Invalid credentials"
        ip = self.repository.get_ip(device.id)
        if ip is None:
            return False, "Not found device"
        self.repository.manage_security(device.id, device.state)
        return True, "OK"
