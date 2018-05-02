from requests_html import HTMLSession  # pip install requests-html

import scraperwiki

MPS_A_Z_URL = "https://www.eduskunta.fi/FI/kansanedustajat/Sivut/Kansanedustajat-aakkosjarjestyksessa.aspx"


def scrape_list(url):
    """Parse the list of politicians, isolating each one by name"""

    r = session.get(url)
    mps_list = r.html.find("#MSOZoneCell_WebPartWPQ3", first=True)
    mps = mps_list.find(".dfwp-item")

    for mp in mps:
        person = {}
        person["name"] = mp.find("a", first=True).text
        person["party"] = mp.find(".description", first=True).text
        mp_url = mp.links.pop()

        print("{}\t{}\t{}".format(mp_url, person["party"], person["name"]))

        scrape_person(person, mp_url)


def scrape_person(person, url):
    """Parse the data for each individual politician"""

    r = session.get(url)
    table = r.html.find(".mopPersonTable", first=True)
    rows = table.find("tr")

    for row in rows:
        cells = row.find("td")
        key = cells[0].text.rstrip(":")
        person[key] = cells[1].text

        print("{}:\t{}".format(key, person[key]))

        # Write out to the sqlite database using scraperwiki library
        scraperwiki.sqlite.save(unique_keys=["name"], data=person)


session = HTMLSession()

scrape_list(MPS_A_Z_URL)


# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a
# table called "data".
