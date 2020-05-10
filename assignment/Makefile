# stolen from this: https://github.com/martinbjeldbak/CV/blob/master/Makefile
# I am probably not using the full potential of latexmk yet
# looking into it, and using make every time for now

root = synopsis
compileoptions = -pdf -shell-escape

.PHONY: $(root).pdf all clean

all: $(root).pdf

$(root).pdf: $(root).tex
	latexmk $(compileoptions) $(root)

watch: clean
	latexmk $(compileoptions) -pvc $(root)

clean:
	latexmk -c

view:
	open $(root).pdf
