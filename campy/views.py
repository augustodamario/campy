#coding:utf-8
from pyramid.view import view_config

def includeme(config):
    config.add_route("home", "/")
    config.scan(__name__)

@view_config(route_name="home", renderer="home.html")
def home(request):
    return {"name": "Pepe"}
