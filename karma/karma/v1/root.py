import argparse
import requests
from flask import Blueprint, request, abort, jsonify
from flask import current_app as app


root = Blueprint('root', __name__, url_prefix='/v1')


def get_parser():
    '''build argument parser tree'''

    root_parser = argparse.ArgumentParser('karma')
    subparsers = root_parser.add_subparsers(dest='command')

    give_parser = subparsers.add_parser('give')
    give_parser.set_defaults(func=give)
    give_parser.add_argument('target')

    return root_parser


def give(args, form):
    '''process a give request'''

    try:
        target_id, target_name = args.target.split('|')
    except ValueError:
        abort(404)

    source_id = form['user_id']
    source_name = form['user_name']
    currency = app.config['DEFAULT_CURRENCY']

    requests.post(f"http://{app.config['LEDGER_ADDR']}/v1/transactions", json={
        'source': source_id,
        'destination': target_id,
        'amount': 1,
        'currency': currency,
        'description': f'a {currency} given from {source_name} to {target_name}'
    })

    return {
        'message': f'Sucessfully gave 1 {currency} to {target_name}'
    }


@root.route('/', methods=['POST'])
def parse_request():
    try:
        text_split = request.form['text'].split(' ')
    except (KeyError, AttributeError):
        abort(404)

    args = get_parser().parse_args(text_split)
    response = args.func(args, request.form)

    return jsonify(response)
