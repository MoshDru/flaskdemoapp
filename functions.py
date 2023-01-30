import pymysql
import os
from dotenv import load_dotenv
from pymysql.constants import CLIENT

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def connect_db(db_name, dictionary=False):
    cc = pymysql.connect(
        host=os.environ.get('MYSQL_SERVER'),
        user=os.environ.get('MYSQL_USER'),
        passwd=os.environ.get('MYSQL_PASSWORD'),
        database=db_name,
        charset='utf8mb4',
        use_unicode=True,
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    if dictionary == True:
        cursor = cc.cursor(pymysql.cursors.DictCursor)
    else:
        cursor = cc.cursor()

    return (cc, cursor)
