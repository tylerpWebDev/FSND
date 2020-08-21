from flask import Flask
import urllib.request
import os
import json

client_secret = os.environ.get('CLIENT_SECRET')
client_id = os.environ.get('CLIENT_ID')
audience = os.environ.get('AUDIENCE')


def get_token(user, pwd):
    data = dict(
        grant_type="password",
        username=user,
        password=pwd,
        audience="castingagency",
        client_id=client_id,
        client_secret=client_secret)

    data_encode = urllib.parse.urlencode(data).encode('utf-8')
    url = 'https://udacity-capstone-castingagency.us.auth0.com/oauth/token'
    req = urllib.request.Request(
        url, data_encode, {
            'Content-Type': 'application/x-www-form-urlencoded'})

    f = urllib.request.urlopen(req)
    token = json.loads(f.read().decode("utf-8"))['access_token']
    f.close()
    return token


producer_token = get_token("producer@casting.com", "Testpassword!")

print("")
print("Producer Token")
print(producer_token)
print("")
