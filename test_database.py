import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.Database = Database("testing_db")
        self.db = self.Database.db
        self.Database.start_connection()

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertEqual(sorted(tables), ['admin', 'question'])
        cols_ans = self.db.get_columns('admin')
        cols_qs = self.db.get_columns('question')

        self.assertTrue(len(cols_ans) == 2)
        self.assertTrue(len(cols_qs) == 6)

    def test_adding_questions(self):
        self.Database.add_new_question("Nik", "How much wood could a woodchuck chuck if a woodchuck could chuck wood?",
                                       "Tree")
        self.assertEqual(self.Database.Question.select().count(), 1)
        self.assertEqual(self.Database.Question.get(self.Database.Question.id == 1).body,
                         "How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.assertEqual(self.Database.Question.get(self.Database.Question.id == 1).company,
                         "Nik")
        self.assertEqual(self.Database.Question.get(self.Database.Question.id == 1).data_structure,
                         "Tree")

        self.Database.add_new_question("Nik", "What is the meaning of life?", "Tree")
        self.assertEqual(self.Database.Question.select().count(), 2)
        self.Database.add_new_question("Nik", "How much wood could a woodchuck chuck if a woodchuck could chuck wood?",
                                       "Tree")
        self.assertEqual(self.Database.Question.select().count(), 2)
        # Testing this post integrity error
        self.Database.add_new_question("Nik", "What is love?", "Tree")
        self.assertEqual(self.Database.Question.select().count(), 3)

    def test_question_retrieval(self):
        if self.Database.Question.select().count() < 1:
            self.Database.add_new_question("Nik",
                                           "How much wood could a woodchuck chuck if a woodchuck could chuck wood?",
                                           "Tree")
            self.Database.add_new_question("Nik", "What is the meaning of life?", "Tree")
            self.assertEqual(self.Database.Question.select().count(), 2)

        q1 = self.Database.get_day_question()
        q2 = self.Database.get_day_question()

        self.assertIsNotNone(q1)
        self.assertIsNotNone(q2)

        self.assertEqual(q1, q2)

        q3 = self.Database.get_index_question(1)
        q4 = self.Database.get_index_question(2)

        self.assertIsNotNone(q3)
        self.assertIsNotNone(q4)
        self.assertNotEqual(q3, q4)

    def test_question_deleting(self):
        self.Database.add_new_question("Nik", "How much wood could a woodchuck chuck if a woodchuck could chuck wood?", "Tree")
        self.Database.add_new_question("Nik", "What is the meaning of life?", "Tree")
        self.Database.add_new_question("Nik", "What is love?", "Tree")

        self.Database.remove_question(1)
        self.assertTrue(self.Database.Question.select().count(), 2)
        self.Database.remove_question(4)
        self.assertTrue(self.Database.Question.select().count(), 2)

    def test_adding_admins(self):
        self.Database.add_admin("12345")
        self.Database.add_admin("54321")
        self.Database.add_admin("54321")

        self.assertEqual(self.Database.Admin.select().count(), 2)
        self.assertEqual(self.Database.Admin.get(self.Database.Admin.id == 1).user_id, "12345")

    def test_admin_check(self):
        self.Database.add_admin("12345")

        self.assertTrue(self.Database.is_admin("12345"))
        self.assertFalse(self.Database.is_admin("54321"))

    def test_admin_deleting(self):
        self.Database.add_admin("12345")
        self.Database.add_admin("54321")

        self.assertEqual(self.Database.remove_admin("54321"), "54321")
        self.assertEqual(self.Database.Admin.select().count(), 1)

        self.assertIsNone(self.Database.remove_admin("54321"))
        self.assertEqual(self.Database.Admin.select().count(), 1)

    def tearDown(self):
        self.db.drop_tables([self.Database.Admin, self.Database.Question], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
