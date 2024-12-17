from nautobot.apps.jobs import Job, register_jobs, FileVar
from .utils import main

class ImportLocations(Job):
    class Meta:
        name = "Import Locations from CSV"
        description = "RG's Jobs"
    
    filename = FileVar()

    def run(self, filename):
        self.logger.info("Testing...")
        main(logger=self.logger, filename=filename)

register_jobs(ImportLocations)
