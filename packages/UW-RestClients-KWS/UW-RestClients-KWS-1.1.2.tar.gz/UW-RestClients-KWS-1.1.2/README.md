# REST client for the UW Key Web Service

[![Build Status](https://github.com/uw-it-aca/uw-restclients-kws/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/uw-restclients-kws/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-restclients-kws/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/uw-restclients-kws?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-kws.svg)](https://pypi.python.org/pypi/uw-restclients-kws)
![Python versions](https://img.shields.io/badge/python-3.10-blue.svg)

Installation:

    pip install UW-RestClients-KWS

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_KWS_DAO_CLASS='Live'

    # Paths to cert and key files
    RESTCLIENTS_KWS_CERT_FILE='/path/to/cert'
    RESTCLIENTS_KWS_KEY_FILE='/path/to/key'

    # Key Web Service hostname (eval or production)
    RESTCLIENTS_KWS_HOST='https://ws.admin.washington.edu'

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_KWS_TIMEOUT=5
    RESTCLIENTS_KWS_POOL_SIZE=10
