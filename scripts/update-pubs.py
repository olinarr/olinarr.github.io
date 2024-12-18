import re
import os

data = {}
with open("../cv-source/conference.bib", "r") as file:
	data["pubs"] = file.read()

with open("../cv-source/journal.bib", "r") as file:
	data["pubs"] += file.read()

with open("../cv-source/thesis.bib", "r") as file:
	data["pubs"] += file.read()

with open("../cv-source/preprint.bib", "r") as file:
	data["preprints"] = file.read()


entries = {"pubs": [], "preprints": []}
for key in ("pubs", "preprints"):
	curr = ""
	mode = "eating"
	for char in data[key]:
		if mode == "eating":
			if char in {"}", "\n"} and curr[-1] == "}":
				curr += "\n}"
				entries[key].append(curr)
				curr = ""
				mode = "waiting"
			else:
				curr += char
		else:
			if char == "@":
				curr = "@"
				mode = "eating"

def month_gt(m1, m2):
	row = ["january", "february", "march", "april", "may", "june", "july", "september", "october", "november", "december"]
	return row.index(m1.lower()) < row.index(m2.lower())

eprints = {}
with open("../files/publications/eprints.txt", "r") as file:
	data = file.read()
	if data:
		for row in data.split("\n"):
			name, link, eprintType = row.split(" ")
			if link == "local":
				link = "./files/publications/full-versions/" + name + ".pdf"
			assert name not in eprints
			eprints[name] = (link, eprintType)

dois = {}
with open("../files/publications/dois.txt", "r") as file:
	data = file.read()
	if data:
		for row in data.split("\n"):
			name, doi = row.split(" ")
			assert name not in dois
			dois[name] = doi

links = {}
with open("../files/publications/links.txt", "r") as file:
	data = file.read()
	if data:
		for row in data.split("\n"):
			name, link = row.split(" ")
			assert name not in links
			links[name] = link

codes = {}
with open("../files/publications/codes.txt", "r") as file:
	data = file.read()
	if data:
		for row in data.split("\n"):
			name, code = row.split(" ")
			assert name not in codes
			codes[name] = code

class Entry:
	def __init__(self, entry, isPreprint):


		self.the_type = None
		self.file_name = None
		self.author_surnames = None
		self.authors = None
		self.school = None
		self.note = None
		self.conference = None
		self.publisher = None
		self.month = None
		self.year = None
		self.title = None
		self.booktitle = None
		self.eprint = None
		self.eprintType = None
		self.doi = None
		self.link = None
		self.code = None
		self.isPreprint = isPreprint

		self.bib = entry

		entry = entry.replace("\n", " ")
		self.the_type = re.match(r"@([^\{]*)\{", entry).group(1)
		self.file_name = re.match(r"@[^\{]*\{([^,]*),", entry).group(1)
		authors = re.match(r".*author[^\{]*\{([^\}]*)\}", entry).group(1)
		authors = authors.split(" and ")
		authors_good = []
		self.author_surnames = [author.split(", ")[0] for author in authors]
		for author in authors:
			authors_good.append(" ".join(author.split(", ")[::-1]))
		
		if len(authors_good) > 1:
			self.authors = ", ".join(authors_good[:-1])
			self.authors += " and " + authors_good[-1]
		else:
			self.authors = authors_good[0]

		self.month = re.match(r".*month[^\{]*\{([^\}]*)\}", entry).group(1)
		self.year = re.match(r".*year[^\{]*\{([^\}]*)\}", entry).group(1)

		booktitle = re.match(r".*booktitle[^\{]*\{([^\}]*)\}", entry)
		if booktitle is not None:
			self.booktitle = booktitle.group(1)
			conference = re.match(r"[^\(]*(\(.*\))$", self.booktitle)
			if conference is not None:
				self.conference = conference.group(1)
				self.booktitle = self.booktitle.replace(" " + self.conference, "")

		publisher = re.match(r".*publisher[^\{]*\{([^\}]*)\}", entry)
		if publisher is not None:
			self.publisher = publisher.group(1)

		note = re.match(r".*note[^\{]*\{([^\}]*)\}", entry)
		if note is not None:
			self.note = note.group(1)

		school = re.match(r".*school[^\{]*\{([^\}]*)\}", entry)
		if school is not None:
			self.school = school.group(1)

		title = re.match(r".*[^k]title[^\{]*\{(.*)", entry).group(1)

		title_good = ""
		mode = "looking"
		for char in title:
			if char == "{":
				if mode == "looking":
					mode = "checked"
			elif char == "}":
				if mode == "looking":
					break
				else:
					mode = "looking"
			else:
				title_good += char

		self.title = title_good

		if self.file_name in eprints:
			self.eprint, self.eprintType = eprints[self.file_name]

		if self.file_name in dois and not self.isPreprint:
			self.doi = dois[self.file_name]

		if self.file_name in links:
			self.link = links[self.file_name]

		if self.file_name in codes:
			self.code = codes[self.file_name]

		self.pdf = os.path.isfile("../files/publications/pdf/" + self.file_name + ".pdf")

		self.poster = os.path.isfile("../files/publications/posters/" + self.file_name + ".pdf")

	def __gt__(self, other):
		if self.year > other.year:
			return True
		elif self.year < other.year:
			return False
		elif month_gt(self.month, other.month):
			return True
		elif month_gt(other.month, self.month):			
			return False
		elif self.author_surnames > other.author_surnames:
			return True
		elif self.author_surnames < other.author_surnames:
			return False
		else:
			return self.title > other.title

