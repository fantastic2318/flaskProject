from Config.mysqlConfig import db


class CatModel(db.Model):
    __tablename__ = 'cat'

    id = db.Column(db.Integer, primary_key=True)
    # init_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __repr__(self):  # 自定义 交互模式 & print() 的对象打印
        return "(%s, %s, %s)" % (self.id, self.name, self.age)

    # @property
    # def __dict__(self):
    #     return {'id': self.id, 'name': self.name, 'age': self.age}

