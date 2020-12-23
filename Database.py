import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from datetime import datetime
import os


# TODO: check that the queries and database stuff works
# TODO: function descriptors
class DatabaseWrapper:
    conn = None

    def close(self):
        print("Closing database...")

        self.cursor.close()
        self.conn.close()

        print("Successfully closed connection to database!")

    def newUser(self, username: str, passwd: str):
        query = "INSERT INTO users (username, password) VALUES ( %s, crypt(%s, gen_salt('bf')) )"
        data = (username, passwd)

        self.cursor.execute(query, data)
        self.conn.commit()

    def checkUser(self, username: str, passwd: str):
        query = "SELECT (password=crypt(%s, password)) AS pwd_match from users where username = %s"
        data = (passwd, username)

        self.cursor.execute(query, data)

        res = self.cursor.fetchone()

        if res is None:
            return False
        else:
            return res[0]

    def userExists(self, username: str):
        query = "SELECT username from users where username = %s"
        data = (username,)

        self.cursor.execute(query, data)

        res = self.cursor.fetchone()

        if res is None:
            return False
        else:
            return len(res) > 0

    def verifyAdmin(self, key: str):
        query = "SELECT (password=crypt(%s, password)) AS pwd_match from users where username = 'admin_key'"
        data = (key,)

        self.cursor.execute(query, data)
        return self.cursor.fetchone()[0]

    def __init__(self, dbName: str, passwd: str):
        try:
            # Establishing the connection
            self.conn = psycopg2.connect(
                database=dbName, user='postgres', password=passwd, host='localhost', port='5432'
            )

            # TODO: Check if all the required tables are present
            print("Successfully connected to database %s" % dbName)

            # Creating a cursor object
            self.cursor = self.conn.cursor()
        except:
            print("Database %s does not exist" % dbName)
            ans = input("Do you want to create the database now? ([yes]/no): ")

            if ans == "no":
                sys.exit(1)

            print("Connecting to PostgreSQL...")

            try:
                # Connect to the default database (we need a cursor to create the database, and we need a connection
                # to create a cursor so...)
                conn = psycopg2.connect(user='postgres', password=passwd, host='localhost', port='5432')
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            except Exception as e:
                # Password might be wrong, but I do not want to ask again. Just exit with an error

                print("Something went wrong...")
                print(e)
                sys.exit(1)

            print("Connected!")
            print("Creating database...")

            # Creating a cursor object
            cursor = conn.cursor()

            # Inserting the order to create the database
            cursor.execute("CREATE DATABASE " + dbName + ";")

            # Execute the order
            conn.commit()

            print("Database created successfully!")

            # Close the temporary connection to the default database
            # Notice that these are **local** variables
            cursor.close()
            conn.close()

            print("Connecting to the newly created database...")

            # TODO: error handling (the password might be wrong)
            self.conn = psycopg2.connect(
                database=dbName, user='postgres', password=passwd, host='localhost', port='5432'
            )

            self.cursor = self.conn.cursor()

            print("Importing the pgcrypto to encode passwords...")

            self.cursor.execute('create extension pgcrypto')
            self.conn.commit()

            print("Creating the game binaries' table...")

            # Create the table to store the game binaries' information
            self.cursor.execute('CREATE TABLE game_bin (version VARCHAR(5) PRIMARY KEY, release_date TIMESTAMP, ' +
                                'description VARCHAR(255), file_location VARCHAR(200))')

            # Execute the changes
            self.conn.commit()

            print("Creating users' table...")

            # Create the table to store the data for the users
            self.cursor.execute('create table users (id int generated always as identity(cache 10 ) primary key' +
                                ', username text not null unique, password text not null)')

            # Execute the changes
            self.conn.commit()

            print("Creating admin verification key...")
            admnkey = ""
            while admnkey == "":
                admnkey = input("Admin key: ")

            query = "INSERT INTO users (username, password) VALUES ( 'admin_key', crypt(%s, gen_salt('bf')) )"
            data = (admnkey,)

            self.cursor.execute(query, data)
            self.conn.commit()

            print("Done! Database is ready to use")
