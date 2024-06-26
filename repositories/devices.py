import psycopg2
import json
import logging

from schemas.devices import DeviceCreate, DeviceUpdate, Led


class DeviceRepository:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='database.log')

    @staticmethod
    def connect():
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

    def get_user_id(self, e_mail, hash_password):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "user" WHERE e_mail = %s AND hash_password = %s',
                           (e_mail, hash_password))
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

    def get_user_devices(self, user_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT id, room_id, name, type, state, time, alarm_time, alarm_lamp, ip FROM "device" WHERE user_id = %s ORDER BY id',
                (user_id,))
            data = cursor.fetchall()
        conn.close()
        return data

    def delete_device(self, device_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM "device" WHERE id = %s', (device_id,))
        conn.commit()
        conn.close()

    def update_device(self, device: DeviceUpdate):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET room_id = %s, name = %s, type = %s WHERE id = %s',
                           (device.room_id, device.name, device.type, device.id))
        conn.commit()
        conn.close()

    def get_ip(self, device_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT ip FROM "device" WHERE id = %s', (device_id,))
            ip = cursor.fetchone()
        conn.close()
        if ip is not None:
            ip = ip[0]
        return ip

    def manage_led(self, led: Led):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET state = %s WHERE id = %s', (led.state, led.id))
        conn.commit()
        conn.close()

    def manage_clock_lamp(self, device_id: int, state: bool):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET alarm_lamp = %s WHERE id = %s', (state, device_id))
        conn.commit()
        conn.close()

    def manage_clock_time(self, device_id: int, time: str):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET time = %s WHERE id = %s', (time, device_id))
        conn.commit()
        conn.close()

    def manage_alarm(self, device_id: int, state: bool, time: str):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET state = %s, alarm_time = %s WHERE id = %s', (state, time, device_id))
        conn.commit()
        conn.close()

    def manage_security(self, device_id: int, state: bool):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "device" SET state = %s WHERE id = %s', (state, device_id))
        conn.commit()
        conn.close()
