 #!/usr/bin/env python

from core.main import work
from timeit import default_timer as timer

if __name__ == '__main__':
    start_work = timer()
    work()
    end_work = timer()
    print 'Total work time: ' + str(end_work - start_work)
