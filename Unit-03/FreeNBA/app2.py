import requests

url = "https://free-nba.p.rapidapi.com/players"

querystring = {"page":"0","per_page":"25"}

headers = {
    'x-rapidapi-host': "free-nba.p.rapidapi.com",
    'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxx"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)



#response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)
