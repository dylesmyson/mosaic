install:
	pip install -r requirements.txt
	pip install -e $$PWD

clean:
	rm -i *.mid

demo:
	./bin/mosaic generate 'data/yml/demo.yml'
	./bin/mosaic play 'demo.mid'

test:
	python3 -m unittest discover
