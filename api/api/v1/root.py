import argparse
import requests
from flask import Blueprint, request, abort, jsonify
from flask import current_app as app


root = Blueprint('root', __name__, url_prefix="/v1")


def get_parser():
    '''build argument parser tree'''

    root_parser = argparse.ArgumentParser('gbp')
    subparsers = root_parser.add_subparsers(dest='command')

    give_parser = subparsers.add_parser('give')
    give_parser.set_defaults(func=give)
    give_parser.add_argument('target')

    return root_parser


def give(args):
    '''process a give request'''

    try:
        u_id, u_name = args.target.split("|")
    except ValueError:
        abort(404)

    requests.post("http://ledger:80/v1/transactions", json={
        "source": "god",
        "destination": u_id,
        "amount": 1,
        "currency": "gbp",
        "description": "hello gbp"
    })

    return {
        "message": f"Sucessfully gave 1 gbp to {u_name}"
    }


@root.route('/', methods=["POST"])
def parse_request():
    try:
        text_split = request.form["text"].split(" ")
    except (KeyError, AttributeError):
        abort(404)

    args = get_parser().parse_args(text_split)
    response = args.func(args)

    return jsonify(response)
