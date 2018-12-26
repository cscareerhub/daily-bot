import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):

        self.Database = Database("testing_db")
        self.db = self.Database.db
        self.Database.start_connection()

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertEquals(sorted(tables), ['answer', 'question'])
        cols_ans = self.db.get_columns('answer')
        cols_qs = self.db.get_columns('question')

        self.assertTrue(len(cols_ans) == 4)
        self.assertTrue(len(cols_qs) == 3)

    def tearDown(self):
        self.db.drop_tables([self.Database.Answer, self.Database.Question], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
