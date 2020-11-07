def getConfig():
    conf = {}

    conf['SQLALCHEMY_DATABASE_URI'] = "sql://user:pass@host:port/database"
    conf['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        
    conf['SECRET_KEY'] = 'mySecret'
    conf['SESSION_TYPE'] = 'filesystem'

    return conf


CONFIG = getConfig()