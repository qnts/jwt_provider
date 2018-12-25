# jwt_provider

This module is meant for developers, building endpoints for web and mobile app.

## Prerequisites

This module require `pyjwt` and `simplejson` to be installed. Run:

```
pip3 install pyjwt
pip3 install simplejson
```

If you run odoo in docker, remember to login to bash in docker container and run the above command.

## Installation

Download or clone this repo and move it to odoo addons dir. Install it via odoo just like a normal module. This module require zero confiugration, just change the `SECRET_CODE` in `validator.py` for your own.

## Developer

Developers might need to verify jwt token inside private endpoints:

```python
http_method, body, headers, token = jwt_http.parse_request()
result = validator.verify_token(token)
if not result['status']:
    return jwt_http.errcode(code=result['code'], message=result['message'])
```

## To Do

- Add an interface to store secret key (instead of hard-coding the key) and ability to pick a hashing algorithm (currently we use HMACSHA256).

## Endpoints

For private endpoints, include your jwt token in the header like this:

```
Authorization: Bearer your_token
```
1. Login
  ```
  POST /api/login
  ```
  Request payload:
  ```
  email=user@odoo.com&
  password=password
  ```
  Response:

  `400`: Incorect login

  `200`: OK
  ```json
  {
    "data": {
        "user": {
            "id": 8,
            "login": "user@odoo.com",
            "company_id": [
                1,
                "My Company"
            ],
            "name": "John"
        },
        "token": "generated_token"
    },
    "success": true,
    "message": null
  }
  ```
 
2. Register
  ```
  POST api/register
  ```
  Require: Free signup setting is ON (as well as enabled `auth_signup`).

  On success, response an access token as well.

  Request payload:
  ```
  email=user@odoo.com&
  password=password&
  name=Your%sName
  ```
  Response:

  `400`: User input invalid, message might be one of:

    Invalid email address
    Name cannot be empty
    Password cannot be empty
    Email address already existed

  `501`: Signup is disabled

  `200`: OK
  ```json
  {
    "data": {
        "user": {
            "id": 8,
            "login": "user@odoo.com",
            "company_id": [
                1,
                "My Company"
            ],
            "name": "John"
        },
        "token": "generated_token"
    },
    "success": true,
    "message": null
  }
  ```

3. My profile
  ```
  ANY /api/me
  ```
  Response:

  `498`: Token invalid or expired

  `200`: OK, return user object
  ```json
  {
    "data": null,
    "success": {
        "company_id": [
            1,
            "My Company"
        ],
        "avatar": "http://yourwebsite.com/web/avatar/8",
        "name": "Join",
        "id": 8,
        "email": "user@odoo.com"
    },
    "message": null
  }
  ```

4. Logout
  ```
  ANY /api/logout
  ```
  Response:

  `498`: Token invalid or expired

  `200`: OK, log the user out