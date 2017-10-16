# campy

## Python

1. Python 2.7.x: from
   > https://www.python.org/downloads/

2. Google App Engine SDK for Python: from
   > https://cloud.google.com/appengine/downloads

3. Dependencies: run
   > `python -m pip install -r @docs/requirements.txt -t src/lib`

   and delete these files and folders
   ```
   /src/lib/*-info
   /src/lib/_markerlib
   /src/lib/easy_install.py
   /src/lib/markupsafe/tests.py
   /src/lib/pyramid/tests
   /src/lib/pyramid_jinja2/demo/tests.py
   /src/lib/pyramid_jinja2/tests
   /src/lib/repoze/lru/tests.py
   /src/lib/setuptools
   /src/lib/translationstring/tests
   /src/lib/venusian/tests
   /src/lib/zope/deprecation/tests.py
   /src/lib/zope/interface/common/tests
   /src/lib/zope/interface/tests
   ```

## Sass

1. Rubby 2.2.x: from
   > http://rubyinstaller.org/downloads/

2. Sass 3.4.x: run
   > `gem install sass`

3. Compile automatically: run
   > `sass --style=compressed --sourcemap=none --nocache --watch src/resources/css/main.scss:src/resources/css/main.min.css`
