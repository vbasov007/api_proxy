from flask import Flask, request
import requests
from waitress import serve


import os

# API_HOST = os.environ.get('API_HOST'); assert API_HOST, 'Envvar API_HOST is required'
API_HOST = r"https://api.openai.com/v1/chat/completions"


app = Flask(__name__)

@app.route('/', methods=['POST'])
def replace_url_handler():
    # Get the request data
    data = request.get_json()

    # Get the original request method, headers, and data
    method = data.get('method')
    headers = data.get('headers')
    url = data.get('url')
    payload = data.get('payload')

    print(method, headers, url, payload)
    # Replace the URL with the new one
    new_url = API_HOST
    url = url.replace(url, new_url)

    # Send the updated request with the original method, headers, and data
    response = requests.request(method, url, headers=headers, data=payload)

    # Return the response object
    return response.json(), response.status_code, response.headers.items()


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
