import psycopg2
import json
import logging
from typing import List

from schemas.devices import DeviceCreate, DeviceItem
from schemas.users import UserValidate


class DeviceRepository:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='database.log')

    def connect(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            database_params = config['database']
            f.close()
        try:
            conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                                    password=database_params['password'], host=database_params['host'])
        except Exception as e:
            logging.error(e)
            return
        return conn

    def get_user_id(self, user: UserValidate):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "user" WHERE e_mail = %s AND hash_password = %s',
                           (user.e_mail, user.hash_password))
            user_id = cursor.fetchone()
        conn.close()
        return user_id

    def create_device(self, device: DeviceCreate, user_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "device" (user_id, room_id, name, type, ip) VALUES (%s, %s, %s, %s, %s)',
                           (user_id, device.room_id, device.name, device.type, device.ip))
            conn.commit()
            conn.close()

    def get_last_id(self):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "device" ORDER BY id DESC LIMIT 1')
            last_id = cursor.fetchone()
        conn.close()
        return last_id[0]
