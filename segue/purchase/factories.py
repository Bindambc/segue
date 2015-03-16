from segue.factory import Factory

from models import Buyer, Purchase, Payment

class BuyerFactory(Factory):
    model = Buyer

class PurchaseFactory(Factory):
    QUERY_WHITELIST = ('customer_id',)
    model = Purchase

    @classmethod
    def create(cls, buyer, product, account):
        result = cls.model()
        result.buyer = buyer
        result.product = product
        result.customer = account
        return result

class PaymentFactory(Factory):
    model = Payment

    @classmethod
    def create(cls, purchase, target_model=Payment):
        payment = target_model()
        payment.purchase = purchase
        payment.amount   = purchase.outstanding_amount
        return payment

