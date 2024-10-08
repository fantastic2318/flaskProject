DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = "root"
PASSWORD = "root"
HOST = '119.3.223.250'
PORT = '33060'
DATABASE = 'fantasy'  # 这里是数据库文件名
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                                                       HOST, PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True