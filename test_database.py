import unittest
import peewee
import main


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = peewee.PostgresqlDatabase(
            'testing_db',
            user='test',
            password='test',
            host='localhost'
        )

        main.init_db(database=self.db)

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertTrue(len(tables) == 2)
        self.assertEquals(sorted(tables), ['Answer', 'Question'])
        cols_ans = self.db.get_columns('Answer')
        cols_qs = self.db.get_columns('Question')

        self.assertTrue(len(cols_ans) == 4)
        self.assertTrue(len(cols_qs) == 3)

    def tearDown(self):
        self.db.drop_tables([main.Answer, main.Question], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
