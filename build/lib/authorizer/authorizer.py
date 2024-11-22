import json
import base64
from urllib.parse import quote, unquote
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Signer:
    def __init__(self, request_data):
        self.request_data = request_data

    def _get_http_method(self):
        return self.request_data['http_method'].lower()

    def _get_path(self):
        return unquote(self.request_data['path'])

    def _get_headers_data(self):

        headers = self.request_data['headers']

        if 'Host' not in headers.keys():
            raise Exception("Header 'Host' is required")

        host = headers['Host']

        header_data = f'host:{str(host)}'

        sorted_headers_key = sorted(filter(lambda key: key.startswith('x-api-'), headers))

        headers_data = list(map(lambda key: f'{key.lower()}:{str(headers[key])}', sorted_headers_key))

        return '&'.join([header_data, *headers_data])

    def _get_query_string_params_data(self):
        if 'query_string_parameters' not in self.request_data.keys():
            self.request_data['query_string_parameters'] = None

        query_params = self.request_data['query_string_parameters'] or {}

        query_params_data = map(lambda key: f'{quote(unquote(key))}={quote(unquote(query_params[key] or ""))}', sorted(query_params))

        return '&'.join(query_params_data)

    def _get_json_body(self):
        if 'body' not in self.request_data.keys() or not self.request_data['body']:
            return ''

        sorted_body = {}

        for key in sorted(self.request_data['body']):
            sorted_body[key] = self.request_data['body'][key]

        body = json.dumps(sorted_body, separators=(',', ':'))

        return body

    def _get_data(self):
        parts = []

        query_string = self._get_query_string_params_data()

        parts.append(self._get_http_method())
        parts.append(self._get_path())
        parts.append(self._get_headers_data())

        if query_string:
            parts.append(query_string)

        parts.append(self._get_json_body())

        return '\n'.join(parts)

    def sign(self, private_key):
        digest = SHA256.new()
        data = self._get_data()

        digest.update(data.encode('utf-8'))

        _private_key = RSA.importKey(private_key)

        signer = PKCS1_v1_5.new(_private_key)

        return base64.b64encode(signer.sign(digest)).decode('utf-8')

    def verify(self, public_key, signature):
        digest = SHA256.new()
        digest.update(self._get_data().encode('utf-8'))

        sig = base64.standard_b64decode(bytes(signature, 'utf-8'))

        _public_key = RSA.importKey(public_key)

        verifier = PKCS1_v1_5.new(_public_key)

        return verifier.verify(digest, sig)
