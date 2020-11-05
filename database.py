import peewee
import datetime


class Database:
    def __init__(self, db_name, uname="test", pwd="test", host="localhost", debug=True):
        if debug:
            self.db = peewee.SqliteDatabase("testing.db")
        else:
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
            user_id = peewee.CharField(max_length=19, unique=True)

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
        Close connection to database.
        """
        self.db.close()

    def add_admin(self, user_id):
        """
        Adds an admin to bot users.

        :param user_id: User ID of admin to be added
        :return: 1 if successful, 0 if already in table
        """
        try:
            q = self.Admin(user_id=user_id)
            return q.save()
        except peewee.IntegrityError:
            self.db.rollback()
            return 0

    def remove_admin(self, user_id):
        """
        Removes an admin from bot users.

        :param user_id: User ID of admin to be removed
        :return: ID of user deleted. None if nothing found.
        """
        target = self.Admin.get_or_none(self.Admin.user_id == user_id)

        if target is None:
            return None

        string = target.user_id
        target.delete_instance()
        return string

    def is_admin(self, user_id):
        """
        Returns true if user_id is in admin table

        :param user_id: User ID of player attempting to do command
        :return: True if in table, False otherwise
        """
        return self.Admin.get_or_none(self.Admin.user_id == user_id) is not None

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

    def add_multiple_questions(self, questions):
        """

        :param questions: list of tuple of questions
        :return: nothing
        """
        try:
            self.Question.insert_many(questions, fields=[self.Question.company, self.Question.data_structure,
                                                         self.Question.body]).execute()
        except peewee.IntegrityError:
            self.db.rollback()

    def modify_question(self, index, body):
        """
        Modifies a question body.

        :param index: index of said question
        :param body: the new body of the question
        :return: true if question found and updated
        """
        try:
            q = self.Question.get_or_none(self.Question.id == index)

            if q is not None:
                q.body = body
                q.save()
                return True
            return False
        except peewee.IntegrityError:
            self.db.rollback()

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

            if q is None:
                q = self.__get_random_helper()

        q.last_date = datetime.datetime.now().date()
        q.save()

        if q.leetcode is not None:
            return q.id, q.company, q.body, q.leetcode
        else:
            return q.id, q.company, q.body

    def get_random_question(self, company=None):
        """
        Returns a random question from the database.

        :param company: (Optional) Limit random question to one asked by given company 
        :return: randomly chosen question
        """
        q = self.__get_random_helper(company)

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

    def get_company_list(self):
        companies = self.Question.select(self.Question.company, peewee.fn.COUNT(self.Question.body).alias('count')) \
            .group_by(self.Question.company).order_by(self.Question.company.asc())
        return companies

    def list_questions(self, first_index=0, company=None):
        """
        Lists questions.

        Lists 5 questions sorted by insertion order into database.
        By providing an integer, you retrieve 5 values starting from that index.
        Note: index starts at 1.

        :param first_index: The first index to start at
        :param company: The company which is to be filtered for
        :return: a string that represents set block of questions
        """
        string = "{:>3} | {:10} | {}\n".format("ID", "Last Asked", "Company")
        if company is None:
            query = self.Question.select().where(self.Question.id > first_index).order_by(self.Question.id).limit(5).dicts()
        else:
            query = self.Question.select().where((self.Question.id > first_index) & (self.Question.company == company)) \
                .order_by(self.Question.id).limit(5).dicts()
        for row in query:
            body = row["last_date"]

            if body is not None:
                body = body.strftime('%d/%m/%Y')
            else:
                body = "Never"

            string += "{:>3} | {:10} | {}\n".format(row["id"], body, row["company"])

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

    def __get_random_helper(self, company=None):
        if company is None:
            q = self.Question.select().order_by(peewee.fn.Random()).get()
        else:
            q = self.Question.select().where(self.Question.company == company).order_by(peewee.fn.Random()).get()

        return q