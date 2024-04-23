import re
from bs4 import BeautifulSoup
import socket
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
    robots_txt_content = get_robots_txt(url)
    disallowed_urls = disallowed_robots_urls(robots_txt_content)

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.search(r"(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu)", parsed.netloc):
            return False
        if parsed.path in disallowed_urls: # If url path in disallowed, then robots.txt says not allowed
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
def get_robots_txt(url):
    '''Open robots.txt file of website to make sure that every
    webpage accessed is allowed to our web crawler'''

    try:
        parsed = urlparse(url)
        hostname = parsed.netloc

        # Connect to server 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as response:
            response.connect((hostname, 80))
            request = f"GET /robots.txt HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
            response.sendall(request.encode())

            response = b""
            while True:
                data = response.recv(1024)
                if not data:
                    break
                response += data

            # Extract content from response
            _, _, content = response.partition(b'\r\n\r\n')

            # Decode content as utf-8
            content_str = content.decode('utf-8')

            return content_str

    except Exception as error:
        print("Error:", error)

def disallowed_robots_urls(robots_txt_content):
    '''Puts disallowed urls into disallowed_urls list'''

    disallowed_urls = []
    if robots_txt_content:
        lines = robots_txt_content.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("Disallow: "):
                disallowed_url = line[10:].strip()
                disallowed_urls.append(disallowed_url)

        return disallowed_urls
