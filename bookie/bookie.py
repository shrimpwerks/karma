import threading
import time
import requests

from flask import Flask, request, abort
from hilo import HiLo
from docopt import docopt, DocoptExit

app = Flask(__name__)

doc = """Bookie.

Usage:
  /bookie create --quantity=<qty> --unit=<unit>
  /bookie join
  /bookie help

Options:
  --quantity=<qty> Quantity for the game [default: 100]
  --unit=<unit>    Unit for the game [default: karma]
"""

current_wager: HiLo = None

def create_game(user_id, quantity, unit, response_url):
    global current_wager

    if current_wager is not None:
        raise "there is another active wager. use `/bookie join` to join it."

    current_wager = HiLo(quantity, unit, response_url=response_url)

    t = threading.Thread(target=finalize_game, args=(current_wager))
    t.start()

    return "game started."

def finalize_game(wager):
    time.sleep(60)

    (win, lose) = wager.finalize()
    delta = win.value - lose.value

    requests.post(wager.callback, json={
        "text": f"@<{win.user_id}> owes @<{lose.user_id}> {delta} {wager.unit}.",
        "response_type": "in_channel",
    })

def join_game(user_id: str):
    if current_wager is None:
        raise "there is no current wager. use `/bookie create` to create one."
    roll = current_wager.roll(user_id)
    return f"@<{roll.user_id}> rolled {roll.value}."

def help():
    return doc


@app.route('/bookie', methods=['POST'])
def bookie():
    user_id = request.form.get('user_id')
    response_url = request.form.get('response_url')

    text = request.form.get("text")
    args = parser.parse_args(text.split())

    try:
        args = docopt(doc, help=False)
    except DocoptExit:
        pass

    if args.create:
        res = create_game(user_id, args.quantity, args.unit, response_url)
    if args.join:
        res = join_game(user_id)
    else:
        res = help()

    return {"text": res, "response_type": "ephemeral"}

if __name__ == "__main__":
    app.run(debug=True)
