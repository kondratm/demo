Test Plan for Web Server



3 general approaches were tested under circumstances of this document:
    1. Authentication mechanism
    2. Legal usage of web server by user (provided by documentation - mail)
    3. Illegal usage of web server by user (incorrect inputs / query params)




General Notes:
    1. Documentation (mail explanation) was used to generate this test plan.
    2. Https is not implemented on server side therefore not tested.
    3. Authorization mechanism is not implemented therefore not tested.
    4. Error codes not provided therefore bugs not opened for pages that return only status codes (404).
    5. Bug’s priorities – P0 (High priority), P1 (Medium priority), P2 (Low priority)
    6. Curl 7.78.0 was used.


Authentication mechanism bugs:

    1. Bug number 1: No username required for authorization (P0)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -vo /dev/null -u'abc:admin' 'http://localhost:8000/players?page=3'

Expected: 

	Response code is 401 Unathorized.

Actual:

	User gets response with players data and bypass authentication mechanism.


			
Legal Usage of Web Server

    1. Bug number 2: Response content shown in incorrect format (P1)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=3'

Expected: 

	Response header Content-Type is application/json (same as response format itself, this is mentioned in documentation).

Actual:

	Response header Content-Type is text/plain, therefore would not be parsed correctly at client.



    2. Bug number 3: Number of JSON objects at response is incorrect (P0)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=4'
    b) First object’s id is 150.
    c) Execute next command in terminal: 
       curl -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=3'


Expected: 

	Last JSON object id for page 3 is 149.

Actual:

	Last JSON object id for page 3 is 148, therefore one object is missed and user can’t read it (same for all pages).


    3. Bug number 4: Empty Name values of JSON objects (P0)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=4'
    b) Observe response for empty values at Name keys


Expected: 

	No empty values should exist.

Actual:

	Some JSON objects at response have empty Name values.

       
       
    4. Bug number 5: HTTP request methods are not implemented correctly but GET method (P1)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -X DELETE -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=3'


Expected: 

	Delete request method is not implemented correctly, response code 400 should return with suitable error message (or code 200 with error message).

Actual:

	Content of page 3 with all JSON objects return.
Illegal Usage of Web Server

    1. Bug number 6: No correct response code / validation for incorrect type of query params / exceeded buffer for page number. (P0)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=\"3\"'
    b) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=asd'
    c) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=12.2'
    d) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=99999999999999999999'

Expected: 

	Response code is 400 for all requests.

Actual:

	Response code is 418 for all requests.


    2. Bug number 6: No correct error message for incorrect type of query params / exceeded buffer for page number (P0)

Steps to reproduce:

    a) Execute next command in terminal: 
       curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=\"3\"'
    b) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=asd'
    c) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=12.2'
    d) curl -vo /dev/null -u'admin:admin' -H'Accept:application/json' 'http://localhost:8000/players?page=99999999999999999999'

Expected: 

	Meaningful error message at response regarding incorrect input/request parameteres.

Actual:

	“I am a teapot [TODO change]“ response with TODO.
