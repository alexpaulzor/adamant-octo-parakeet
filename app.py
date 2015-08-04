

from flask import Flask, request, Response, jsonify
app = Flask(__name__)

users = {}
groups = {}

class User:
  def __init__(self, params):
    self.groups = []
    self.first_name = None
    self.last_name = None
    self.update(params)

  def update(self, params):
    if 'userid' in params and self.userid != params['userid']:
      # TODO: handle changing user id
      pass
    self.userid = params['userid']
    if 'first_name' in params:
      self.first_name = params['first_name']
    if 'last_name' in params:
      self.last_name = params['last_name']
    if 'groups' in params:
      # TODO: map group name to objects
      # TODO: set difference
      for group_name in params['groups']:
        if group_name not in groups:
          groups[group_name] = Group(group_name)
        
        group = groups[group_name]
        group.add_user(self)
        self.groups.append(group)

  def to_json(self):
    return jsonify(userid=self.userid, first_name=self.first_name, last_name=self.last_name,
      groups=map(lambda g: g.name, self.groups))

  def destroy(self):
    for group in self.groups:
      group.remove_user(self)

class Group:
  def __init__(self, name=None):
    self.name = name
    self.users = []
  
  def add_user(self, user):
    if user not in self.users:
      self.users.append(user)

  def remove_user(self, user):
    if user in self.users:
      self.users.remove(user)

  def to_json(self):
    return jsonify(map(lambda u: u.userid, self.users))

  def destroy(self):
    for user in self.users:
      user.groups.remove(self)

  def set_users(self, users):
    added_users = set(self.users) - set(users)
    removed_users = set(users) - set(self.users)
    for user in added_users:
      user.groups.append(self)
      self.users.append(user)
    for user in removed_users:
      user.groups.remove(self)
      self.users.remove(user)

@app.route('/users/<userid>', methods=['GET'])
def get(userid):
  if userid not in users:
    return jsonify(error="user %s not found" % userid), 404
  return users[userid].to_json()

@app.route('/users', methods=['POST'])
def create():
  user = request.get_json()
  if 'userid' not in user:
    return jsonify(error="body must contain userid"), 400
  if user['userid'] in users:
    return jsonify(error="user %s already exists" % user['userid']), 409
  users[user['userid']] = User(user)

  return users[user['userid']].to_json(), 201

@app.route('/users/<userid>', methods=['DELETE'])
def delete(userid):
  if userid not in users:
    return jsonify(error="user %s not found" % userid), 404
  user = users[userid]
  user.destroy()
  del users[userid]
  return user.to_json()

@app.route('/users/<userid>', methods=['PUT'])
def put(userid):
  if userid not in users:
    return jsonify(error="user %s not found" % userid), 404
  user = users[userid]
  user.update(request.get_json())
  return user.to_json()

@app.route('/groups/<groupid>', methods=['GET'])
def get_group(groupid):
  if groupid not in groups:
    return jsonify(error="group %s not found" % groupid), 404
  return groups[groupid].to_json()

@app.route('/groups', methods=['POST'])
def create_group():
  group = request.get_json()
  if 'name' not in group:
    return jsonify(error="body must contain name"), 400
  if group['name'] in groups:
    return jsonify(error="group %s already exists" % group['name']), 409
  groups[group['name']] = Group(group['name'])

  return groups[group['name']].to_json(), 201

@app.route('/groups/<groupid>', methods=['DELETE'])
def delete_group(groupid):
  if groupid not in groups:
    return jsonify(error="group %s not found" % groupid), 404
  group = groups[groupid]
  group.destroy()
  del groups[groupid]
  return group.to_json()

@app.route('/groups/<groupid>', methods=['PUT'])
def put_group(groupid):
  if groupid not in groups:
    return jsonify(error="group %s not found" % groupid), 404
  group = groups[groupid]
  user_ids = set(request.get_json())
  # TODO: user id not found?
  user_objs = map(lambda uid: users[uid], user_ids)
  group.set_users(user_objs)
  return group.to_json()


if __name__ == "__main__":
  app.run(debug=True)
