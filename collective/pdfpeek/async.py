import datetime
import logging

import persistent
from zope import interface
from zope import component
from zope.app.component.hooks import getSite, getSiteManager
from ZODB.POSException import ConflictError

logger = logging.getLogger('collective.pdfpeek.async')


class IQueue(interface.Interface):
    pass


class Queue(persistent.Persistent):
    interface.implements(IQueue)

    def __init__(self):
        self.pending = persistent.list.PersistentList()
        self.failures = persistent.list.PersistentList()
        self.finished = persistent.list.PersistentList()

    def process(self):
        num = len(self.pending)
        if num > 0:
            job = self.pending[0]
            try:
                job()
            except (ConflictError, KeyboardInterrupt):
                # Let Zope handle this.
                raise
            except:
                logger.warn("Removing job %s after Exception:" % job,
                            exc_info=1)
                job.value = "%s failed" % job
                self.failures.append(job)
            else:
                logger.info("Finished job: %s", job)
                self.finished.append(job)
            self.pending.remove(job)
        return num


class Job(persistent.Persistent):
    executed = None
    title = u''

    def __init__(self, fun, *args, **kwargs):
        self._fun = fun
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        self.value = self._fun(*self._args, **self._kwargs)
        self.executed = datetime.datetime.now()

    def __str__(self):
        return '<Job %r with args %r and kwargs %r>' % (
            self._fun.__name__, self._args, self._kwargs)


def get_queue(name):
    portal = getSite()
    queue = component.queryUtility(IQueue, name)
    if queue is None:
        queue = Queue()
        sm = getSiteManager()
        sm.registerUtility(queue, provided=IQueue, name=name)
    return queue
