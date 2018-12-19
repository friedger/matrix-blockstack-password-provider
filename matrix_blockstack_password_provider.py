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

logger = logging.getLogger("synapse.authprovider")


class BlockstackPasswordProvider(object):
    __version__ = "0.1"

    def __init__(self, config, account_handler):
        self.account_handler = account_handler
        self.blockstack_node = config.blockstack_node

    @defer.inlineCallbacks
    def check_password(self, user_id, password):
		if not password:
			defer.returnValue(False)
		blockstack_id = user_id.split(":", 1)[0][1:]
		app = password.split("|")[1]
		r = requests.get(self.blockstack_node + '/v1/names/' + blockstack_id)
		if not r.status_code == requests.codes.ok:
			defer.returnValue(False)
		names_response = r.json()
		logger.info("names %s", names_response)
		z = blockstack_zones.parse_zone_file(names_response["zonefile"])
		logger.info("zone %s", z)
		r = requests.get(z["uri"][0]["target"])
		if not r.status_code == requests.codes.ok:
			defer.returnValue(False)
		zone_file_response = r.json()
		logger.info("zone %s", zone_file_response)
		appBucket = zone_file_response[0]["decodedToken"]["payload"]["claim"]["apps"][app]
		r = requests.get(appBucket+"mxid.json")
		if not r.status_code == requests.codes.ok:
			defer.returnValue(False)
		mxid_response = r.text
		logger.info("Response for user %s: %s", user_id, mxid_response)
		if mxid_response == "mychallengefromserver":
			if (yield self.account_handler.check_user_exists(user_id)):
				logger.info("User %s exists, logging in", user_id)
				defer.returnValue(True)
			else:
				try:
					user_id, access_token = (yield self.account_handler.register(localpart=blockstack_id))
					logger.info("User %s created, logging in",blockstack_id)
					defer.returnValue(True)
				except:
					logger.warning("User %s not created", blockstack_id)
					defer.returnValue(False)
		else:
			logger.warning("Wrong password for user %s", blockstack_id)
			defer.returnValue(False)

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
