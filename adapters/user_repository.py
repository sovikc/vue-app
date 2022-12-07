import os
import psycopg
import logging
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from vue import repository, user
from identity import gen

logger = logging.getLogger('entrypoint.api.usr')


class UniqueEmail(Exception):
    pass


class UserRepository(repository.AbstractUserRepository):

    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def create_user_account(self, person: user.User) -> str:
        conn = self.pool.getconn()
        tx = conn.transaction()
        tx.isolation_level = psycopg.IsolationLevel(2)
        cur = conn.cursor()
        try:
            random_uuid = gen.get_uuid()
            cur.execute(
                "INSERT INTO user_account(account_uuid, full_name, email, pass) VALUES (%s, %s, %s, %s)",
                (random_uuid,
                 person.name,
                 person.email,
                 person.password))
            conn.commit()
        except (Exception) as err:
            logger.error(err)
            conn.rollback()
            raise err
        finally:
            self.pool.putconn(conn)
        return random_uuid

    def create_file_store(self, user_account_id: str):
        # TODO do the following in Block Store instead of local directory
        try:
            os.mkdir("./" + user_account_id)
        except Exception as err:
            logger.error("Error creating directory for " + user_id, err)
            raise err

    def get_user_by_email(
            self,
            email: str,
            with_password: bool = False) -> user.User:
        conn = self.pool.getconn()
        cur = conn.cursor()
        existing_user = None
        try:
            if with_password:
                cur.execute(
                    "SELECT account_uuid, full_name, pass FROM user_account WHERE email = %s",
                    (email,
                     ))
            else:
                cur.execute(
                    "SELECT account_uuid, full_name FROM user_account WHERE email = %s", (email,))

            user_records = []
            for record in cur:
                user_records.append(record)

            if len(user_records) > 0:
                user_record = user_records[0]
                identifier = user_record[0]
                name = user_record[1]

                existing_user = user.User()
                existing_user.identifier = identifier
                existing_user.email = email
                existing_user.name = name
                if with_password:
                    existing_user.password = user_record[2]

            if len(user_records) > 1:
                # create a data violation notification
                logger.error("Data Corruption")

        except (Exception) as err:
            logger.error(err)
            raise Exception
        finally:
            self.pool.putconn(conn)

        return existing_user

    def get_user_by_id(self, user_uuid: str) -> user.User:
        conn = self.pool.getconn()
        cur = conn.cursor(row_factory=dict_row)
        existing_user = None
        try:
            user_record = cur.execute(
                "SELECT email, full_name FROM user_account WHERE account_uuid = %s",
                (user_uuid,
                 )).fetchone()
        except (Exception) as err:
            logger.error(err)
            raise Exception
        finally:
            self.pool.putconn(conn)

        if "email" not in user_record:
            return existing_user

        existing_user = user.User()
        existing_user.identifier = user_uuid
        existing_user.email = user_record["email"]
        existing_user.name = user_record["full_name"]

        return existing_user
