from flask import Flask
import urllib.request
import os
import json

client_secret = os.environ.get('CLIENT_SECRET')
client_id = os.environ.get('CLIENT_ID')
audience = os.environ.get('AUDIENCE')

print("")
print("")
print("client_secret", client_secret)
print("client_id", client_id)
print("audience", audience)

print("")
print("")


def cprint(label, data):
    print("")
    print(label)
    print(data)
    print("")


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


assistant_token = get_token("assistant@casting.com", "Testpassword!")
director_token = get_token("director@casting.com", "Testpassword!")
producer_token = get_token("producer@casting.com", "Testpassword!")

os.environ["ASSISTANT_TOKEN"] = assistant_token
os.environ["DIRECTOR_TOKEN"] = director_token
os.environ["PRODUCER_TOKEN"] = producer_token


cprint("Assistant Token", assistant_token)
cprint("Director Token", director_token)
cprint("Prodcuer Token", producer_token)