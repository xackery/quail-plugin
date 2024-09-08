VERSION ?= 2.2.1

comma := ,
COMMA_VERSION := $(subst .,${comma} ,${VERSION})

.PHONY: test
test:
	@pytest --rootdir=. wce/wce_test.py

build:
	@echo "build: packing and building"
	mkdir -p bin
	-rm -rf bin/*
	cd /src/quail && make build-windows-addon
	cp /src/quail/bin/quail-addon.exe bin/quail.exe
	sed -i 's/"version": (1, 0, 0),/"version": (${COMMA_VERSION}),/' __init__.py
	sed -i 's/"0.0.1"/"${VERSION}"/' common/__init__.py
	sed -i 's/return True  # Build/return False  # Build/' common/__init__.py
	mkdir -p bin/quail-addon
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
	cp bin/quail.exe LICENSE README.md *.py bin/quail-addon
	cp -r auto_load common exporter importer material_panel view_panel bin/quail-addon
	cd bin && zip -r quail-${VERSION}.zip quail-addon
	rm -rf bin/quail-addon
	rm bin/quail.exe
	sed -i 's/"version": (${COMMA_VERSION}),/"version": (1, 0, 0),/' __init__.py
	sed -i 's/return False  # Build/return True  # Build/' common/__init__.py
	sed -i 's/"${VERSION}"/"0.0.1"/' common/__init__.py

build-darwin:
	@echo "build-darwin: packing and building"
	@mkdir -p bin
	cd /src/quail && make build-darwin
	cp /src/quail/bin/quail-darwin quail-darwin