from webob import Request, Response
from typing import Callable, Dict
from parse import parse


class API:

    def __init__(self):
        self.routes: Dict[str,Callable] = {}

    def __call__(self, environ: dict, start_response: Callable):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)
    
    def find_handler(self, request_path: str):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None


    def handle_request(self, request: Request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response


    
    def route(self, path):
        assert path not in self.routes, "Such route already exists."

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def default_response(self, response: Response):
        response.status_code = 404
        response.text = "Not found."