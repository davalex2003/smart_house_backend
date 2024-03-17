import psycopg2
import json
import logging

from schemas.rooms import RoomDTO
from schemas.users import UserValidate


class RoomRepository:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='database.log')

    def get_user_id(self, user: UserValidate):
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
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM "user" WHERE e_mail = %s AND hash_password = %s',
                           (user.e_mail, user.hash_password))
            user_id = cursor.fetchone()
        return user_id

    def create_room(self, room: RoomDTO):
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
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "room" (name, user_id) VALUES (%s, %s)', (room.name, room.user_id))
        conn.commit()

    def get_user_rooms(self, user_id: int):
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
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, name FROM "room" WHERE user_id = %s', (user_id,))
            return cursor.fetchall()
