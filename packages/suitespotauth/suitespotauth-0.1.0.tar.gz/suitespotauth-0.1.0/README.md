# SuiteSpot Auth

## Introduction
This package is a light wrapper for the SuiteSpot authentication API to provide easy generation of an access token to be used in SuiteSpot data API calls.

Disclaimer: This package is unofficial and is not affiliated with SuiteSpot. The official SuiteSpot authentication API docs can be found at: https://auth.suitespot.io/api#/.

Suitespot data API requests require Bearer Authorization including an access token. This package provides an abstraction layer to easily generate an access token.

## Installation
```shell
$ pip install suitespotauth
```

## Usage
1. Set your SuiteSpot credentials (username and password)
```shell
$ suitespotauth-configure
```

2. In your Python program, import the authenticator class
```python
from suitespotauth import SuiteSpotAuth
```

3. Create a class instance
```python
# Optionally, provide a name string variable to the instantiation. This is stored in the SuiteSpot API token object.
auth = SuiteSpotAuth()
```

4. Use the `access_token` attribute in your data API request header
```python
"Authorization": f"Bearer {auth.access_token}"
```

Official SuiteSpot data API docs should be retrieved directly from your SuiteSpot representative.