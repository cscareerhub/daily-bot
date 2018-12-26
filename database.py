import peewee


class Database:
    def __init__(self, db_name, uname="test", pwd="test"):
        self.db = peewee.PostgresqlDatabase(
            db_name,
            user=uname,
            password=pwd,
            host='localhost'
        )

        # This is taken mostly from the Peewee sample app
        class BaseModel(peewee.Model):
            class Meta:
                database = self.db

        class Question(BaseModel):
            body = peewee.TextField()
            last_date = peewee.DateField()

        class Answer(BaseModel):
            uname = peewee.TextField()  # TODO: probably not the best format to save id
            url = peewee.CharField(max_length=2083)
            question = peewee.ForeignKeyField(Question)

        self.Question = Question
        self.Answer = Answer

    def start_connection(self):
        self.db.connect()
        self.db.create_tables([self.Question, self.Answer])
        self.db.commit()

    def end_connection(self):
        self.db.close()