for key in ("pubs", "preprints"):
	entries[key] = [Entry(entry = e, isPreprint = (key == "preprints")) for e in entries[key]]
	# we assume it's empty -- make.bash
	for entry in entries[key]:
		with open("../files/publications/bib/" + entry.file_name + ".bib" , "w") as file:
			file.write(entry.bib)
	
years = {"preprints": set()}

for entry in entries["preprints"]:
	years["preprints"].add(entry)

for entry in entries["pubs"]:
	if entry.year in years:
		years[entry.year].add(entry)
	else:
		years[entry.year] = {entry}


result = "<!-- Automatically generated from my personal .bib file -->\n<h2 id=\"publications\">Publications</h2>\n\n(You may also check my <a href=\"https://dblp.uni-trier.de/pid/319/9565.html\">dblp page</a>.)\n\n"

for year, year_entries in years.items():
	if not year_entries:
		continue
	
	result += f"<h3>{year}</h3>\n\t<ul>\n"
	for entry in sorted(year_entries):

		assert entry.the_type in ("inproceedings", "mastersthesis", "misc")

		result += "\t\t<li> "

		result += entry.authors + ". <strong>" + entry.title + "</strong>. "

		if entry.the_type == "inproceedings":
			result += "In <em>" + entry.booktitle + "</em> " + entry.conference
			if entry.publisher is not None:
				result += ", " + entry.publisher
			result += ", " + f"{entry.month} {entry.year}. "
		elif entry.the_type == "mastersthesis":
			result += "Master's Thesis, " + entry.school + ", " + f"{entry.month} {entry.year}. "
		elif entry.the_type == "misc":
			if not entry.isPreprint:
				result += f"{entry.month} {entry.year}. "

		if entry.note:
			result += f"{entry.note}."

		resources = []
		if entry.pdf:
			resources.append("<a target=\"_blank\" href=\"./files/publications/pdf/" + entry.file_name + ".pdf\">pdf</a>")
		if entry.eprint is not None:
			resources.append("<a target=\"_blank\" href=\"" + entry.eprint + "\">" + entry.eprintType + "</a>")
		if entry.code is not None:
			resources.append("<a target=\"_blank\" href=\"" + entry.code + "\">code</a>")
		if entry.poster:
			resources.append("<a target=\"_blank\" href=\"./files/publications/posters/" + entry.file_name + ".pdf\">poster</a>")
		if entry.link is not None:
			resources.append("<a target=\"_blank\" href=\"" + entry.link + "\">link</a>")
		if entry.doi is not None:
			resources.append("<a target=\"_blank\" href=\"" + entry.doi + "\">doi</a>")

		resources.append("<a target=\"_blank\" href=\"./files/publications/bib/" + entry.file_name + ".bib\">bib</a>")

		result += ("&nbsp;&nbsp;[" + ", ".join(resources) + "]") if resources else ""

		result += "\n"


	result += "\t</ul>\n"

result += "<!-- END PUBLICATIONS -->"

with open("index_template.html", "r") as file:
	data = file.read()

data = data.replace("{{publications}}", result)

with open("../index.html", "w") as file:
	file.write(data)