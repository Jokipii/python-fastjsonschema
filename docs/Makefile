.PHONY: all
all: sphinx

BUILDDIR=../../python-fastjsonschema-doc
SPHINXOPTS=-W -d $(BUILDDIR)/doctrees .

.PHONY: sphinx
sphinx:
	sphinx-build -b html $(SPHINXOPTS) $(BUILDDIR)/html

clean:
	rm -rf build
