import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):

        self.Database = Database("testing_db")
        self.db = self.Database.db

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertTrue(len(tables) == 2)
        self.assertEquals(sorted(tables), ['Answer', 'Question'])
        cols_ans = self.db.get_columns('Answer')
        cols_qs = self.db.get_columns('Question')

        self.assertTrue(len(cols_ans) == 4)
        self.assertTrue(len(cols_qs) == 3)

    def tearDown(self):
        self.db.drop_tables([self.Database.Answer, self.Database.Question], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
