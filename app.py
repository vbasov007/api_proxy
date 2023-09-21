import time

import requests
from flask import Flask, request, jsonify, Response
from waitress import serve

from proxy import ProxyBox

app = Flask(__name__)


import os


# API_HOST = os.environ.get('API_HOST'); assert API_HOST, 'Envvar API_HOST is required'
API_HOST = "https://api.openai.com/v1/chat/completions"

@app.route('/', defaults={'path': ''})  # ref. https://medium.com/@zwork101/making-a-flask-proxy-server-online-in-10-lines-of-code-44b8721bca6
@app.route('/<path>')
def redirect_to_API_HOST(path):  #NOTE var :path will be unused as all path we need will be read from :request ie from flask import request
    res = requests.request(  # ref. https://stackoverflow.com/a/36601467/248616
        method          = request.method,
        url             = request.url.replace(request.host_url, f'{API_HOST}/'),
        headers         = {k:v for k,v in request.headers if k.lower() != 'host'}, # exclude 'host' header
        data            = request.get_data(),
        cookies         = request.cookies,
        allow_redirects = False,
    )

    #region exlcude some keys in :res response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']  #NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    #endregion exlcude some keys in :res response

    response = Response(res.content, res.status_code, headers)
    return response

# @app.route('/', methods=['GET', 'POST', 'CONNECT'])
# def proxy():
#     # Retrieve request method, URL, headers, and body
#     print(request.method)
#     print(request.headers)
#     print(request.data)
#     method = request.method
#     url = "https://api.openai.com/v1/chat/completions"
#     headers = {key: value for (key, value) in request.headers if key != 'Host'}
#     data = request.data
#     # Make the request to the target API server using requests library
#     response = requests.request(method, url, headers=headers, data=data, stream=True)
#
#     # Return the response from the target API server
#     return jsonify(response), response.status_code


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
    # box = ProxyBox(base_url='0.0.0.0', port=8080)
    # box.start()
    #
    # while True:
    #     time.sleep(30)
    #     print("Live")