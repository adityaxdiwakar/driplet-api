payload = {
	"personalizations": [
		{
			"to": [
				{
					"email": "aditya@diwakar.io"
				}
			],
			"subject": "Hello world"
		}
	],
	"from": {
		"email": "noreply@driplet.cf"
	},
	"content": [
		{
			"type": "text/plain",
			"value": "Hello, world!"
		}
	]
}


import requests as r
from dotenv import load_dotenv
load_dotenv()

import os

API_KEY = os.getenv("API_KEY")

headers = {
	"Authorization": f"Bearer {API_KEY}",
	"Content-Type": "application/json"
}

s = r.post("https://api.sendgrid.com/v3/mail/send", headers=headers, data=payload)

print(s)
print(s.text)
