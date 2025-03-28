#!/bin/bash

# Function to extract all 'max-width: <number>px' values from a CSS file
extract_css_max_widths() {
  local file="$1"
  grep -oP '@media screen and \(max-width:\s*\K\d+(?=px\))' "$file"
}

# Function to extract 'min-width' values from a CSS file
extract_css_min_widths() {
  local file="$1"
  grep -oP '@media screen and \(min-width:\s*\K\d+(?=px\))' "$file"
}

# Function to extract all 'max-width' values from a JavaScript file
extract_js_max_widths() {
  local file="$1"
  grep -oP 'max-width:\s*\K\d+(?=px)' "$file"
}

# Extract max-width values from CSS and JavaScript files
css_max_widths=($(extract_css_max_widths "../oli-style.css"))
css_min_widths=($(extract_css_min_widths "../oli-style.css"))
js_max_widths=($(extract_js_max_widths "../oli-script.js"))

# Check if any max-width values were found in CSS
if [ ${#css_max_widths[@]} -eq 0 ]; then
  echo "Error: No max-width values found in oli-style.css."
  exit 1
fi

# Check if any min-width values were found in CSS
if [ ${#css_min_widths[@]} -eq 0 ]; then
  echo "Error: No min-width values found in oli-style.css."
  exit 1
fi

# Check if any max-width values were found in JavaScript
if [ ${#js_max_widths[@]} -eq 0 ]; then
  echo "Error: No max-width values found in oli-script.js."
  exit 1
fi

# Ensure all CSS max-width values are the same
first_css_value="${css_max_widths[0]}"
for value in "${css_max_widths[@]}"; do
  if [ "$value" -ne "$first_css_value" ]; then
    echo "Error: Inconsistent max-width values found in oli-style.css."
    exit 1
  fi
done

# Ensure that each min-width is exactly 1 pixel greater than the preceding max-width
for ((i = 0; i < ${#css_min_widths[@]}; i++)); do
  if [ "${css_min_widths[$i]}" -ne "$((css_max_widths[0] + 1))" ]; then
    echo "Error: In oli-style.css, min-width (${css_min_widths[$i]}px) does not equal max-width (${max_widths[0]}px) + 1."
    exit 1
  fi
done

# Compare CSS and JavaScript max-width values
for js_value in "${js_max_widths[@]}"; do
  if [ "$js_value" -ne "$first_css_value" ]; then
    echo "Error: Mismatch between CSS and JavaScript max-width values (oli-style.css: $first_css_value, oli-script.js: $js_value)."
    exit 1
  fi
done

echo "All max-width values are consistent and match between oli-style.css and oli-script.js"


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