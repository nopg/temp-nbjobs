from nautobot.apps.jobs import Job, register_jobs, FileVar
import load_locations

class ImportLocations(Job):
    class Meta:
        name = "Import Locations from CSV"
        description = "RG's Jobs"
    
    filename = FileVar()

    def run(self, filename):
        self.logger.info("Testing...")
        load_locations.run(logger=self.logger, filename=filename)

register_jobs(ImportLocations)
