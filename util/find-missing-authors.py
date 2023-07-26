import csv
from lxml import etree as ElementTree


def parseDBLP():
    authors = {}

    with open("dblp.xml", mode="r") as f:
        # was: with gzip.open('dblp.xml.gz') as f:

        oldnode = None

        foundArticle = False
        authorName = ""

        for (event, node) in ElementTree.iterparse(f, events=["start", "end"]):

            if oldnode is not None:
                oldnode.clear()
            oldnode = node

            if oldnode.tag in ["inproceedings", "article"]:

                for child in oldnode:
                    if child.tag in ["booktitle", "journal"]:
                        foundArticle = True
                        break

                if not foundArticle:
                    # Nope.
                    continue

                for child in oldnode:
                    if child.tag == "author":
                        authorName = child.text
                        if authorName is not None:
                            authorName.strip()
                            if authorName not in authors:
                                authors[authorName] = 1

    return authors


#    a = sorted(authors.iteritems(), key=operator.itemgetter(1))
#    for k in a:
#        print k[0]


def csv2dict_str_str(fname):
    with open(fname, mode="r") as infile:
        reader = csv.reader(infile)
        # for rows in reader:
        #    print rows[0], "-->", rows[1]
        d = {
            unicode(rows[0].strip(), "utf-8"): unicode(
                rows[1].strip(), "utf-8"
            )
            for rows in reader
        }
    return d


facultydict = csv2dict_str_str("faculty-affiliations.csv")

authors = parseDBLP()

for name in facultydict:
    if name not in authors:
        print(name.encode("utf-8"))
