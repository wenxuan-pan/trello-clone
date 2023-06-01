from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())


class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'date_created')


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


@app.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')


@app.cli.command('seed')
def seed_db():
    # create an instance of the Card model in memory
    cards = [Card(
        title='Start the project',
        description='Stage 1 - Create an ERD',
        status="Done",
        date_created=date.today()
    ),
        Card(
        title='ORM queries',
        description='Stage 2 - Implement several queries',
        status='In Progress',
        date_created=date.today()
    ),
        Card(
        title='Marshmellow',
        description='Stage 3 - Implement jsonify of models',
        status='In Progress',
        date_created=date.today()
    ),]

    # truncate table; delete all rows in the table
    db.session.query(Card).delete()

    # add the card to the session (transaction)
    db.session.add_all(cards)

    # commit the transaction to the database
    db.session.commit()
    print('Models seeded')


@app.route('/cards')
def all_cards():
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return cards_schema.dump(cards)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
