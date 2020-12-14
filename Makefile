install:
	pip install -r requirements.txt
	pip install -e $$PWD

clean:
	rm -i *.mid

demo:
	python3 bin/generate 'data/yml/demo.yml'
	python3 bin/player 'demo.mid'

test:
	python3 -m unittest discover
