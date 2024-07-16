from api import API


app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/crud")
class CrudResource:
    def get(self, req, resp):
        resp.text = "R of CRUD Page"

    def post(self, req, resp):
        resp.text = "C of CRUD page"