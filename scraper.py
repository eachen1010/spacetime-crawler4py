import re
from bs4 import BeautifulSoup
from manager import Manager
from tokenizer import tokenize
from urllib.parse import urlparse, urljoin, urldefrag
from helper import compare_urls

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # if the url is already in the blacklist, return an empty list
    if url in Manager.blacklist:
        return []

    # if the response status indicates an error, check if the current url has been seen before and blacklist it if it has
    if resp.status >= 400:
        if url not in Manager.retry:
            Manager.retry.add(url)
            return []
        else:
            Manager.retry.remove(url)
            Manager.blacklist.add(url)
            return []
    
    # if the response status is 204, directly blacklist the url and return an empty list
    if resp.status == 204:
        Manager.blacklist.add(url)
        return []
    
    if resp.status == 200:
        # if the url has no data, blacklist the url and return an empty list
        if not resp.raw_response.content:
            Manager.blacklist.add(url)
            return []

        # parses the raw HTML content of the page using lxml's html parser
        soup = BeautifulSoup(resp.raw_response.content, "lxml")
        # extracts only text content and removes whitespaces
        text = re.sub(r'\s+', ' ', soup.get_text())
        
        # if the text-to-html ratio is less than 25%, blacklist the url and return an empty list
        # if (len(''.join(text)) / len(resp.raw_response.content) < 0.25): 
        #     Manager.blacklist.add(url)
        #     return []

        # tokenizes the text content of the page
        tokenize(url, text)

        Manager.crawled.add(url)
        Manager.blacklist.add(url)

        links = set()
        # for each <a> tag, extracts the href attribute and transforms the relative URL to absolute URL
        for tag in soup.find_all('a', href = True):
            try: 
                # discards the fragments from the relative url 
                relativeURL = urldefrag(tag['href'])[0]
                if relativeURL: 
                    # transforms the relative url to absolute url
                    absoluteURL = urljoin(url, relativeURL)
                    # checks if the url has been encountered before during the crawling process
                    if absoluteURL not in Manager.seen:
                        links.add(absoluteURL)
                        Manager.seen.add(absoluteURL)
                        Manager.current_compare_url = absoluteURL
            except KeyError:
                # if the 'href' attribute is not present in the tag, skips it
                pass
        return list(links)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    # Compare the urls
    # if not compare_urls(Manager.current_compare_url, url):
    #     return False
        
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return ".ics.uci.edu" in parsed.hostname and not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
