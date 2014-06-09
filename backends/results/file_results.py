import csv

from .results_backend import ResultsBackend


class FileResults(ResultsBackend):

    def __init__(self, **output):
        self.csv = open(output['filename'], 'a')

    def write(self, domain, domain_details):
        csvwriter = csv.writer(self.csv, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([domain] + domain_details)