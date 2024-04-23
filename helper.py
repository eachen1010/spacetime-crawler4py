import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag

# Compare two urls to avoid traps between similar pages            
def compare_urls(url1, url2):
    
    # use the urlparse lib to get the protocol and domain and then use Levenshtein distance to calculate a similarity score
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2).path.split("/")

    basic_compare = False
    if parsed_url1.scheme == parsed.url2.scheme and parsed_url1.netloc == parsed.url2.netloc:
        basic_compare = True
    


    print(parsed_url1)


if __name__ == '__main__':
    compare_urls('https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_files=files&do=media&tab_details=edit&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content', 'https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_details=edit&do=media&tab_files=search&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content')
    