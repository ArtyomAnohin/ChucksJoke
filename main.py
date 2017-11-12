from flask import Flask
from flask import request
from flask import make_response
import json
import logging as l
import requests

app = Flask(__name__)
l.getLogger('flask_assistant').setLevel(l.DEBUG)


@app.route('/')
def hello():
    return 'Hello  Beautiful World!\n'


@app.route('/apiai', methods=['POST'])
def apiai_response():
    l.debug("Debug:")

    req = request.get_json(silent=True, force=True)
    person = req["result"]["parameters"]["person"]

    if person == "":
        speech = "Chuck Norris only!"
    else:
        try:
            r = requests.get('https://api.chucknorris.io/jokes/random')
            data = json.dumps(r.json())
            result = json.loads(data)['value']
            speech = result
        except:
            speech = "Chuck Norris hides. Internet is down"

    my_response = {
        "speech": speech,
        "displayText ": speech,
    }

    res = json.dumps(my_response)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r


@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, nothing at this URL.', 404


if __name__ == '__main__':
    app.run(debug=True)
