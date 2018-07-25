# jwt_provider
A simple jwt provider for Odoo 11 

# Installation

## Pre-installation

This module require `pyjwt` to be installed. Run:

```
pip3 install pyjwt
```

If you run odoo in docker, remember to login to bash in docker container and run the above command.

## Installation

Download or clone this repo and move it to odoo addons dir. Install it via odoo just like a normal module. This module require zero confiugration, just change the `SECRET_CODE` in `validator.py` for your own.

# Endpoints

All requests to endpoint should have the following headers:
```
Content-type: application/json
```

For private endpoints, include your jwt token in header like this:

```
Authorization: Bearer your_token
```

Your request body should be like this:

```
{
  "params": {
    // "key": value
  }
}
```

Return response:

```
{
    "jsonrpc": "2.0",
    "result": {
        "status": true/false,
        "message": null,
        "data": {
          // data object
          // user: {}
          // token: "token"
        }
    },
    "id": null
}
```

1. Login: post
  ```
  http://odoo.com/api/v1/login
  ```
  ```
  {
    "params": {
      "login": "user@odoo.com",
      "password": "password"
    }
  }
  ```
 
