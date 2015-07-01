from datetime import timedelta
from segue.core import db
from ..models import Payment, Transition

class CashPayment(Payment):
    __mapper_args__ = { 'polymorphic_identity': 'cash' }

class CashTransition(Transition):
    __mapper_args__ = { 'polymorphic_identity': 'cash' }

    cashier_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    ip_addres  = db.Column(db.String)