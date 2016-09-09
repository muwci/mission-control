import unittest
import mission_control


class RoutesTest(unittest.TestCase):
    """
    Checks basic routes to pages in the applicaiton.
    """

    def setUp(self):
        self.app = mission_control.app.test_client()

    def check_route(self, route, test_string=None):
        """
        For some page `page` we have set up routes ONLY to
        .../page/ and NOT to .../page. Just check if that is working properly.
        The templates the pages are supposed to use have a simple test string
        embedded in them, we just check if the string is there.
        """
        if not test_string:
            test_string = route.upper()

        rv = self.app.get('/{}'.format(route))
        assert '{}.HTML TEST STRING'.format(test_string) not in str(rv.data)
        rv = self.app.get('/{}/'.format(route))
        assert '{}.HTML TEST STRING'.format(test_string) in str(rv.data)

    def test_route_index(self):
        rv = self.app.get('/')
        assert 'INDEX.HTML TEST STRING' in str(rv.data)

    def test_route_dashboard(self):
        self.check_route('dashboard')

    def test_route_add_scores(self):
        self.check_route('dashboard/edit', test_string='ADDSCORES')

    def test_route_view_scores(self):
        self.check_route('dashboard/view', test_string='VIEWSCORES')

    def test_route_help(self):
        self.check_route('help')

    def test_route_settings(self):
        self.check_route('settings')

if __name__ == '__main__':
    unittest.main()
