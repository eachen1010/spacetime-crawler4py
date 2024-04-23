import re
from bs4 import BeautifulSoup
import urlopen
from urllib.parse import urlparse, urljoin, urldefrag

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

    links = []
    if resp.status == 200:

        # parses the raw HTML content of the page using lxml's html parser
        soup = BeautifulSoup(resp.raw_response.content, "lxml")

        # for each <a> tag, extracts the href attribute and transforms the relative URL to absolute URL
        for tag in soup.find_all('a'):
            try: 
                # discard the fragments from the relative url 
                relativeURL = urldefrag(tag['href'])[0]
                if relativeURL: 
                    absoluteURL = urljoin(url, relativeURL)
                    links.append(urldefrag(absoluteURL))
            except KeyError:
                # if the 'href' attribute is not present in the tag, skip it
                pass

    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.search(r"(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu)", parsed.netloc):
            return False
        return not re.match(
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
    
# Politeness check - checking the robots.txt file - add to is_valid function?
def robot_txt_check(url):
    disallowed_subdirectories = [] # List of subdirectories of url the crawler is disallowed to search 

    # try:
    robot_txt_url = url.rstrip("/") + "/robots.txt"
    with urlopen(robot_txt_url) as response:
        robots_txt = response.read().decode("utf-8")
        lines = robots_txt.split("\n")
        for_all = False
        for line in lines:
            if line.startswith("User-agent: *"):
                for_all = True
            if for_all == True and line.startswith("Disallow"):
                subdir = line[10:] # Gets the subdirectory with /
                disallowed_subdirectories.insert(subdir)
                    
#     except:
#         pass
