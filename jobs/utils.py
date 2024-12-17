import csv
from nautobot.dcim.models import Location, LocationType
from django.db.models.fields.files import FieldFile
STATES = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

def load_csv(filename, logger):
    logger.warning(f"type: ```{type(filename)}```")
    if isinstance(filename, FieldFile):
        data = filename.open(mode="r")
    else:
        data = open(filename, "r")
    logger.warning(f"type-data: ```{type(data)}```")
    logger.warning(data)
    try:
        locations = csv.DictReader(data)
        return list(locations)
    except FileNotFoundError:
        raise Exception(f"{filename} not found!")

def create_state(name):
    state, created = Location.objects.get_or_create(name=state, location_type=LocationType.objects.get(name="State"))
    return created

def load_locations(logger, locations):
    for location in locations:
        state = location.get("state")
        if not state:
            raise Exception(f"State missing for location: '{location.get('name')}'")
        if state in STATES:
            state_name = STATES[state]
        elif state in STATES.values():
            state_name = state
        else:
            raise Exception(f"State {state} does not appear to be correct.")
        created = create_state(state_name)
        if created:
            logger.info(f"Created State: '{state_name}")

def main(logger, filename) -> None:

    locations = load_csv(filename, logger)
    logger.info(f"locations = {locations}")

    load_locations(logger, locations)


if __name__ == "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)

    filename = "locations.csv"
    main(logger=logger, filename=filename)
