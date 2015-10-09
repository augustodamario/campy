PYTHON

1. Python 2.7.x: from
   https://www.python.org/downloads/

2. Google App Engine SDK for Python: from
   https://cloud.google.com/appengine/downloads

3. Dependencies: run
   python -m pip install -r @docs/requirements.txt -t lib

   and delete these files and folders
   /lib/*-info
   /lib/_markerlib
   /lib/easy_install.py
   /lib/markupsafe/tests.py
   /lib/pyramid/tests
   /lib/pyramid_jinja2/demo/tests.py
   /lib/pyramid_jinja2/tests
   /lib/repoze/lru/tests.py
   /lib/setuptools
   /lib/translationstring/tests
   /lib/venusian/tests
   /lib/zope/deprecation/tests.py
   /lib/zope/interface/common/tests
   /lib/zope/interface/tests


SASS

1. Rubby 2.2.x: from
   http://rubyinstaller.org/downloads/

2. Sass 3.4.x: run
   gem install sass

3. Compile automatically: run
   sass --style=compressed --sourcemap=none --nocache --watch resources/css/main.scss:resources/css/main.min.css
