import peewee
import datetime


class Database:
    def __init__(self, db_name, uname="test", pwd="test", host="localhost"):
        self.db = peewee.PostgresqlDatabase(
            db_name,
            user=uname,
            password=pwd,
            host=host
        )

        # This is taken mostly from the Peewee sample app
        class BaseModel(peewee.Model):
            class Meta:
                database = self.db

        class Question(BaseModel):
            body = peewee.TextField(unique=True)
            last_date = peewee.DateField(null=True)
            company = peewee.TextField()
            data_structure = peewee.TextField()
            leetcode = peewee.CharField(max_length=2083, null=True)

        class Admin(BaseModel):
            user_id = peewee.CharField(max_length=19)

        self.Question = Question
        self.Admin = Admin

    def start_connection(self):
        """
        Start connection to database.
        """
        self.db.connect()
        self.db.create_tables([self.Question, self.Admin])
        self.db.commit()

    def end_connection(self):
        """
        close connection to database.
        """
        self.db.close()

    def add_new_question(self, company, text, structure):
        """
        Adds a new question to the database.

        :param text: The body of the text that will appear.
        :param company: Company  that asked this question.
        :param structure: The key data structure used for this question.

        :return: amount of rows altered.
        """
        try:
            q = self.Question(body=text, data_structure=structure, company=company)
            return q.save()
        except peewee.IntegrityError:
            self.db.rollback()
            return 0

    def get_day_question(self):
        """
        Get the question for the day.

        Retrieves the question that should be asked on the day.
        Goes in order of: question that has today's date, has no date attached, date furthest from today.

        :return: Question for the day (none if nothing found)
        """
        q = self.Question.get_or_none(self.Question.last_date == datetime.datetime.now().date())

        if q is None:
            q = self.Question.get_or_none(self.Question.last_date.is_null())

        # TODO: also do another is none check and add the furthest date from today. This should cover all bases
        q.last_date = datetime.datetime.now().date()
        q.save()

        if q.leetcode is not None:
            return q.id, q.company, q.body, q.leetcode
        else:
            return q.id, q.company, q.body

    def get_index_question(self, index):
        """
        Gets the question based on a provided index.

        :param index: Index of question that is to be found (look at list_questions)
        :return: list containing index, body and asking company
        """
        target = self.Question.get_or_none(self.Question.id == index)

        if target is None:
            return None

        return target.id, target.company, target.body

    def list_questions(self, first_index=0):
        """
        Lists questions.

        Lists 10 questions sorted by insertion order into database.
        By providing an integer, you retrieve 10 values starting from that index.
        Note: index starts at 1.

        :param first_index: The first index to start at
        :return: a string that represents set block of questions
        """
        count = 0
        string = "{:>3} | {:10} | {}\n".format("ID", "Last Asked", "Company")
        for row in self.Question.select().dicts():
            if count >= 10:
                break

            if row["id"] >= first_index:
                body = row["last_date"]

                if body is not None:
                    body = body.strftime('%d/%m/%Y')
                else:
                    body = "Never"

                string += "{:>3} | {:10} | {}\n".format(row["id"], body, row["company"])
                count += 1

        return string

    def remove_question(self, index):
        """
        Remove a question by providing its index.

        Removes a question by providing its index (found by listing questions).

        :param index: Index of question to remove
        :return: None if question was not found, otherwise string body of set question
        """
        target = self.Question.get_or_none(self.Question.id == index)

        if target is None:
            return None

        string = target.body
        target.delete_instance()
        return string
