from dataclasses import dataclass
from datetime import datetime, date
from websocket import create_connection
import json

@dataclass
class Petition:
    id: int
    title: str
    signatures: int
    author: str
    tags: list
    response: bool
    updates: list
    timestamp: date
    expires: date
    status: int
    in_progress: bool
    deleted: bool


# From web browser
headers = json.dumps({
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Host': 'pawprints.rit.edu',
    'Origin': 'https://pawprints.rit.edu',
    'Pragma': 'no-cache',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Key': 'bYbaIZLH7/k2NAhz56kWw==',
    'Sec-WebSocket-Version': '13',
    'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
})


# Launch the connection to the server.
# Perform the handshake.
ws = create_connection('wss://pawprints.rit.edu/ws/',headers=headers)
ws.send(json.dumps({"command":"paginate","sort":"most recent","filter":"all","page":1}))
# ws.send(json.dumps({"command":"all"}))
# ws.send(json.dumps({"command": "get", "id": 7}))
# Printing all the result


print("\nReciving paginate")
result = ws.recv()
print("Reciving all")
# result = ws.recv()

print("\nRemoving header")
result = result[14:result.find(', \"map\": {')]
print("Loading json")
data = json.loads(result)
print ("Length of data: " + str(len(data)))

# print(type(data[0]))
# print(data[0].values())

print("\nLoading Petitions List")
petitions = []
for i in data:
    date1 = datetime.strptime(i['timestamp'],'%B %d, %Y')
    date2 = datetime.strptime(i['expires'],'%B %d, %Y')
    petitions.append((Petition(
        id=int(i['id']),
        title=i["title"],
        signatures=int(i['signatures']),
        author=i['author'],
        tags=i['tags'],
        response=bool(i['response']),
        updates=list(i['updates']),
        timestamp= date1,
        expires= date2,
        status=int(i['status']),
        in_progress=bool(i['in_progress']),
        deleted=bool(i['deleted']))))

print("Finished Loading Petitions List")
print("Length of petitions: " + str(len(petitions)))

filename = "Output/" + str(datetime.now()) + " - Length: " + str(len(petitions)) + ".txt"
print("\nOpening "+filename)
with open(filename, 'a') as f:
    print("Writing to " + filename)
    for i in petitions:
        f.write(str(i))
        f.write("\n")
print(filename +" written\n")
