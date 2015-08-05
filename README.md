# adamant-octo-parakeet

```
sudo pip install virtualenv
virtualenv env
env/bin/pip install -r requirements.txt
# Run tests
env/bin/python app_tests.py
# Run server
env/bin/python app.py

# Create a user
curl -H 'Content-Type: application/json' -X POST -d'{"userid": "user0"}' localhost:5000/users
```



