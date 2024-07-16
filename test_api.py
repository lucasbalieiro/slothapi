import pytest

from api import API


@pytest.fixture
def api():
    return API()

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "HOME"

def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "HOME"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "DUPLICATED HOME"
