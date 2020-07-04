import os

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///default.db'

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    source = db.Column(db.Text)
    destination = db.Column(db.Text)
    amount = db.Column(db.Integer)
    currency = db.Column(db.Text)
    description = db.Column(db.Text)

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    source = fields.Str()
    destination = fields.Str()
    amount = fields.Int()
    currency = fields.Str()
    description = fields.Str()

tx_schema = TransactionSchema()
txs_schema = TransactionSchema(many=True)

@app.route('/v1/transactions', methods=['POST'])
def create_transaction():
    payload = request.get_json()

    tx = Transaction(
        source=payload.get('source'),
        destination=payload.get('destination'),
        amount=payload.get('amount'),
        currency=payload.get('currency'),
        description=payload.get('description'))
    db.session.add(tx)
    db.session.commit()

    return {"transaction": tx_schema.dump(tx)}

@app.route('/v1/transactions', methods=['GET'])
def list_transactions():
    txs = db.session.query(Transaction).all()
    return {"transactions": txs_schema.dump(txs)}

@app.route('/v1/transactions/<txID>', methods=['GET'])
def get_transaction(txID: int):
    tx = db.session.query(Transaction).filter_by(id=txID).first()
    if tx is None:
        abort(404)
    return {"transaction": tx_schema.dump(tx)}

@app.route('/v1/balance/<userID>', methods=['GET'])
def get_balance(userID: str):
    balance = db.session.query(
        Transaction.destination.label('userID'),
        func.sum(Transaction.amount).label('amount')
    ).filter(Transaction.destination==userID
    ).group_by(Transaction.destination
    ).first()
    if balance is None:
        abort(404)
    return { "balance": balance._asdict() }

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
