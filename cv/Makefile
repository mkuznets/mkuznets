READMES = $(patsubst cv%.yaml,README%.md,$(wildcard cv*.yaml))
MDS = $(patsubst cv%.yaml,cv%.md,$(wildcard cv*.yaml))
TEXS = $(patsubst %.md,%.tex,$(MDS))
PDFS = $(patsubst %.tex,%.pdf,$(TEXS))

.PHONY: all-docker
all-docker:
	docker build --quiet -f scripts/Dockerfile scripts -t cv:latest
	docker run --rm -it --user="$(shell id --user):$(shell id --group)" -v ${PWD}:/cv cv:latest make all

.PHONY: all
all: markdown pdf clean

.PHONY: markdown
markdown: $(READMES)

README%md : cv%md
	cp "$^" "$@"

%.md : %.yaml
	python scripts/build.py markdown -i "$^" -o "$@" -t templates/cv.md

.PHONY: latex
latex: $(TEXS)

%.tex : %.md
	grep -v 'Download PDF' $^ \
	  | pandoc --from=gfm --to=latex --template=templates/cv.tex - > $@

.PHONY: pdf
pdf: $(PDFS)

%.pdf : %.tex
	latexmk -pdf -pdflatex="pdflatex -halt-on-error" "$^"
	latexmk -c "$^"

.PHONY: clean
clean:
	rm -f cv*.md cv*.tex

.PHONY: distclean
distclean: clean
	rm -f README* *.pdf
