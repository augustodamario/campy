#coding:utf-8
from pyramid.config import Configurator
from sys import modules


# Fixes bug in pyramid_jinja2 library
modules["__main__"]= globals()

config= Configurator()
config.include("pyramid_jinja2")
config.add_jinja2_renderer(".html")
config.add_jinja2_search_path("templates", name=".html")
config.add_route("home", "/")
config.scan("campy")

app= config.make_wsgi_app()
