import tomllib
import serial
# parse config for client id, secret
data = {}
try:
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
    print(data)
except FileNotFoundError:
    print("Error: config.toml not found.")
except tomllib.TOMLDecodeError as e:
    print(f"Error decoding TOML: {e}")

API_ENDPOINT = 'https://discord.com/api/v10'
redirect = 'http://127.0.0.1/callback'
client_id = data["client_id"]
client_secret = data["client_secret"]


import requests
def exchange_code(code):
  data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(client_id, client_secret))
  r.raise_for_status()
  return r.json()

def refresh_token(refresh_token):
  data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(client_id, client_secret))
  r.raise_for_status()
  return r.json()


from pypresence import Client # The simple rich presence client in pypresence
import time
cl = Client(client_id)  # InitializeALARM_POW_PIN the Presence client

cl.start() # Start the handshake loop

refresh = ''
access_token = ''
try:
    with open(".refresh_token","r") as f:
        refresh = f.readline().strip()
    o = refresh_token(refresh)
    print(o)
    with open(".refresh_token","w") as f:
        f.write(o['refresh_token'])
    print("got access token by refreshing")
    access_token = o['access_token']
except:
    auth = cl.authorize(str(client_id), ['rpc'])
    code_grant = auth['data']['code']
    print("got past auth",code_grant)
    o = exchange_code(code_grant)
    with open(".refresh_token","w") as f:
        f.write(o['refresh_token'])
    print("got access token by reauth")
    access_token = o['access_token']

#need to save the refresh token
# we authorize the first time then we can just refresh and authenticate
cl.authenticate(access_token)


ser = serial.Serial('/dev/ttyUSB0', 9600)
def voice_update(data):
    print('voice updated to ' + str(data['mute']))
    if data['deaf']:
        ser.write("True\n".encode())
    else:
        ser.write((str(data['mute'])+'\n').encode())

cl.register_event('VOICE_SETTINGS_UPDATE',voice_update)

while True:
    cl.get_voice_settings()['data']['mute']
    time.sleep(.2) # Can only update rich presence every 15 seconds
