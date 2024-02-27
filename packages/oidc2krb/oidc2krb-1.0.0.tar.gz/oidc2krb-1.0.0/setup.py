import setuptools

setuptools.setup(
    name="oidc2krb",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/oidc2krb.git",
    description="Flask app for exchanging OIDC access tokens for Kerberos tickets",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "setuptools",
        "certifi==2023.7.22",
        "charset-normalizer~=3.0",
        "click~=8.1",
        "Command==0.1.0",
        "Flask~=2.2",
        "Flask-HTTPAuth~=4.7",
        "idna~=3.4",
        "itsdangerous~=2.1",
        "Jinja2~=3.1",
        "MarkupSafe~=2.1",
        "PyYAML~=6.0",
        "requests~=2.28",
        "urllib3~=2.0",
        "Werkzeug~=2.2",
    ],
)
