import mockito

from segue.purchase.pagseguro import PagSeguroPaymentService, PagSeguroSessionFactory
from segue.purchase.models import PagSeguroPayment

from ..support import SegueApiTestCase, hashie
from ..support.factories import *

class PagSeguroPaymentServiceTestCases(SegueApiTestCase):
    def setUp(self):
        super(PagSeguroPaymentServiceTestCases, self).setUp()
        self.factory = mockito.Mock()
        self.service = PagSeguroPaymentService(session_factory=self.factory)

    def test_creates_a_payment_on_db(self):
        account = self.create_from_factory(ValidAccountFactory, id=333)
        purchase = self.create_from_factory(ValidPurchaseFactory, id=666, customer=account)

        result = self.service.create(purchase, {})

        self.assertEquals(result.type, 'pagseguro')
        self.assertEquals(result.__class__, PagSeguroPayment)
        self.assertEquals(result.status, 'pending')
        self.assertEquals(result.reference, 'A00333-PU00666')
        self.assertEquals(result.amount, purchase.product.price)

    def test_processes_a_pagseguro_checkout(self):
        payment = self.create_from_factory(ValidPagSeguroPaymentFactory)
        session = mockito.Mock()

        mockito.when(self.factory).create_session(payment).thenReturn(session)
        mockito.when(session).checkout().thenReturn(hashie(payment_url='http://songa'))

        result = self.service.process(payment)

        self.assertEquals(result['redirectUserTo'], 'http://songa')

class PagSeguroSessionFactoryTestCases(SegueApiTestCase):
    def setUp(self):
        super(PagSeguroSessionFactoryTestCases, self).setUp()
        self.factory = PagSeguroSessionFactory(use_env='sandbox')

    def test_builds_a_pagseguro_session_from_payment(self):
        account  = self.create_from_factory(ValidAccountFactory)
        product  = self.create_from_factory(ValidProductFactory, price=200)
        purchase = self.create_from_factory(ValidPurchaseByPersonFactory, id=444, product=product, customer=account)
        payment  = self.create_from_factory(ValidPagSeguroPaymentFactory, id=999, amount=200, purchase=purchase)

        result = self.factory.create_session(payment)

        self.assertEquals(result.reference,          'SEGUE-FISL16-A00555-PU00444-PA00999')
        self.assertEquals(result.redirect_url,       'http://192.168.33.91:9001/api/purchases/444/payment/999/conclude')
        self.assertEquals(result.notification_url,   'http://192.168.33.91:9001/api/purchases/444/payment/999/notify')

        self.assertEquals(result.sender['name'],      purchase.buyer.name)
        self.assertEquals(result.sender['email'],     purchase.customer.email)
        self.assertEquals(result.sender['phone'],     "2345678")
        self.assertEquals(result.sender['area_code'], "51")

        self.assertEquals(result.shipping['type'], 3)
        self.assertEquals(result.shipping['street'],      purchase.buyer.address_street)
        self.assertEquals(result.shipping['number'],      purchase.buyer.address_number)
        self.assertEquals(result.shipping['complement'],  purchase.buyer.address_extra)
        self.assertEquals(result.shipping['postal_code'], purchase.buyer.address_zipcode)
        self.assertEquals(result.shipping['city'],        purchase.buyer.address_city)
        self.assertEquals(result.shipping['country'],     purchase.buyer.address_country)

        self.assertEquals(len(result.items), 1)
        self.assertEquals(result.items[0]['id'], '0001')
        self.assertEquals(result.items[0]['amount'], '200.00')
        self.assertEquals(result.items[0]['description'], product.description)
        self.assertEquals(result.items[0]['quantity'], 1)
        self.assertEquals(result.items[0]['weight'], 0)
