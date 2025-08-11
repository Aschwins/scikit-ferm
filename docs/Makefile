SOURCEDIR = source
BUILDDIR = _build
APIDOCDIR = source
PACKAGEDIR = ../skferm

.PHONY: help clean html apidoc serve dev

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  apidoc     to generate API documentation"
	@echo "  serve      to serve the documentation"
	@echo "  dev        to generate API docs and serve with auto-rebuild"
	@echo "  clean      to clean build directory"

clean:
	rm -rf $(BUILDDIR)/*

apidoc:
	sphinx-apidoc -o $(APIDOCDIR) $(PACKAGEDIR) --force --no-toc

html: apidoc
	sphinx-build -b html $(SOURCEDIR) $(BUILDDIR)

serve: html
	@echo "Starting development server..."
	@echo "Documentation will be available at:"
	@echo "  WSL2 IP: http://$$(hostname -I | cut -d' ' -f1):8000"
	@echo "  (VSCode port forwarding: http://localhost:8000 - may not work)"
	@echo ""
	python -m http.server -d $(BUILDDIR) 8000

dev: apidoc
	@echo "Starting development server..."
	@echo "Documentation will be available at:"
	@echo "  WSL2 IP: http://$$(hostname -I | cut -d' ' -f1):8000"
	@echo "  (VSCode port forwarding: http://localhost:8000 - may not work)"
	@echo ""
	sphinx-autobuild $(SOURCEDIR) $(BUILDDIR) --open-browser --watch $(PACKAGEDIR) --host 0.0.0.0 --port 8000
