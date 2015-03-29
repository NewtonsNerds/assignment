import os
import Assignment
import unittest
import tempfile

class assignmentTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, assignment.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = assignment.app.test_client()
        assignment.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(assignment.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()