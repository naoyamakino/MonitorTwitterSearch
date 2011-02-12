import sys
import time
import re
from twython import Twython
urls = {}
def update_urls(max_id):
    twitter = Twython()
    results = twitter.searchTwitter(q=sys.argv[1], rpp="100", since_id = max_id)
    max_id = results["max_id"]
    for tweet in results["results"]:
        text = tweet["text"]
        links = re.findall(r'(http?://\S+)', text)
        for link in links:
            try:
                url =  link.encode('ascii') 
            except UnicodeEncodeError:
                continue
            if url in urls:
                count = urls[url]
                count += 1
                urls[url] = count
            else:
                urls[url] = 1
    return max_id

def count_popular_links(k):
    i = 0
    for url, count in urls.items():
        if count >= k:
            i += 1
    return i

def populate_links(k):
    for url, count in urls.items():
        if count >= k:
            print url + ': ' + str(count)

def main():
    if len(sys.argv) != 2:
        print "usage: monitor.py [query]"
        sys.exit()
    else:
        max_id = 0
        current_number_of_links = 0
        k = 3
        while(1):
            time.sleep(1)
            max_id = update_urls(max_id)
            if count_popular_links(k) > current_number_of_links:
                populate_links(k)
                current_number_of_links = count_popular_links(k) 

if __name__ == "__main__":
    main()

