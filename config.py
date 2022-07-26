import os

token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
main_url = f'https://api.telegram.org/bot{token}'
#host = "127.0.0.1"
#user = "review"
#passwd = 'mypass'
#database = "reviews"
#passwd = os.getenv('MYSQLPASS')
db_config = {
    "mysql": {
    "host": "127.0.0.1",
    "user": "review",
    "passwd": os.getenv('MYSQLPASS'),
    "database": "reviews",
    }
}
