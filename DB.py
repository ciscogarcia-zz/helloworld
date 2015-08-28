import psycopg2
from psycopg2.extras import DictCursor

class DB:
    def get_database_connection(self):
        config_file = "db.config"
        username = None
        password = None
        database = None
        host = None

        with open(config_file, "r") as f:
             for line in f:
                 (name, value) = line.split("=")
                 value = value.strip()
                 if name == 'username':
                     username = value
                 elif name == 'password':
                     password = value
                 elif name == 'dbname':
                     database = value
                 elif name == 'dbhost':
                     host = value

        conn = psycopg2.connect(database=database, user=username, password=password, host=host)
        return conn
        
    def get_registered_users(self):
        database_connection = self.get_database_connection()
        select_statement = "select * from user_registration"
        cursor = database_connection.cursor(cursor_factory = DictCursor)
        cursor.execute(select_statement)
        users = cursor.fetchall()
        cursor.close()
        database_connection.close()
        return users

    def insert_registered_user(self, user):
        database_connection = self.get_database_connection()
        insert_statement = "insert into user_registration (fname, lname, address1, address2, city, state, zip, country, registration_date) values (%s, %s, %s, %s, %s, %s, %s, %s, 'now')"

        cursor = database_connection.cursor(cursor_factory = DictCursor)
        cursor.execute(insert_statement, (user['fname'], user['lname'], user['address1'], user['address2'], user['city'], user['state'], user['zip'], user['country']))
        database_connection.commit()
        cursor.close()
        database_connection.close()
        

if __name__ == '__main__':
    db = DB()
    users = db.get_registered_users()
    for user in users:
        print user['fname']

    
