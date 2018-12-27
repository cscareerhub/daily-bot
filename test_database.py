import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.Database = Database("testing_db")
        self.db = self.Database.db
        self.Database.start_connection()

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertEqual(sorted(tables), ['answer', 'question'])
        cols_ans = self.db.get_columns('answer')
        cols_qs = self.db.get_columns('question')

        self.assertTrue(len(cols_ans) == 4)
        self.assertTrue(len(cols_qs) == 3)

    def test_adding_questions(self):
        self.Database.add_new_question("How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.assertEqual(self.Database.Question.select().count(), 1)
        self.Database.add_new_question("What is the meaning of life?")
        self.assertEqual(self.Database.Question.select().count(), 2)
        self.Database.add_new_question("How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.assertEqual(self.Database.Question.select().count(), 2)
        # Testing this post integrity error
        self.Database.add_new_question("What is love?")
        self.assertEqual(self.Database.Question.select().count(), 3)

    def test_question_retrieval(self):
        if self.Database.Question.select().count() < 1:
            self.Database.add_new_question("How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
            
        q1 = self.Database.get_day_question()
        q2 = self.Database.get_day_question()

        self.assertIsNotNone(q1)
        self.assertIsNotNone(q2)

        self.assertEqual(q1, q2)

    def tearDown(self):
        self.db.drop_tables([self.Database.Answer, self.Database.Question], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
