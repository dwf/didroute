from collections import Mapping
import requests
from functools import partial


def validate_response(response_obj):
    if response_obj.status_code != requests.codes.ok:
        raise requests.HTTPError('expected status code {}, got {}'
                                 .format(requests.codes.ok,
                                         response_obj.status_code))
    response = response_obj.json()
    if response['status'] != 'success':
        raise VoipMSAPIError('API status returned {}'
                             .format(response['status']),
                             response)
    return response


class VoipMSAPIError(Exception):
    pass


class VoipMS(object):
    def __init__(self, username, password,
                 url='https://voip.ms/api/v1/rest.php'):
        self.username = username
        self.password = password
        self.url = url
        self.ivrs = Directory(self, 'getIVRs', 'ivrs', 'name')
        self.forwarders = Directory(self, 'getForwardings',
                                    'forwardings', 'description')
        self.dids = Directory(self, 'getDIDsInfo', 'dids', 'did',
                              partial(DID, api=self))

    @property
    def credentials(self):
        return {'api_' + s: getattr(self, s) for s in ('username', 'password')}


class Directory(Mapping):
    """
    Emulates a dictionary. Returned items are mutable but mutation
    has no effect.

    """
    def __init__(self, api, method_name, items_key, id_key, factory=dict):
        self.api = api
        self.method_name = method_name
        self.items_key = items_key
        self.id_key = id_key
        self.factory = factory

    def _query(self):
        params = {'method': self.method_name}
        params.update(self.api.credentials)
        response = validate_response(requests.get(self.api.url, params))
        return response[self.items_key]

    def __getitem__(self, key):
        response = self._query()
        for item in response:
            if item[self.id_key] == key:
                return self.factory(item)
        raise KeyError(key)

    def items(self):
        for item in self._query():
            key = item[self.id_key]
            yield key, self.factory(item)

    def keys(self):
        for key, _ in self.items():
            yield key

    def values(self):
        for _, value in self.items():
            yield value

    def __iter__(self):
        yield from self.keys()

    def __len__(self):
        return len(self._query())


class DID(dict):
    def __init__(self, mapping, api):
        self.api = api
        super(DID, self).__init__(mapping)

    def set_routing(self, which):
        if 'forwarding' in which:
            kind = 'fwd'
            key = which['forwarding']
        elif 'ivr' in which:
            kind = 'ivr'
            key = which[kind]
        routing = ':'.join((kind, key))
        params = {'method': 'setDIDRouting', 'routing': routing,
                  'did': self['did']}
        params.update(self.api.credentials)
        response = validate_response(requests.get(self.api.url, params))
        return response
