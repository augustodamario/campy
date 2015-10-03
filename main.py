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
config.add_tween("campy.security.session_tween_factory")
config.include("campy.views.system")
config.include("campy.views.ui", route_prefix="/sede/{branch:[a-z]+}")
config.include("campy.views.api", route_prefix="/sede/{branch:[a-z]+}/api")

app = config.make_wsgi_app()
