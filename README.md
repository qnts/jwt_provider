# jwt_provider

A simple jwt provider for Odoo 11.

This module is in development. Any contribution is welcome.

# Installation

## Prerequisites

This module require `pyjwt` to be installed. Run:

```
pip3 install pyjwt
```

If you run odoo in docker, remember to login to bash in docker container and run the above command.

## Installation

Download or clone this repo and move it to odoo addons dir. Install it via odoo just like a normal module. This module require zero confiugration, just change the `SECRET_CODE` in `validator.py` for your own.

## To Do

- Add an interface to store secret key (instead of hard-coding the key) and ability to pick a hashing algorithm (currently we use HMACSHA256).

# Endpoints

All requests to endpoints MUST USE `POST` and have the following headers:
```
Content-type: application/json
```

For private endpoints, include your jwt token in the header like this:

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

1. Login
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
 
2. Register
  
  Require: Free signup setting is ON.
  ```
  http://odoo.com/api/v1/register
  ```
  ```
  {
    "params": {
      "login": "user@odoo.com",
      "password": "password",
      "name": "Jack"
    }
  }
  ```

  On success, return an access token and a simplified user object.

3. My profile
  ```
  http://odoo.com/api/v1/me
  ```
  Body: empty json object
  ```
  {}
  ```
  On success, return full user object (without sensitive data like password)

4. Logout
  ```
  http://odoo.com/api/v1/logout
  ```
  Body: empty json object
  ```
  {}
  ```

5. Coming soon...