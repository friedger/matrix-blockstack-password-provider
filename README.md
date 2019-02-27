# matrix-blockstack-password-provider

[Matrix](https://matrix.org) [Synapse](https://github.com/matrix-org/synapse) Authentication Provider for [Blockstack](https://blockstack.org) IDs and [EOS](https://eos.io) account names

## Installation

Use `pip install matrix_blockstack_password_provider` to install the package in your synapse environment

## Configuration

In `homeserver.yaml` edit the `password_provider` section:

```
password_providers:
    - module: "matrix_blockstack_password_provider.BlockstackPasswordProvider"
      config:
        enabled: true
        endpoint: "https://core.blockstack.org"
```

The `endpoint` is optional and defaults to `https://core.blockstack.org`

## Known Homeservers for Blockstack users

- [openintents.modular.im](https://openintents.modular.im)

### Client support for Blockstack

- Currently only [OI Chat](https://chat.openintents.org) supports this type of authentication.
- Client apps need to write a file `mxid.json` into the root of their gaia bucket. The content is the
  challenge received from a [home server auth endpoint](https://auth.openintents.org). Then for authentication, the client needs to send the id address as username and as password a client app generated nonce that was used when requesting the challenge together with the app domain in the format
  `nonce + "|" + appDomain + "|" + blockstackId` . Users can do this manually on a [account management site](https://github.com/friedger/matrix-blockstack-auth).

### Client support for EOS

- Currently only [Diri Chat](https://diri.chat) supports this type of authentication.
- Client apps need to sign the following message:
  `${account.name} would like to login using the ${account.authority} permission. Block ID: ${chainInfo.last_irreversible_block_num} ${chainInfo.last_irreversible_block_id.slice(-12).toUpperCase()}`
  Then for authentication, the client needs to send the account name as username and as password a client app generated nonce that was used when requesting the challenge together with the message and signature in the format
  `nonce + "|" + message + "|" + signature` .
