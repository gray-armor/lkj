VERSION_FILE=VERSION
VERSION=`cat $(VERSION_FILE) | sed 's/^ *\| */$//'`

install:
	python setup.py sdist
	pip install dist/lkj-${VERSION}.tar.gz

clean:
	pip uninstall lkj -y
	rm -rf dist lkj.egg-info
