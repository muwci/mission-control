import os
import tempfile
import unittest

import mission_control


class MCAuthTestCase(unittest.TestCase):
    """
    Tests to verify authentication, and account type selection.
    """
    def setUp(self):
        self.db_fd, mission_control.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = mission_control.app.test_client()
        mission_control.database.init_db()
        self.app = mission_control.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(mission_control.app.config['DATABASE'])

    def login(self, useremail, password):
        return self.app.post('/login/',
                             data=dict(useremail=useremail, password=password),
                             follow_redirects=True)

    def test_valid_fac_login(self):
        rv = self.login('clyon@muwci.net', 'sealions')
        assert 'You were logged in successfully' in str(rv.data)

    def test_valid_stu_login(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        assert 'You were logged in successfully' in str(rv.data)

    def test_logout(self):
        rv = self.app.get('/logout/', follow_redirects=True)
        assert 'You were logged out'

    def test_invalid_password(self):
        rv = self.login('clyon@muwci.net', 'giraffes')
        assert 'Invalid password.' in str(rv.data)

    def test_invalid_username(self):
        rv = self.login('someoneelse@muwci.net', 'giraffes')
        assert 'Invalid email.' in str(rv.data)

    def test_no_login_button_after_login(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        login_button = "<li><a href=\"/login/\">Login</a></li>"
        assert login_button not in str(rv.data)

    def test_user_name_drop_down_after_login(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        user_dropdown = "G. Raffe<span class=\"caret\"></span>"
        assert user_dropdown in str(rv.data)

    def test_no_dropdown_on_logout(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        rv = self.app.get('/logout/', follow_redirects=True)
        user_dropdown = "G. Raffe<span class=\"caret\"></span>"
        assert user_dropdown not in str(rv.data)

    def test_nav_dropdown_student(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        assert "STUDENT ACCOUNT DROPDOWN LINKS" in str(rv.data)
        assert "FACULTY ACCOUNT DROPDOWN LINKS" not in str(rv.data)

    def test_nav_dropdown_faculty(self):
        rv = self.login('clyon@muwci.net', 'sealions')
        assert "FACULTY ACCOUNT DROPDOWN LINKS" in str(rv.data)
        assert "STUDENT ACCOUNT DROPDOWN LINKS" not in str(rv.data)

    def test_dashboard_actions_student(self):
        rv = self.login('graffe@muwci.net', 'giraffes')
        assert "STUDENT ACCOUNT ACTIONS" in str(rv.data)
        assert "COMMON ACCOUNT ACTIONS" in str(rv.data)
        assert "FACULTY ACCOUNT ACTIONS" not in str(rv.data)

    def test_dashboard_actions_faculty(self):
        rv = self.login('clyon@muwci.net', 'sealions')
        assert "FACULTY ACCOUNT ACTIONS" in str(rv.data)
        assert "COMMON ACCOUNT ACTIONS" in str(rv.data)
        assert "STUDENT ACCOUNT ACTIONS" not in str(rv.data)

if __name__ == '__main__':
    unittest.main()
