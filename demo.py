import requests

# url = "http://127.0.0.1:5001/json/jsonify"
# response = requests.get(url)
# print(type(response))
# print(response.json())



url = "http://127.0.0.1:5001/cat_add"
data = {"id":"5", "name": "hh", "age":5}
response = requests.post(url, data=data)
print(type(response))
print(response.json())