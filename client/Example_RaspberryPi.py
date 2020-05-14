from .src.piclient import PiClient

# Setup the PiClient
client = PiClient(
    url='http://127.0.0.1',
    token='a_random_token_please'
)

# Ping the API server to check its uptime
#   This will return either True or False
print(client.ping())

# Send an image to detect the figures
#   This will return two variables
#       1. the list of pieces for the game logic
#       2. debug infos, if client.detect(debug=True)
pieces, _ = client.detect()
print(pieces)
