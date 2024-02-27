# krb-oidc-token-exchanger

Flask app for exchanging OIDC access tokens for Kerberos tickets. Utilizes OAuth 2.0 Token Exchange mechanism.

## Configuration

All configuration options are described in the `config-template.yaml` file. Section `basic-auth` is optional.

## Usage

Use docker or run directly:

```sh
python3 oidc2krb/app.py
```

The app will start on `http://localhost:80/`.

### uWSGI

Use the callable `oidc2krb.app:get_app` with uWSGI, e.g.:

```plain
mount = /oidc2krb=oidc2krb.app:get_app
```
