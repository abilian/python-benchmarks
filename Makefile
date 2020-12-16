clean:
	rm -f **/*.pyc
	find . -type d -empty -delete

format:
	docformatter -i *.py
	black *.py

