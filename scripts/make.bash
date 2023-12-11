cd ../cv-source

# Clean
rm Conf.*
rm Jour.*
rm Thes.*
rm Prep.*

pdflatex OlivieroNardi.tex

# Only if nonempty
if [ -s conference.bib ]; then
    bibtex Conf.aux
fi

if [ -s journal.bib ]; then
    bibtex Jour.aux
fi

if [ -s thesis.bib ]; then
    bibtex Thes.aux
fi

if [ -s preprint.bib ]; then
    bibtex Prep.aux
fi

pdflatex OlivieroNardi.tex
pdflatex OlivieroNardi.tex
mv OlivieroNardi.pdf ../files/OlivieroNardiCV.pdf

cd ..

touch ./files/publications/bib/deletemeplease.tmp
rm ./files/publications/bib/*

cd ./scripts

python3 update-pubs.py
python3 last-update.py