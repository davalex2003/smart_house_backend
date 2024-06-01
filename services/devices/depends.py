from services.devices.repositories.devices import DeviceRepository
from services.devices.services.devices import DeviceService


def get_device_service() -> DeviceService:
    device_repository = DeviceRepository()
    device_service = DeviceService(device_repository)
    return device_service
