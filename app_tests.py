import flaskr
import unittest

class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    self.app = flaskr.app.test_client()

  def tearDown(self): pass

  def test_empty_db(self):
    rv = self.app.get('/')
    assert 'No entries here so far' in rv.data

if __name__ == '__main__':
  unittest.main()

