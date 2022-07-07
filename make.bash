cd cv-source

pdflatex OlivieroNardi.tex
bibtex OlivieroNardi.aux
pdflatex OlivieroNardi.tex
pdflatex OlivieroNardi.tex
mv OlivieroNardi.pdf ../files/OlivieroNardiCV.pdf
cd ..

python3 update-pubs.py