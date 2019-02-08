from app.tests.v1.base_test import Base
from app.v1.models.my_db import Database


class TestParties(Base):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required tests """
        super().setUp()

        self.party_list = Database().get_table(Database.PARTIES)

        self.new_party = {
            "name": "RADAR RADAR PARTY",
            "hq_address": "Mathare",
            "logo_url": "url"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST parties
    def test_create_party(self):
        """ Tests that a party was created successfully """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Party created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_party_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v1/parties', json={
            "hq_address": "Mathare",
            "logo_url": "url"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        """ Tests when there's no data provided """

        res = self.client.post('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')
        self.assertEqual(res.status_code, 400)

    def test_create_party_same_name(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Party exists')
        self.assertEqual(res.status_code, 400)


