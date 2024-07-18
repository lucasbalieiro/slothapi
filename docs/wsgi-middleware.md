# Exploring WSGI Middleware

Well then, this is the last theoretical part of this project. In the next sessions, we will start our framework, creating its routing logic. So let's go!


In this section, we will delve into WSGI middleware, which is a powerful feature that allows you to process requests and responses in a modular and reusable manner. Middleware can be used to add functionality such as authentication, logging, or session management to your WSGI applications.

## What is WSGI Middleware?

WSGI middleware is a callable that sits between the server and the application, processing requests and responses. Middleware can modify the `environ` dictionary, the response, or both. Middleware functions can be stacked, allowing you to compose complex behaviors from simple components.

 ![Image of the middleware flow](./assets/images/wsgi-middleware.png "Middleware on the webserver flow")

## Creating a Simple Middleware

Let's start by creating a simple middleware that logs each incoming request. We'll create a new file called `middleware.py` and define our middleware there:

```python
# middleware.py

def simple_middleware(app):
    def wrapped_app(environ, start_response):
        # Log the request path
        print(f"Request path: {environ['PATH_INFO']}")
        
        # Call the original application
        return app(environ, start_response)
    
    return wrapped_app
```

This middleware wraps the original WSGI application, logs the request path, and then calls the original application.

## Using Middleware with Your Application

To use the middleware with your WSGI application, you need to wrap your application with the middleware function. Update your `app.py` to include the middleware:

```python
# app.py

from middleware import simple_middleware

def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Hello, World!"]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    app = simple_middleware(simple_app)  # Wrap the app with middleware
    server = make_server('localhost', 8000, app)
    print("Serving on http://localhost:8000")
    server.serve_forever()
```

With this setup, every request to your application will be logged by the middleware before being processed by `simple_app`.

## Adding More Middleware

You can stack multiple middleware functions to add more functionality. For example, let's create another middleware to add a custom header to the response. Add the following code to `middleware.py`:

```python
# middleware.py

def simple_middleware(app):
    def wrapped_app(environ, start_response):
        # Log the request path
        print(f"Request path: {environ['PATH_INFO']}")
        
        # Call the original application
        return app(environ, start_response)
    
    return wrapped_app

def header_middleware(app):
    def wrapped_app(environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-Custom-Header', 'MyValue'))
            return start_response(status, headers, exc_info)
        
        return app(environ, custom_start_response)
    
    return wrapped_app
```

Update your `app.py` to use both middleware functions:

```python
# app.py

from middleware import simple_middleware, header_middleware

def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Hello, World!"]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    app = simple_middleware(simple_app)  # First middleware
    app = header_middleware(app)  # Second middleware
    server = make_server('localhost', 8000, app)
    print("Serving on http://localhost:8000")
    server.serve_forever()
```

Now, your application logs each request and adds a custom header to the response.

## Practical Use Cases for Middleware

Middleware can be used for various purposes, including:

- **Logging**: Log incoming requests, responses, and errors.
- **Authentication**: Check user credentials and manage sessions.
- **Compression**: Compress response data to reduce bandwidth usage.
- **Caching**: Store and retrieve cached responses to improve performance.
- **Security**: Implement security features like input validation and output escaping.

## Next Step:
[Starting the SlothAPI: Requests and routing](./requests-and_routing.md)
