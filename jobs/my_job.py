from nautobot.apps.jobs import Job, register_jobs, FileVar

class ImportLocations(Job):
    class Meta:
        name = "Import Locations from CSV"
        description = "RG's Jobs"
    
    csv = FileVar()

    def run(self, csv):
        self.logger.info("Testing...")


register_jobs(ImportLocations)
