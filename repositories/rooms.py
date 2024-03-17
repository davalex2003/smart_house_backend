import psycopg2
import json
import logging

from schemas.rooms import RoomDTO, RoomItem
from schemas.users import UserValidate


class RoomRepository:
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

    def create_room(self, room: RoomDTO):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "room" (name, user_id) VALUES (%s, %s)', (room.name, room.user_id))
        conn.commit()
        conn.close()

    def get_user_rooms(self, user_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, name FROM "room" WHERE user_id = %s', (user_id,))
            data = cursor.fetchall()
        conn.close()
        return data

    def delete_room(self, room_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM "room" WHERE id = %s', (room_id,))
            conn.commit()
        conn.close()

    def update_room(self, room: RoomItem):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "room" SET name = %s WHERE id = %s', (room.name, room.id))
            conn.commit()
        conn.close()

    def get_room_id(self, room_id: int):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "room" WHERE id = %s', (room_id,))
            room_id = cursor.fetchone()
        conn.close()
        return room_id

    def get_last_id(self):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "room" ORDER BY id DESC LIMIT 1')
            last_id = cursor.fetchone()
        conn.close()
        return last_id[0]
