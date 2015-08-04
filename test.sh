#!/bin/bash

URL='localhost:5000'
CURL="curl -D- -H 'Content-Type: application/json'"

echo "Get empty user"
$CURL $URL/users/a
echo "Put empty user"
$CURL -X PUT $URL/users/a -d '{"userid":"a"}'
echo "Delete empty user"
$CURL -X DELETE $URL/users/a

echo "Create user (no groups)"
echo "Create user (new group)"
echo "Create user (existing group)"

echo "Update user (no groups)"
echo "Update user (new group)"
echo "Update user (existing group)"

echo "Get empty group"
$CURL $URL/groups/a
echo "Put empty group"
$CURL -X PUT $URL/groups/a -d '["a"]'
echo "Delete empty group"
$CURL -X DELETE $URL/groups/a



$CURL -X POST -d '{"userid":"alex2","groups":["a"]}' $URL/
