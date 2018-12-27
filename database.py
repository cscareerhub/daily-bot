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
            body = peewee.TextField(unique=True)
            last_date = peewee.DateField()

        class Answer(BaseModel):
            uname = peewee.TextField()  # TODO: probably not the best format to save id
            url = peewee.CharField(max_length=2083)
            question = peewee.ForeignKeyField(Question)

        self.Question = Question
        self.Answer = Answer

    def start_connection(self):
        """
        Start connection to database.
        """
        self.db.connect()
        self.db.create_tables([self.Question, self.Answer])
        self.db.commit()

    def end_connection(self):
        """
        close connection to database.
        """
        self.db.close()

    def add_new_question(self, text):
        """
        Adds a new question to the database.

        :param text: The body of the text that will appear.

        :return: amount of rows altered.
        """
        q = self.Question(body=text)
        return q.save()

    # TODO: cache the people for the day. At the moment this will be messier by constantly checking the DB
    # TODO: untested
    def add_new_answer(self, ans_url, qIndex, uname):
        """
        Add a new answer to a question.

        :param ans_url: URL that references the answer
        :param qIndex: ID (or index) of the question being answered
        :param uname: The author ID of the person answering

        :return: amount of rows altered
        """
        ans = self.Answer.get_or_create(question=qIndex, uname=uname, defaults={'url': ans_url})
        return ans.save()
