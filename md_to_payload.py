import datetime
import json
import re

mdf = open("index.md", "r")
md = mdf.read()
md = md.replace("<br>", "\n")

pld = open("payload.json", "w")

md_sections = re.split("^\#\#[^#]", md, flags=re.MULTILINE)[1:]
embeds = []
for section in md_sections:
    title = section.split("\n")[0].strip()
    color = section.split("\n")[1].strip("<!-> \n\t")

    contents = "\n".join(section.split("\n")[2:])
    items = re.split("^\#\#\#", contents, flags=re.MULTILINE)[1:]
    fields = []
    for item in items:
        #TODO: handle links
        item_title = item.split("\n")[0].strip()
        item_title, link = re.match("\[(.*)\]\((.*)\)", item_title).groups()

        item_contents = "\n".join(item.split("\n")[1:]).strip() + "\n" + link
        fields.append({"name":item_title, "value":item_contents})
    embeds.append({"title": title, "color":int(color, 16), "fields":fields})

if len(embeds) > 10:
    raise Exception("Cannot have more than 10 embeds!")

json.dump({"embeds": embeds}, pld)
pld.close()