from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(100))
    amount = db.Column(db.Float)

    def __repr__(self):
        return f"<Transaction {self.id} {self.description} {self.amount}>"

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = request.form['amount']
    new_transaction = Transaction(description=description, amount=amount)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
