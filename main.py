import threading
import sys
from queue import Queue
from spider import Spider
from domain import *
from general import *


NUMBER_OF_THREADS = 8
queue = Queue()

# do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# each queued link is a new job
def create_jobs(queued_links):
    for link in queued_links:
        queue.put(link)
    queue.join()
    crawl()


# check if there are items in the queue, if so crawl them
def crawl():
    queue_file = project_name + '/queue.txt'
    
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(queued_links)


def main(project_name, homepage):
    domain_name = get_domain_name(homepage)
    Spider(project_name, homepage, domain_name)

    create_workers()
    crawl()


if __name__ == '__main__':
    if len(sys.argv) < 3 :
        print('Not enough arguments')
        sys.exit(1)
    else:
        project_name = sys.argv[1]
        homepage = sys.argv[2]
        main(project_name, homepage)
