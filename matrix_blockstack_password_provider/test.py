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
result = []
localpart = "13ibxaRcfKKhrnfu3QPktKVXEjQNU4r4aD".lower()
print pwdProvider.check_password("@" + localpart + ":localhost", "1Maw8BjWgj6MWrBCfupqQuWANthMhefb2v0.7965665230758666|https://matrix.openintents.org|friedger.id")

result = []
localpart = "friedgermuef".lower()
print pwdProvider.check_password("@" + localpart + ":localhost", "1Maw8BjWgj6MWrBCfupqQuWANthMhefb2v0.7965665230758666|friedgermuef would like to login using the active permission. Block ID: 44952862 3D444BD06ADC|SIG_K1_Ki7Wvjed6r8jzyKv8sRmTJJbE3hxPEA1shCMsd5Z3PMW2KqEAc6tTVQLtVddEXjpwNwxD3sQQ4EnNbF1N5TxnWK2PXcEsT")

