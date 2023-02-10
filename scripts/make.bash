cd ../cv-source

pdflatex OlivieroNardi.tex
bibtex OlivieroNardi.aux
pdflatex OlivieroNardi.tex
pdflatex OlivieroNardi.tex
mv OlivieroNardi.pdf ../files/OlivieroNardiCV.pdf

cd ..

rm ./files/publications/bib/*

cd ./scripts

python3 update-pubs.py
python3 last-update.py