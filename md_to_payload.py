# md_to_payload.py
#   by patataofcourse
#
#   Converts a resources-and-guides style (see the README for reference) markdown file
#   into a Discord JSON payload that can be curl-ed to the Discord webhook API.
#   To see how the webhook is sent, see .github/workflows/discord-hook.yml

import datetime
import json
import re

#TODO: maybe act as a markdown preprocessor as well?

mdf = open("index.md", "r")
md = mdf.read()
md = md.replace("<br>", "\n")

pld = open("payload.json", "w")

embeds = []

# detect every section (headed by a h2 ##), separate the "header"
md_sections = re.split("^\#\#[^#]", md, flags=re.MULTILINE)
header = md_sections[0].strip()
md_sections = md_sections[1:]

for section in md_sections:
    title = section.split("\n")[0].strip()
    color = section.split("\n")[1].strip("<!-> \n\t")

    contents = "\n".join(section.split("\n")[2:])

    # detect every item (headed by a h3 ###)
    items = re.split("^(?:<!--\s+)?\#\#\#", contents, flags=re.MULTILINE)[1:]
    fields = []
    for item in items:
        item_title = item.split("\n")[0].strip()
        item_meta = []

        # pre-title meta parameters (for commented items)
        if not item_title.startswith("["):
            item_meta += item_title[:item_title.find("[")].strip().split(" ")
            item_title = item_title[item_title.find("["):]

        # detect the markdown link [a](b) format
        item_title, link = re.match("\[(.*)\]\((.*)\)", item_title).groups()

        item_contents = "\n".join(item.split("\n")[1:]).strip().strip("-> ")

        # pre-contents meta parameters (for uncommented items)
        if item_contents.startswith("<!--"):
            item_meta += item_contents.split("\n")[0].strip("<!- ").split(" ")
            item_contents = "\n".join(item_contents.split("\n")[1:])

        # right now, links 
        item_contents += "\n" + link

        # no-discord and no-display do basically the same rn,
        # they're just different for semantic purposes
        if not ("no-discord" in item_meta) and not ("no-display" in item_meta):
            fields.append({"name":item_title, "value":item_contents})
    embeds.append({"title": title, "color":int(color, 16), "fields":fields})

# if we ever run out of space in an embed, or 10 RH games get released, we'll worry about this
if len(embeds) > 10:
    raise Exception("Cannot have more than 10 embeds!")
payload = json.dumps({"embeds": embeds, "content": header})
pld.write(payload)
pld.close()