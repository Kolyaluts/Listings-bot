import requests

TOKEN = '7427905616:AAFO6yeDs6o1WlsjzfThS8hMcZAmESFj3f8'

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
requests.get(url, params={"offset": -1})
