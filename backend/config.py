def getConfig():
    conf = {}

    # mysql_config = {
    #     'MYSQL_HOST': 'localhost',
    #     'MYSQL_USER': 'root',
    #     'MYSQL_PASSWORD': 'jujuba',
    #     'MYSQL_DB': 'teste',
    #     'MYSQL_CURSORCLASS': 'DictCursor'
    # }

    conf['SQLALCHEMY_DATABASE_URI'] = "postgresql://bgjgjiovkcimjb:f0510d8035f2429bcd69d5d7aedaa75a683007214fa17ca5567124773d7d9296@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d49snvtcgnmkbd"
    conf['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        
    conf['SECRET_KEY'] = 'secret123'
    conf['SESSION_TYPE'] = 'filesystem'

    return conf


CONFIG = getConfig()