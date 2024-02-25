SETUP = python3 setup.py

.PHONY: default i test clean all html rst build sdist bdist bdist_egg bdist_wheel install release

default: i

i:
	@(cd src/; python3 -i -c 'import i_got; print("igot %s\n>>> import i_got" % i_got.version.__version__)')

test:
	$(SETUP) test

clean:
	zenity --question
	rm -fr build/ dist/ src/*.egg-info/
	find . | grep __pycache__ | xargs rm -fr
	find . | grep .pyc | xargs rm -f

all: build sdist bdist bdist_egg bdist_wheel

html:
	pandoc README.md > README.html

rst:
	pandoc -s -t rst README.md > README.rst

build:
	$(SETUP) build

sdist:
	$(SETUP) sdist

bdist:
	$(SETUP) bdist

bdist_egg:
	$(SETUP) bdist_egg

bdist_wheel:
	$(SETUP) bdist_wheel

install:
	$(SETUP) install --user --prefix=

release:
	#zenity --question
	$(SETUP) sdist bdist_wheel
	echo 'Upload new version to PyPI using:'
	echo '	twine upload --sign dist/igot-VERSION.tar.gz dist/i_got-VERSION-py3-none-any.whl'