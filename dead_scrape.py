import threading
import yaml

from dead_scrape.domain_data import *
from dead_scrape.check_domain import DomainChecker
from backends.feeders.domain_feeder import DomainFeeder
from backends.feeders.mysql_feeder import MySQLDomainFeeder
from backends.results.results_handler import ResultsHandler
from backends.results.file_results import FileResults

config_file = open('config.yaml', 'r')
config = yaml.load(config_file)
feeder_config = config['feeder']
results_config = config['results']

for addr in config['ips']:
    ip_addr.append(addr)

threshold = feeder_config['load']['threshold']
count = feeder_config['load']['count']
if feeder_config['type'] == 'mysql':
    feed_backend = MySQLDomainFeeder(credentials=feeder_config['credentials'], conf=feeder_config['config'])

if results_config['type'] == 'file':
    res_backend = FileResults(filename=results_config['details']['filename'])

lock = threading.Lock()
feeder_thread = DomainFeeder(0, lock, threshold, count, feed_backend)
feeder_thread.start()
results_thread = ResultsHandler(1, lock, res_backend)
results_thread.start()

threads = [feeder_thread, results_thread]
for i in range(2, config['threads']+1):
    thread = None
    thread = DomainChecker(i, lock)
    thread.start()
    threads.append(thread)