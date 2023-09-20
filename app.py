import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'CONNECT'])
def proxy():
    # Retrieve request method, URL, headers, and body
    method = request.method
    url = request.url
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    data = request.data
    if data:
        print(data)
    # Make the request to the target API server using requests library
    response = requests.request(method, url, headers=headers, data=data, stream=True)

    # Return the response from the target API server
    return jsonify(response.headers), response.status_code


if __name__ == '__main__':
    app.run()
