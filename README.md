# matrix-blockstack-password-provider
Matrix Synapse Authentication Provider for Blockstack IDs

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
