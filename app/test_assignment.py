import os
import assignment
import unittest
import tempfile
from behave import *

class AssignmentTestCase(unittest.TestCase):

    ''' Begin using code from http://flask.readthedocs.org/en/latest/testing/ 
        This code is used because it does the job well.
    '''

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, assignment.app.config['DATABASE'] = tempfile.mkstemp()
        assignment.app.config['TESTING'] = True
        self.app = assignment.app.test_client()
        assignment.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(assignment.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    # testing functions
    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/')
        assert b'no records' in rv.data

    ''' Stop using code from http://flask.readthedocs.org/en/latest/testing/ 
        Remaining testing functions are written by me (the student)
    '''

    def test_login(self):
        rv = self.login(assignment.app.config['USERNAME'],
                        assignment.app.config['PASSWORD'])
        assert b'You are logged in' in rv.data

    def test_logout(self):
        rv = self.logout()
        assert b'You were logged out' in rv.data

    def test_BadUsername(self):
        rv = self.login(assignment.app.config['USERNAME'] + 'Blah',
                        assignment.app.config['PASSWORD'])
        assert b'no matching username' in rv.data

    def test_BadPassword(self):
        rv = self.login(assignment.app.config['USERNAME'],
                        assignment.app.config['PASSWORD'] + 'Blah')
        assert b'password is wrong' in rv.data

    def test_SaveLog(self):
        rv = self.login(assignment.app.config['USERNAME'],
                        assignment.app.config['PASSWORD'])
        rv = self.app.post('/add_entry', data=dict(
            user='Brett',
            log='Test log'
        ), follow_redirects=True)
        assert (b'successfully saved' in rv.data)

    @given(u'user tried to save with invalid notes')
    def test_DontSaveLog(self):
        rv = self.login(assignment.app.config['USERNAME'],
                        assignment.app.config['PASSWORD'])
        rv = self.app.post('/add_entry', data=dict(
            user='Brett',
            logged='Test log'
        ), follow_redirects=True)
        self.assertFalse(b'successfully saved' in rv.data)





if __name__ == '__main__':
    unittest.main()