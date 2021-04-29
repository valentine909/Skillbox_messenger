import time
from flask import Flask, request, abort
from datetime import datetime


app = Flask(__name__)
db = [
    {
        'name': 'Nick',
        'text': 'Hello!',
        'time':  time.time()
    },
    {
        'name': 'Ivan',
        'text': 'Hello, Nick!',
        'time': time.time()
    }
]


@app.route("/")
def hello():
    return "Hello, Messenger!"


@app.route("/status")
def status():
    my_status = {
        'status': True,
        'name': "My Messenger",
        'time': str(datetime.now()),
        'number_of_messages': len(db),
        'number_of_users': len(set(i['name'] for i in db))
    }
    return my_status


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    name = data['name']
    text = data['text']
    if not isinstance(name, str) \
            or not isinstance(text, str):
        return abort(400)
    if name == '' or text == '':
        return abort(400)
    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })
    if text == '/help':
        db.append({
            'name': 'BOT',
            'text': 'Ha-ha, looser!',
            'time': time.time()
        })
    return {'OK': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except ValueError:
        abort(400)
    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)
    return {'messages': messages[:50]}


app.run()
