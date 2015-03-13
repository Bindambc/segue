from pagseguro import PagSeguro

from segue.factory import Factory

from models import Buyer, Purchase

class BuyerFactory(Factory):
    model = Buyer

class PurchaseFactory(Factory):
    model = Purchase

    @classmethod
    def create(self, buyer, product, account):
        result = Purchase()
        result.buyer = buyer
        result.product = product
        result.customer = account
        return result

class PagSeguroSessionFactory(object):
    def __init__(self):
        pass

    def create_session(self):
        instance = PagSeguro(config.PAGSEGURO_EMAIL, config.PAGSEGURO_TOKEN)
        instance.config.BASE_URL = config.PAGSEGURO_BASEURL
        return instance

    def example_purchase(self):
        pg = self.create_session()
        pg.shipping = None
        pg.reference_prefix = "SEGUE-FISL16-"
        pg.reference = "00123456789"
        pg.items = [ {"id": "0001", "description": "Produto 1", "amount": 354.20, "quantity": 2, "weight": 200} ]
        pg.redirect_url = "http://google.com"
        pg.notification_url = "http://google.com"
        return pg


