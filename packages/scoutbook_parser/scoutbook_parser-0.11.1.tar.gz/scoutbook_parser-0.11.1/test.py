from scoutbook_parser import Parser
from pathlib import Path

ROOT = Path("/home/perkinsms/Projects/django-troop/django_troop/data/example_troop_scoutbook")



p = Parser(input_advancement=ROOT / "advancement.csv", input_personal=ROOT / "personal_data.csv", file_format="json")


for scout in p.scouts:
    print(scout)

    print('\n'.join(key for key in p.scouts[scout]))

