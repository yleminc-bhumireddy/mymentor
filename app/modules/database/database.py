import yaml
from mysql.connector import pooling
import mysql.connector
from mysql.connector import errorcode

db_config = yaml.load(open('/Users/swathipotu/PycharmProjects/my-mentor/app/db.yaml'), Loader=yaml.SafeLoader)


connection_pool_name=''


def initialize_database():
    try:
        connection_pool=pooling.MySQLConnectionPool(pool_name="mymentor-db-pool",
                                                      pool_size=1,
                                                      pool_reset_session=True,
                                                      host=db_config['mysql_host'],
                                                      database=db_config['mysql_db'],
                                                      user=db_config['mysql_user'],
                                                      password=db_config['mysql_password'])
        global connection_pool_name
        connection_pool_name=connection_pool.pool_name
        return connection_pool
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)


