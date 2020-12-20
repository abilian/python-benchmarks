env:
	python3.8 -m venv env
	./env/bin/pip install -U pip wheel setuptools
	./env/bin/pip install -r requirements.txt
	echo "Now run 'source ./env/bin/activate.{sh|fish}"

clean:
	rm -f **/*.pyc
	find . -type d -empty -delete

format:
	docformatter -i *.py
	black *.py


push-programs:
	rsync -e ssh -avz programs chai:python-benchmarks/
