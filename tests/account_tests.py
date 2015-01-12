import json
import mockito

from werkzeug.exceptions import NotFound

from segue.account import AccountController, AccountService, Account
from segue.errors import SegueValidationError

from support import SegueApiTestCase, ValidAccountFactory, InvalidAccountFactory, hashie

class AccountServiceTestCases(SegueApiTestCase):
    def setUp(self):
        super(AccountServiceTestCases, self).setUp()
        self.service = AccountService()

    def test_invalid_account_raises_validation_error(self):
        account = InvalidAccountFactory().to_json()

        with self.assertRaises(SegueValidationError):
            self.service.create(account)

    def test_create_and_retrieve_of_valid_account(self):
        account = ValidAccountFactory().to_json()

        saved = self.service.create(account)
        retrieved = self.service.get_one(saved.id)

        self.assertEquals(saved, retrieved)
#
#     def test_non_existing_entity_is_none(self):
#         retrieved = self.service.get_one(1234)
#         self.assertEquals(retrieved, None)
#
# class ProposalControllerTestCases(SegueApiTestCase):
#     def setUp(self):
#         super(ProposalControllerTestCases, self).setUp()
#         self.mock_service = self.mock_controller_dep('proposals', 'service')
#
#     def _build_validation_error(self):
#         error_1 = hashie(message="m1", schema_path=["1","2"])
#         error_2 = hashie(message="m2", schema_path=["3","4"])
#
#         return SegueValidationError([error_1, error_2])
#
#     def test_invalid_entities_become_400_error(self):
#         data = { "arbitrary": "json that will be mocked out anyway" }
#         raw_json = json.dumps(data)
#         validation_error = self._build_validation_error()
#         mockito.when(self.mock_service).create(data).thenRaise(validation_error)
#
#         response = self.jpost('/proposal', data=raw_json)
#         errors = json.loads(response.data)['errors']
#
#         self.assertEquals(errors['1.2'], 'm1')
#         self.assertEquals(errors['3.4'], 'm2')
#         self.assertEquals(response.status_code, 400)
#         self.assertEquals(response.content_type, 'application/json')
#
#     def test_json_input_is_sent_to_service_for_creation(self):
#         data = { "arbitrary": "json that will be mocked out anyway" }
#         raw_json = json.dumps(data)
#         mockito.when(self.mock_service).create(data).thenReturn('bla')
#
#         response = self.jpost('/proposal', data=raw_json)
#
#         mockito.verify(self.mock_service).create(data)
#         self.assertEquals(response.status_code, 201)
#
#     def test_404s_on_non_existing_entity(self):
#         mockito.when(self.mock_service).get_one(456).thenReturn(None)
#
#         response = self.jget('/proposal/456')
#
#         self.assertEquals(response.status_code, 404)
#
#     def test_200_on_existing_entity(self):
#         mock_proposal = ValidProposalFactory.build()
#         mockito.when(self.mock_service).get_one(123).thenReturn(mock_proposal)
#
#         response = self.jget('/proposal/123')
#
#         self.assertEquals(response.status_code, 200)
#
#     def test_response_is_json(self):
#         mock_proposal = ValidProposalFactory.build()
#         mockito.when(self.mock_service).get_one(123).thenReturn(mock_proposal)
#
#         response = self.jget('/proposal/123')
#         content = json.loads(response.data)['resource']
#
#         self.assertEquals(content['title'],    mock_proposal.title)
#         self.assertEquals(content['full'],     mock_proposal.full)
#         self.assertEquals(content['summary'],  mock_proposal.summary)
#         self.assertEquals(content['language'], mock_proposal.language)
#         self.assertEquals(content['level'],    mock_proposal.level)
