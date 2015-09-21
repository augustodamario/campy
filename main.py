# coding: utf-8
from pyramid.config import Configurator
from sys import modules


# Fixes bug in pyramid_jinja2 library
modules["__main__"] = globals()

config = Configurator(settings={
    "jinja2.variable_start_string": "{=",
    "jinja2.variable_end_string": "=}"
})
config.include("pyramid_jinja2")
config.add_jinja2_renderer(".html")
config.add_jinja2_search_path("templates", name=".html")
config.include("campy.views")

app = config.make_wsgi_app()
