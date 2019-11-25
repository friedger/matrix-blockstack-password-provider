from matrix_blockstack_password_provider import BlockstackPasswordProvider
from twisted.internet import reactor
import requests

class _BlockstackConfig(object):
    pass

blockstack_config = _BlockstackConfig()
blockstack_config.enabled = False
blockstack_config.blockstack_node = "https://core.blockstack.org"

class AccountHandler(object):
    def check_user_exists(self, name):
        return False

    def register(self, localpart):
        return localpart, "abc"

class Store(object):
    def set_profile_displayname(self, user, name):
        pass
    def set_profile_avatar_url(self, user, url):
        pass

class ProfileHandler(object):
    store = Store()

class HS(object):
    def get_profile_handler(self):
        return ProfileHandler()

ah = AccountHandler()
ah.hs = HS()

pwdProvider = BlockstackPasswordProvider(blockstack_config, ah)

# result = []
# localpart = "13ibxaRcfKKhrnfu3QPktKVXEjQNU4r4aD".lower()
# print(pwdProvider.check_password("@" + localpart + ":localhost", "1Maw8BjWgj6MWrBCfupqQuWANthMhefb2v0.7965665230758666|https://matrix.openintents.org|friedger.id"))
#
# result = []
# localpart = "friedgermuef".lower()
# print(pwdProvider.check_password("@" + localpart + ":localhost", "1Maw8BjWgj6MWrBCfupqQuWANthMhefb2v0.7965665230758666|friedgermuef would like to login using the active permission. Block ID: 44952862 3D444BD06ADC|SIG_K1_Ki7Wvjed6r8jzyKv8sRmTJJbE3hxPEA1shCMsd5Z3PMW2KqEAc6tTVQLtVddEXjpwNwxD3sQQ4EnNbF1N5TxnWK2PXcEsT"))

result = []
localpart = "12Gpr9kYXJJn4fWec4nRVwHLSrrTieeywt".lower()
print(pwdProvider.check_password("@" + localpart + ":localhost", "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJqdGkiOiI3MWI3NWY1Yi0xNDJkLTQxMzQtOGZkYy0zYWUyMWRmZTkzNjAiLCJpYXQiOjE1MzcxNjkxODYsImV4cCI6MTUzOTc2MTE4NSwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjEyR3ByOWtZWEpKbjRmV2VjNG5SVndITFNyclRpZWV5d3QiLCJwcml2YXRlX2tleSI6IjdiMjI2OTc2MjIzYTIyMzEzOTMzMzM2NTM5MzYzNTY2NjMzNzM5NjM2MjYyMzAzNjY0NjMzMjM0MzIzNzY2NjY2MjYzMzczMjMyMzgzOTIyMmMyMjY1NzA2ODY1NmQ2NTcyNjE2YzUwNGIyMjNhMjIzMDMyMzQzMTY1MzY2NjYzMzEzODM0MzAzMDMyMzQzMTY0NjYzNzMzMzMzNTY1NjM2MjY2MzQzMzM0NjY2NDM5MzU2MjY0NjUzMjY2MzIzNTMxNjU2MzM3MzczNjMxMzQzNDM0MzAzMjY2NjUzNTM3NjE2MzYzMzA2MjY2MzQzNjYxMzQyMjJjMjI2MzY5NzA2ODY1NzI1NDY1Nzg3NDIyM2EyMjM5MzkzMTYxMzM2MzM1NjYzOTY2NjI2MzM2MzYzMzY2MzMzMDY0MzgzNzMxMzgzNzMyNjIzODM5MzMzMTYxMzMzMTMyNjUzMjM0NjM2MjM4MzAzNzM1NjQzODY0MzkzNzM1Mzg2MjM3NjEzMDY1NjMzMTM0Mzg2MTM2MzEzMjM2MzIzMjY1MzYzMjYyMzQ2NjY1NjYzNjMzNjMzMTYzNjYzMjMzNjEzMTM3MzM2NTM0NjUzOTMwMzIzMzM5MzQ2NDY1NjEzMTMxMzQzOTYzNjE2NTYxMzMzMzY2MzMzODY2NjIzMTMwMzczNTM0MzU2NDM1MzUzNDM3NjYzNjY2NjMzODMwMzg2MTM2MzIzNjM2MzAzMDMzNjMzNzM5MzMzNzM4MzYzMzM4MzMzNDMyNjEzNjYzMzMzOTM4MzM2MjM5MjIyYzIyNmQ2MTYzMjIzYTIyNjYzODMwMzQ2MjMzMzY2MjY0MzgzMjM2NjQzNTM3MzIzMzYxMzQzOTM4MzczOTYzMzAzMDYzNjQ2MzMzNjYzMDYxNjQzNzY0NjE2MTYyNjE2NDM0MzY2NDMzMzczNjY0MzUzMTYxNjI2NjYzNjYzMTM4MzM2MTM4MzAzNDMwMzgyMjJjMjI3NzYxNzM1Mzc0NzI2OTZlNjcyMjNhNzQ3Mjc1NjU3ZCIsInB1YmxpY19rZXlzIjpbIjAyODcyNmQyMGZhMTI4Yjc1OWViOGIwOWZjY2Y2ODU2ZTQzMjM1YmI5OTkxNjI0OWNmNjNhM2NiMjA0MTY0Y2I4ZSJdLCJwcm9maWxlIjpudWxsLCJ1c2VybmFtZSI6bnVsbCwiY29yZV90b2tlbiI6bnVsbCwiZW1haWwiOiJmcmllZGdlckBnbWFpbC5jb20iLCJwcm9maWxlX3VybCI6Imh0dHBzOi8vZ2FpYS5ibG9ja3N0YWNrLm9yZy9odWIvMTJHcHI5a1lYSkpuNGZXZWM0blJWd0hMU3JyVGllZXl3dC9wcm9maWxlLmpzb24iLCJodWJVcmwiOiJodHRwczovL2h1Yi5ibG9ja3N0YWNrLm9yZyIsInZlcnNpb24iOiIxLjIuMCJ9.QM8wx-EDjZrHk1ubK99divaejN5XAcCn_OkYAiPXQUNtzENUy8ogyrHzB4xC7mwfMckzFsMxEOdzwVW_Xcjqqg"))
