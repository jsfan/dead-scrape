import threading
from random import shuffle

import dead_scrape.domain_data as data


class DomainFeeder(threading.Thread):
    
    def __init__(self, thread_id, lock, threshold, count, backend):
        threading.Thread.__init__(self)
        self.lock = lock
        self.cond = threading.Condition(self.lock)
        self.thread_id = thread_id
        self.load_threshold = threshold
        self.load_count = count
        self.counter = 0
        self.backend = backend

    def run(self):
        more = True
        while more:
            with self.lock:
                if more and len(data.domain_list) < self.load_threshold:
                    i = 0
                    for d in self.backend.domainloader:
                        data.domain_list.append(d[0])
                        i += 1
                    if i < 1000:
                        more = False
                        data.domain_list = None
                    self.counter += i
                    self.cond.notify_all()