clean:
	rm -f **/*.pyc
	find . -type d -empty -delete

format:
	docformatter -i *.py
	black .


push:
	rsync -e ssh -avz *.py programs c17:python-benchmarks/

pull-results:
	rsync -e ssh -avz c17:python-benchmarks/result.txt web/


publish:
	make pull-results
	cd web && python publish.py
	rsync -e ssh -avz web/*.html root@bulma:/srv/web/lab.abilian.com/python-benchmarks/

