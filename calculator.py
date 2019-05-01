#Tim Pauley
#Python 230, Assignment 04
#Date: April 29, 2019

#Wsgi Calculator


""" 
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import os
import traceback
import operator
from functools import reduce

def add(*args):
    args = [int(num) for num in args]
    return str(reduce(operator.add, args))


def multiply(*args):
    args = [int(num) for num in args]
    return str(reduce(operator.mul, args))


def subtract(*args):
    args = [int(num) for num in args]
    return str(reduce(operator.sub, args))


def divide(*args):
    args = [int(num) for num in args]
    return str(reduce(operator.truediv, args))

# TODO: Add functions for handling more arithmetic operations.

def index():
    """
    Landing page instructions for how to use the calculator site
    """
    body="""
    <html>
        <div class="container"> 
            <body>
                <h1 id="Foo">Tim Pauley's Calculator Website</h1>           
                <h5>On this site: you can add, multiply, subtract, and divide numbers 
                based on what you type in the URL path.<br>
                </h5>
                <a href=http://localhost:8080/add/3/9>http://localhost:8080/add/3/9</a>
            </body>
        </div>
                <script>
    $(document).ready(function() {
    var f = document.getElementById('Foo');
    setInterval(function() {
        f.style.display = (f.style.display == 'none' ? '' : 'none');
    }, 1000); 
}); </script>
    </html>"""

    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    operations = {
        "" : index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    try:
        func = operations[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1> Not Found</h>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h>"
        print(traceback.format_exc())
    # except ZeroDivisionError:
    #     status = "406 Not Acceptable"
    #     body = "<h1> Cannot divide by zero.</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    port = int(os.environ.get("PORT", 8080))

    srv = make_server('0.0.0.0', port, application)
    #srv = make_server('localhost', 8080, application)
    srv.serve_forever()
