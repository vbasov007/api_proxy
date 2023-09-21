from flask import Flask, request, jsonify
import requests
from waitress import serve


app = Flask(__name__)

@app.route('/', methods=['POST'])
def replace_url_handler():
    # Get the request data
    request_data = request.get_json()

    print(request_data)

    # Get the original request method, headers, and data
    method = request_data.get('method')
    print(method)
    headers = request_data.get('headers')
    url = request_data.get('url')
    payload = request_data.get('payload')

    print(method, headers, url, payload)
    # Replace the URL with the new one

    # Send the updated request with the original method, headers, and data
    response = requests.request(method, url, headers=headers, json=payload)

    print(response.json(), response.status_code, response.headers.items())

    # Return the response object
    # return response.json(), response.status_code, response.headers.items()
    return jsonify(response.json())


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
