from scoutbook_parser.parser import Parser
from pathlib import Path
from objexplore import explore
import csv


ROOT = Path("/home/perkinsms/Projects/django-troop/django_troop/data/example_troop_scoutbook")


p = Parser(input_advancement=ROOT / "advancement.csv", 
           input_personal=ROOT / "personal_data.csv", 
           file_format="json",
           )


rank_types = set()

with open (ROOT / "advancement.csv") as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line["Advancement Type"] == "Rank":
            if line["Advancement"].split()[-1] == "Scout" and len(line["Advancement"].split()) == 2:
                rank_types.add(line["Advancement"].split()[0])
            else:
                rank_types.add(" ".join((word for word in line["Advancement"].split())))

print(rank_types)
            
    

explore(p)
