

from flask import Flask, request, Response, jsonify, json
app = Flask(__name__)

users = {}
groups = {}

def find_or_create_user(userid):
  if userid not in users:
    users[userid] = User({'userid': userid})
  return users[userid]

def find_or_create_group(groupid):
  if groupid not in groups:
    groups[groupid] = Group(groupid)
  return groups[groupid]


class User:
  def __init__(self, params):
    self.userid = None
    self.groups = set()
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
      # TODO: missing group?
      group_objs = set(map(find_or_create_group, params['groups']))
      added_groups = group_objs - self.groups
      removed_groups = self.groups - group_objs

      for group in removed_groups:
        group.remove_user(self)
      for group in added_groups:
        group.add_user(self)

  def to_json(self):
    return jsonify(userid=self.userid, first_name=self.first_name, last_name=self.last_name,
      groups=map(lambda g: g.name, self.groups))

  def destroy(self):
    for group in self.groups.copy():
      group.remove_user(self)


######################################

class Group:
  def __init__(self, name=None):
    self.name = name
    self.users = set()
  
  def add_user(self, user):
    if user not in self.users:
      self.users.add(user)
      user.groups.add(self)

  def remove_user(self, user):
    if user in self.users:
      self.users.remove(user)
      user.groups.remove(self)

  def to_json(self):
    return json.dumps(map(lambda u: u.userid, self.users))

  def destroy(self):
    for user in self.users.copy():
      self.remove_user(user)

  def set_users(self, user_ids):
    user_objs = set(map(find_or_create_user, user_ids))
    removed_users = self.users - user_objs
    added_users = user_objs - self.users

    for user in added_users:
      self.add_user(user)
    for user in removed_users:
      self.remove_user(user)

######################################

@app.route('/users/<userid>', methods=['GET'])
def get(userid):
  if userid not in users:
    return jsonify(error="user %s not found" % userid), 404
  return users[userid].to_json()

@app.route('/users', methods=['POST'])
def create():
  user = request.get_json()
  if not user or 'userid' not in user:
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
  user_ids = request.get_json()
  group.set_users(user_ids)
  return group.to_json()


if __name__ == "__main__":
  app.run(debug=True)
