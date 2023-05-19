cd ../cv-source

pdflatex OlivieroNardi.tex
bibtex Conf.aux
bibtex Prep.aux
pdflatex OlivieroNardi.tex
pdflatex OlivieroNardi.tex
mv OlivieroNardi.pdf ../files/OlivieroNardiCV.pdf

cd ..

touch ./files/publications/bib/deletemeplease.tmp
rm ./files/publications/bib/*

cd ./scripts

python3 update-pubs.py
python3 last-update.py