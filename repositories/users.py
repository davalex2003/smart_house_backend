import psycopg2
import json
import logging

from schemas.users import User, UserValidate, UserUpdate


class UserRepository:
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

    def create_user(self, user: User):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "user" (name, surname, e_mail, hash_password) '
                           'VALUES (%s, %s, %s, %s)', (user.name, user.surname, user.e_mail, user.hash_password))
        conn.commit()
        conn.close()

    def validate_user(self, user: UserValidate) -> bool:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "user" WHERE e_mail = %s AND hash_password = %s',
                           (user.e_mail, user.hash_password))
            data = cursor.fetchall()
        conn.close()
        if len(data) == 0:
            return False
        else:
            return True

    def validate_email(self, e_mail: str) -> bool:
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "user" WHERE e_mail = %s', (e_mail,))
            data = cursor.fetchall()
        conn.close()
        if len(data) == 1:
            return True
        else:
            return False

    def delete_user(self, e_mail: str):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM "user" WHERE e_mail = %s', (e_mail,))
        conn.commit()
        conn.close()

    def update_user(self, user: UserUpdate, e_mail: str):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('UPDATE "user" SET name = %s, surname = %s WHERE e_mail = %s',
                           (user.name, user.surname, e_mail))
        conn.commit()
        conn.close()

    def get_user_name_and_surname(self, e_mail, hash_password):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute('SELECT name, surname FROM "user" WHERE e_mail = %s AND hash_password = %s',
                           (e_mail, hash_password))
            data = cursor.fetchone()
        conn.close()
        return data
