class Manager:
    # set containing URLs that have already been crawled or encountered errors more than once during crawling
    blacklist = set() 

    # set containing URLs that have been successfully crawled
    crawled = set()

    # set containing URLs which encountered errors during the initial crawling attempt
    # but are given another chance to be processed later 
    retry = set()

    # set containing URLs that have been encountered during crawling but not yet crawled
    seen = set()

    # dictionary containing all tokens from each crawled url 
    tokens = dict()

    # list containing information about the longest page encountered 
    longest_page = {"url": '', "count": 0}

    # depth checking for pages, seed starts at 0
    depth_check = 0

    # url similarity checking
    similarity_count = 0
    seen_url_blacklist = set()
    current_compare_url = 'ics.uci.edu'
