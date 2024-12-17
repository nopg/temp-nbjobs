import csv

def load_csv(filename: str) -> dict:
    locations = csv.DictReader(filename)

def main(logger, filename) -> None:
    locations = load_csv(filename=filename)
    logger.info(f"locations = {locations}")
