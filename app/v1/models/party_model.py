from app.v1.utilities.validator import generate_id, exists, validate_ints
from app.v1.utilities.validator import validate_strings
from .base_model import BaseModel


class Party(BaseModel):
    """ model for political party """

    parties = []

    def __init__(self, name=None, hq_address=None, logo_url=None):
        super().__init__('Party', self.parties)

        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "hq_address": self.hq_address,
            "logo_url": self.logo_url,
        }

    def from_json(self, json):
        self.__init__(json['name'], json['hq_address'], json['logo_url'])
        self.id = json['id']
        return self

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        for i in range(len(self.parties)):
            if self.parties[i]['id'] == self.id:
                party = self.parties[i]
                party['name'] = new_name
                self.parties[i] = party
                break

    def validate_object(self):

        if not validate_strings(self.name, self.hq_address, self.logo_url):
            self.error_message = "Integer not allowed in some fields "
            self.error_code = 400
            return False

        if len(self.name) < 4:
            self.error_message = "The {} name provided is short".format(self.object_name)
            self.error_code = 400
            return False

        if exists('name', self.name, self.parties):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()

