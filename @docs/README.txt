PYTHON

1. Python 2.7.x: from
   https://www.python.org/downloads/

2. Google App Engine SDK for Python: from
   https://cloud.google.com/appengine/downloads

3. Dependencies: run
   python -m pip install -r @docs/requirements.txt -t lib

4. Some files may be deleted from the dependencies. Eg: test folders.


SASS

1. Rubby 2.2.x: from
   http://rubyinstaller.org/downloads/

2. Sass 3.4.x: run
   gem install sass

3. Compile automatically: run
   sass --style=compressed --sourcemap=none --nocache --watch resources/css/main.scss:resources/css/main.min.css
