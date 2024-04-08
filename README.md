# API Documentation

This document provides an overview of the API endpoints available in this project.

## Endpoints

| Endpoint                                 | Description                                           |
|------------------------------------------|-------------------------------------------------------|
| '`admin/`'                               | Admin panel                                           |
| '`swagger/`'                             | Swagger Document API endpoints, including parameters, request bodies, and response schemas.|
| '`redoc/`'                               | Redoc Document API endpoints, including parameters, request bodies, and response schemas.|
| '`api/v1/register/`'                    | Register a new user                                   |
| '`api/v1/login/`'                       | User login                                            |
| '`api/v1/logout/`'                      | User logout                                           |
| '`api/v1/user/retrieve/`'               | Retrieve authenticated user profile                   |
| '`api/v1/user/update/`'                 | Update authenticated user profile                     |

## Notes

- The `api/v1/user/retrieve/` endpoint is used for retrieving the authenticated user's profile.
- The `api/v1/user/update/` endpoint is used for updating the authenticated user's profile.

This documentation is intended to provide a clear overview of the API's capabilities and how to interact with it.<br> 
For more detailed information about each endpoint, including required parameters and response formats, please refer <br>
to the Swagger or Redoc documentation provided by the API.<br>

## Postman Collection

For the convenience of testing API endpoints, i provide a Postman Collection. 
This allows users to easily import and use a set of requests for testing various API functions.

### How to Use the Postman Collection

1. Download the Postman Collection file for this project.
2. Open Postman and go to the "Collections" section.
3. Click on the "Import" button and select the downloaded file.
4. After importing, you will see all the available endpoints in your Postman.

### Examples of Requests

The Postman Collection includes example requests for the following endpoints:

- Register a new user (`api/v1/register/`)
- User login (`api/v1/login/`)
- User logout (`api/v1/logout/`)
- Retrieve authenticated user profile (`api/v1/user/retrieve/`)
- Update authenticated user profile (`api/v1/user/update/`)

This allows for quick and efficient testing of API functionality without the need to manually create requests.

### Additional Information

For more information on each endpoint, including required parameters and response formats, please refer to the Swagger or Redoc documentation provided by the API.


### Run Tests:

Execute the following command to run the tests:

``` bash 
./manage pytest
```



## Contributing

telegram: **`@mirbekov0909`** <br>
<br>

email: **`tteest624@gmail.com`** <br>
<br>

email: **`mirbekov1kylych@gmail.com`**








