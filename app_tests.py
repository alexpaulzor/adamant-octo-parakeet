import app
import unittest
import json

class AppTestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.app.test_client()

  def test_get_empty_user(self):
    rv = self.app.get('/users/u0')
    assert rv.status_code == 404
  def test_put_empty_user(self):
    rv = self.app.put('/users/u0')
    assert rv.status_code == 404
  def test_delete_empty_user(self):
    rv = self.app.delete('/users/u0')
    assert rv.status_code == 404
  
  def test_create_user_no_groups(self):
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u1",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": []
    }
    ''')

    assert rv.status_code == 201
    assert 'fname1' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 0

  def test_create_user_new_group(self):
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u2",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": ["g0"]
    }
    ''')

    assert rv.status_code == 201
    assert 'fname1' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 1

  def test_create_user_existing_group(self):
    self.app.post('/groups', content_type='application/json', data='''{
      "name": "g1"}''')
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u3",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": ["g1"]
    }
    ''')

    assert rv.status_code == 201
    assert 'fname1' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 1

  def test_create_user_existing_userid(self):
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u4",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": []
    }
    ''')

    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u4",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": []
    }
    ''')

    assert rv.status_code == 409

  def test_put_user_no_groups(self): 
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u5",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": ["g5"]
    }
    ''')
    rv = self.app.put('/users/u5', content_type='application/json', data='''{
      "userid": "u5",
      "first_name": "fname2",
      "last_name": "lname2",
      "groups": []
    }
    ''')

    assert rv.status_code == 200
    assert 'lname2' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 0

  def test_put_user_new_group(self):
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u6",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": ["g6"]
    }
    ''')
    rv = self.app.put('/users/u6', content_type='application/json', data='''{
      "userid": "u6",
      "first_name": "fname2",
      "last_name": "lname2",
      "groups": ["g6", "g7"]
    }
    ''')

    assert rv.status_code == 200
    assert 'lname2' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 2

  def test_put_user_existing_group(self):
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u7",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": []
    }
    ''')
    self.app.post('/groups', content_type='application/json', data='''{
      "name": "group10"
    }
    ''')
    rv = self.app.put('/users/u7', content_type='application/json', data='''{
      "userid": "u7",
      "first_name": "fname2",
      "last_name": "lname2",
      "groups": ["group10"]
    }
    ''')

    assert rv.status_code == 200
    assert 'lname2' in rv.data
    result = json.loads(rv.data)
    assert len(result['groups']) == 1

  def test_put_user_change_userid(self):
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u99",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": []
    }
    ''')
    rv = self.app.put('/users/u99', content_type='application/json', data='''{
      "userid": "u98",
      "first_name": "fname2",
      "last_name": "lname2",
      "groups": []
    }
    ''')

    assert rv.status_code == 409

    rv = self.app.get('/users/u99')
    assert rv.status_code == 200
    assert 'lname2' not in rv.data
    
    rv = self.app.get('/users/u98')
    assert rv.status_code == 404

  def test_delete_user(self):
    self.app.post('/users', content_type='application/json', data='''{
      "userid": "u9",
      "first_name": "fname1",
      "last_name": "lname1",
      "groups": ["g11"]
    }
    ''')
    rv = self.app.delete('/users/u9')
    assert rv.status_code == 200
    
    rv = self.app.get('/users/u9')
    assert rv.status_code == 404
    
    rv = self.app.get('/groups/g11')
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert len(result) == 0

  def test_get_empty_group(self):
    rv = self.app.get('/groups/g12')
    assert rv.status_code == 404

  def test_put_empty_group(self):
    rv = self.app.put('/groups/g13')
    assert rv.status_code == 404

  def test_delete_empty_group(self):
    rv = self.app.delete('/groups/g14')
    assert rv.status_code == 404

  def test_create_group_no_users(self):
    rv = self.app.post('/groups', content_type='application/json', data='''{
      "name": "g15"
    }
    ''')

    assert rv.status_code == 201
    result = json.loads(rv.data)
    assert len(result) == 0

    rv = self.app.get('/groups/g15')
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert len(result) == 0

  def test_put_group_no_users(self):
    rv = self.app.post('/groups', content_type='application/json', data='''{
      "name": "g16"
    }
    ''')
    rv = self.app.put('/groups/g16', content_type='application/json', data='''[]''')
    assert rv.status_code == 200
    result = json.loads(rv.data)
    assert len(result) == 0

  def test_put_group_new_users(self):
    rv = self.app.post('/groups', content_type='application/json', data='''{
      "name": "g17"
    }
    ''')
    rv = self.app.put('/groups/g17', content_type='application/json', data='''[
      "u100",
      "u101"
    ]''')
  
    assert rv.status_code == 200
    assert 'u101' in rv.data
    result = json.loads(rv.data)
    assert len(result) == 2

  def test_put_group_existing_users(self):
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u102",
      "groups": ["g102"]
    }
    ''')
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u103"
    }''')
    rv = self.app.put('/groups/g102', content_type='application/json', data='''[
      "u102",
      "u103"
    ]''')
    assert rv.status_code == 200
    assert 'u103' in rv.data
    result = json.loads(rv.data)
    assert len(result) == 2
  
  def test_delete_group(self):
    rv = self.app.post('/users', content_type='application/json', data='''{
      "userid": "u107",
      "groups": ["g107"]
    }
    ''')
    rv = self.app.delete('/groups/g107')
    assert rv.status_code == 200

    rv = self.app.get('/groups/g107')
    assert rv.status_code == 404

    rv = self.app.get('/users/u107')
    assert rv.status_code == 200
    assert 'g107' not in rv.data

if __name__ == '__main__':
  unittest.main()

