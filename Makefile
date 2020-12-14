install:
	pip install -r requirements.txt
	pip install -e $$PWD

demo:
	python3 bin/generate 'data/yml/demo.yml'
	python3 bin/player 'example.mid'

test:
	python3 -m unittest discover
