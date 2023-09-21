import time

import requests
from flask import Flask, request, jsonify
from waitress import serve

from proxy import ProxyBox

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'CONNECT'])
def proxy():
    # Retrieve request method, URL, headers, and body
    print(request.method)
    print(request.headers)
    print(request.data)
    method = request.method
    url = "https://api.openai.com/v1/chat/completions"
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    data = request.data
    # Make the request to the target API server using requests library
    response = requests.request(method, url, headers=headers, data=data, stream=True)

    # Return the response from the target API server
    return jsonify(response), response.status_code


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
    # box = ProxyBox(base_url='0.0.0.0', port=8080)
    # box.start()
    #
    # while True:
    #     time.sleep(30)
    #     print("Live")