export FLASK_APP=server.py

run:
	raml2html ./webapi/docs/apidoc.raml > ./webapp/templates/apidoc.html
	flask run