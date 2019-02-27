# -*- coding: utf-8 -*-
#
# Blockstack Authentication module for Matrix synapse
# Copyright (C) 2018 Friedger Müffke
#
# Based on  Zjemm/Matrix-Synapse-mysql-password-provider
# Copyright (C) 2018 Eelke Smit
# https://sjemm.net
#
# Based on juju2143/matrix-synapse-smf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from twisted.internet import defer
import blockstack_zones
import logging
import requests
import traceback
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("synapse.blockstackpwds")


class BlockstackPasswordProvider(object):
    __version__ = "0.6.1"

    def __init__(self, config, account_handler):
        self.account_handler = account_handler
        self.blockstack_node = config.blockstack_node

    @defer.inlineCallbacks
    def checkWhiteListedAppsInProfile(self, app, claim):
        # find status for the app domain via profile
        # currently there is no chat profile define
        # therefore, use chat.openintents.org for now.
        oichatBucket = claim["apps"]["https://chat.openintents.org"]
        r = requests.get(oichatBucket+"mxconf.json")

        is_user_app = false
        if r.status_code == requests.codes.ok:
            try:
                mxconf_response = r.json()
                if mxconf_response.get('userapps'):
                    for user_app in mxconf_response['userapps']:
                        if user_app == app:
                            is_user_app = true
            except Exception:
                pass
        defer.returnValue(is_user_app)

    @defer.inlineCallbacks
    def updateProfileFrom(self, claim, blockstack_id, id_address):
        try:
            store = yield self.account_handler.hs.get_profile_handler().store
            name = claim["name"]
            logger.info("User name set to %s", name)
            yield store.set_profile_displayname(id_address, name)
            avatar = claim["image"][0]["contentUrl"]
            logger.info("User avatar set to %s", avatar)
            yield store.set_profile_avatar_url(id_address, avatar)
        except Exception as err:
            logger.warn("failed to update profile (%s)", err)

    def getUserAppAddress(self, gaia_url):
        url_parts = gaia_url.split("/")
        if (url_parts > 2):
            user_app_address = url_parts[len(url_parts) - 2]
            return user_app_address.lower()
        else:
            return ""

    @defer.inlineCallbacks
    def check_password_blockstack(self, user_id, password, localpart):
        id_address = localpart

        pwd_parts = password.split("|")
        txid = pwd_parts[0]
        app = pwd_parts[1]
        blockstack_id = pwd_parts[2]

        r = requests.get(self.blockstack_node + '/v1/names/' + blockstack_id)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid blockstack name")
            defer.returnValue(False)
        names_response = r.json()

        z = blockstack_zones.parse_zone_file(names_response["zonefile"])

        r = requests.get(z["uri"][0]["target"])
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid profile url")
            defer.returnValue(False)
        zone_file_response = r.json()
        claim = zone_file_response[0]["decodedToken"]["payload"]["claim"]

        account_type = -1
        if localpart == blockstack_id:
            account_type = 0
        elif localpart == names_response["address"].lower():
            account_type = 1
        elif claim["apps"].get(app) and localpart == self.getUserAppAddress(claim["apps"][app]):
            account_type = 2

        if (account_type < 0):
            logger.debug("localpart does not belong to user")
            defer.returnValue(False)


        challengeUrl = "http://auth.openintents.org/c/" + txid
        r = requests.get(challengeUrl)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid txid")
            defer.returnValue(False)
        challenge_text = r.json()["challenge"]
        logger.info("Challenge for user %s: %s", user_id, challenge_text)

        responseUrl = claim["apps"][app] + "mxid.json"
        r = requests.get(responseUrl)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid mxid.json url")
            defer.returnValue(False)
        mxid_response = r.text
        logger.info("Response for user %s: %s", user_id, mxid_response)

        if mxid_response == challenge_text:
            if (yield self.account_handler.check_user_exists(user_id)):
                logger.info("User %s exists, logging in", localpart)
                self.updateProfileFrom(claim, blockstack_id, localpart)
                defer.returnValue(True)
            else:
                try:
                    user_id, access_token = (yield self.account_handler.register(localpart=localpart))
                    logger.info("User %s created, logging in", localpart)
                    self.updateProfileFrom(claim, blockstack_id, localpart)
                    defer.returnValue(True)
                except Exception as err:
                    logger.warning("User %s not created (%s)",
                                   localpart, err)
                    defer.returnValue(False)
        else:
            logger.warning("Wrong password for user %s", localpart)
            defer.returnValue(False)

    @defer.inlineCallbacks
    def check_password_scatter(self, user_id, password, localpart):
        accountName = localpart

        pwd_parts = password.split("|")
        txid = pwd_parts[0]
        message = pwd_parts[1]
        signature = pwd_parts[2]
        try:
            r = requests.post('https://auth.diri.chat/login', json={"message": message, "signature": signature}, headers={"Content-Type":"application/json"})
        except Exception as err:
            r = requests.post('http://auth.diri.chat/login', json={"message": message, "signature": signature}, headers={"Content-Type":"application/json"})
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid signature" + r.text)
            defer.returnValue(False)
        auth_response = r.json()
        if (auth_response['authenticated']):
            if (yield self.account_handler.check_user_exists(user_id)):
                logger.info("User %s exists, logging in", localpart)
                defer.returnValue(True)
            else:
                try:
                    user_id, access_token = (yield self.account_handler.register(localpart=localpart))
                    logger.info("User %s created, logging in", localpart)
                    defer.returnValue(True)
                except Exception as err:
                    logger.warning("User %s not created (%s)",
                                   localpart, err)
                    defer.returnValue(False)
        else:
            logger.warning("Wrong password for user %s", localpart)
            defer.returnValue(False)

    @defer.inlineCallbacks
    def check_password(self, user_id, password):
        logger.info("check password")
        if not password:
            logger.debug("no password provided")
            defer.returnValue(False)

        localpart = user_id.split(":", 1)[0][1:]
        if (len(localpart) == 12):
          result = yield self.check_password_scatter(user_id, password, localpart)
          defer.returnValue(result)
        else:
          result = yield self.check_password_blockstack(user_id, password, localpart)
          defer.returnValue(result)

    @staticmethod
    def parse_config(config):
        class _BlockstackConfig(object):
            pass
        blockstack_config = _BlockstackConfig()
        blockstack_config.enabled = config.get("enabled", False)
        blockstack_config.blockstack_node = config.get(
            "blockstack_node", "https://core.blockstack.org")
        return blockstack_config

    def cleanup(self):
        pass
