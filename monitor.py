import sys
import time
from twython import Twython


def main():
    if len(sys.argv) != 2:
        print "usage: monitor.py [query]"
        sys.exit()
    else:
        k = 3
        twitter = Twython()
        initial_results = twitter.searchTwitter(q=sys.argv[1], rpp=k)
        max_id = initial_results["max_id"]
        
        while(1):
            time.sleep(1)
            results = twitter.searchTwitter(q=sys.argv[1], since_id = max_id, rpp=k)
            if len(results["results"]) >= k:
                refresh_url = "http://search.twitter.com/search" + results["refresh_url"]
                print refresh_url
                max_id = results["max_id"]

if __name__ == "__main__":
    main()

