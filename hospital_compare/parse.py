#!/usr/bin/env python

import csv

filename = "download/HCAHPS Measures.csv"

with open(filename, 'rb') as f:
    reader = csv.reader(f)
    reader.next() # skip header
    hospitals = {}
    marked = [] # duplicates that need to be cleaned up later
    for row in reader:
        # "Patients who reported YES they would definitely recommend the hospital."
        def_recommend = row[38]
        if def_recommend == "N/A": continue # skip hospitals without data

        hosp_id = row[0]
        name = row[1].title()
        city = row[5].title()
        state = row[6]

        # check for duplicate name
        if name in hospitals:
            # mark to be changed laterin case of other duplicates
            if name not in marked:
                marked.append(name)
            # change current one
            name = name + ", " + city + ", " + state

        hospitals[name] = {
            "city": city, 
            "state": state, 
            "hosp_id": hosp_id, 
            "def_recommend": def_recommend,
            "name": name
        }

    # clean up the marked hospitals
    for name in marked:
        city = hospitals[name]["city"]
        state = hospitals[name]["state"]
        new_name = name + ", " + city + ", " + state
        hospitals[new_name] = hospitals.pop(name)


output = open('output.txt', 'w')
tab = "\t"
external_link = "[http://www.hospitalcompare.hhs.gov/ Medicare Hospital Compare]\\n"
abstract_tmpl = "%(def_recommend)s%% of patients would DEFINITELY recommend %(name)s."
source_url_tmpl = "http://www.hospitalcompare.hhs.gov/hospital-profile.aspx?pid=%(hosp_id)s"

for hosp in hospitals:
    abstract =  abstract_tmpl % hospitals[hosp]
    source_url = source_url_tmpl % hospitals[hosp]
    line = hosp + tab + "A" + tab*7 + external_link + tab*3 + abstract + tab + source_url + "\n"
    output.write(line)

output.close()
