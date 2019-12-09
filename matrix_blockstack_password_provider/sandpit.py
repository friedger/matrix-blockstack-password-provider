import coincurve
import encodings
import codecs
import binascii

import base64
import json
import sys
import jwt
import logging
from coincurve.ecdsa import der_to_cdata

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("sandpit")


privateKey = coincurve.PrivateKey.from_hex("278a5de700e29faae8e40e366ec5012b5ec63d36ec77e8a2417154cc1d25383f")
pubKey = privateKey.public_key.format()
logger.info(pubKey)

payload = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJpc3N1ZWRBdCI6IjE0NDA3MTM0MTQuODUiLCJjaGFsbGVuZ2UiOiI3Y2Q5ZWQ1ZS1iYjBlLTQ5ZWEtYTMyMy1mMjhiZGUzYTA1NDkiLCJpc3N1ZXIiOnsicHVibGljS2V5IjoiMDNmZGQ1N2FkZWMzZDQzOGVhMjM3ZmU0NmIzM2VlMWUwMTZlZGE2YjU4NWMzZTI3ZWE2NjY4NmMyZWE1MzU4NDc5IiwiY2hhaW5QYXRoIjoiYmQ2Mjg4NWVjM2YwZTM4MzgwNDMxMTVmNGNlMjVlZWRkMjJjYzg2NzExODAzZmIwYzE5NjAxZWVlZjE4NWUzOSIsInB1YmxpY0tleWNoYWluIjoieHB1YjY2MU15TXdBcVJiY0ZRVnJRcjRRNGtQamFQNEpqV2FmMzlmQlZLalBkSzZvR0JheUU0NkdBbUt6bzVVRFBRZExTTTlEdWZaaVA4ZWF1eTU2WE51SGljQnlTdlpwN0o1d3N5UVZwaTJheHpaIiwiYmxvY2tjaGFpbmlkIjoicnlhbiJ9fQ").encode("utf-8")
logger.info(coincurve.utils.sha256(payload))
sig = privateKey.sign(payload)
logger.info(sig)
logger.info(base64.urlsafe_b64encode(coincurve.ecdsa.serialize_compact(der_to_cdata(sig))))
logger.info(coincurve.utils.bytes_to_hex(coincurve.ecdsa.serialize_compact(der_to_cdata(sig))[:65]))
coincurve.verify_signature(sig, payload,  pubKey)
