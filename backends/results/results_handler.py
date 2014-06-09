import threading
import dead_scrape.domain_data as data


class ResultsHandler(threading.Thread):

    def __init__(self, thread_id, lock, backend):
        threading.Thread.__init__(self)
        self.lock = lock
        self.cond = threading.Condition(self.lock)
        self.thread_id = thread_id
        self.count = 0
        self.backend = backend

    def run(self):
        backlog = True
        while backlog:
            with self.lock:
                while data.nx_domains:
                    dinfo = data.nx_domains.popleft()
                    self.backend.process(dinfo)
                if not data.nx_domains:
                    backlog = False