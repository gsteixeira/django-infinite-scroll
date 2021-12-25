
STATIC_DIR := infscroll/static

default:
	# build the package
	python3 -m build && twine check dist/*

static: $(STATIC_DIR)/js/scroll.ts $(STATIC_DIR)/css/scroll.css
	# compile .ts and compress js and css files
	yui-compressor $(STATIC_DIR)/css/scroll.css > $(STATIC_DIR)/css/scroll.min.css
	tsc --outFile $(STATIC_DIR)/js/scroll.js $(STATIC_DIR)/js/scroll.ts
	yui-compressor $(STATIC_DIR)/js/scroll.js > $(STATIC_DIR)/js/scroll.min.js
	
test:
	# test it
	python3 example/app/manage.py test
