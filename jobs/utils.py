import csv
from io import StringIO

from django.db.models.fields.files import FieldFile
from nautobot.dcim.models import Location, LocationType
from nautobot.extras.models import Status

STATES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


def load_csv(filename, logger):
    if isinstance(filename, FieldFile):
        decoded_csv = filename.read().decode("utf-8")
        locations = csv.DictReader(StringIO(decoded_csv))
    else:
        locations = csv.DictReader(open(filename, "r"))
    return list(locations)


def create_state(location):
    status = Status.objects.get(name="Active")
    state = LocationType.objects.get(name="State")
    state_name = location.get("state")

    if not state_name:
        raise Exception(f"State missing for location: '{location.get('name')}'")
    if state_name in STATES:
        state_name = STATES[state]
    elif state_name in STATES.values():
        state_name = state
    else:
        raise Exception(f"State {state_name} does not appear to be correct.")
    breakpoint()
    _, created = Location.objects.get_or_create(
        name=state_name, location_type=state, status=status
    )
    if created:
        return state_name


def create_city(location):
    status = Status.objects.get(name="Active")
    city = LocationType.objects.get(name="City")
    city_name = location.get("city")
    if not city_name:
        raise Exception(f"City missing for location: '{location.get('name')}'")
    _, created = Location.objects.get_or_create(
        name=city_name, location_type=city, status=status
    )
    if created:
        return city_name


def create_site(location):
    status = Status.objects.get(name="Active")
    site_name = location.get("name")
    if not site_name:
        raise Exception(f"Site Name missing!")
    dc_location = LocationType.objects.get(name="Data Center")
    br_location = LocationType.objects.get(name="Branch")
    if site_name.endswith("-BR"):
        loc_type = br_location
    elif site_name.endswith("-DC"):
        loc_type = dc_location
    else:
        raise Exception(f"Site Name does not follow -BR/-DC standards.")

    _, created = Location.objects.get_or_create(
        name=site_name, status=status, location_type=loc_type
    )
    if created:
        return site_name


def main(logger, filename) -> None:

    locations = load_csv(filename, logger)
    logger.debug(f"```{locations=}```")

    for location in locations:
        created = create_state(location)
        if created:
            logger.info(f"Created State: '{created}'")
        created = create_city(location)
        if created:
            logger.info(f"Created City: '{created}'")
        created = create_site(location)
        if created:
            logger.info(f"Created Site: '{created}'")
