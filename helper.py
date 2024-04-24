import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import Levenshtein

# Compare two urls to avoid traps between similar pages            
def compare_urls(url1, url2):
    
    # use the urlparse lib to get the protocol and domain and then use Levenshtein distance to calculate a similarity score
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2)
    # print(parsed_url1)

    # Extract scheme and domain from parsed URLs
    scheme1, domain1 = parsed_url1[0], parsed_url1[1]
    scheme2, domain2 = parsed_url2[0], parsed_url2[1]

    # If scheme or domain are different, return 0
    if scheme1 != scheme2 or domain1 != domain2:
        return 0

    dist = 1 - Levenshtein.distance(parsed_url1.path, parsed_url2.path) / max(len(parsed_url1.path), len(parsed_url2.path))
    score = (dist + 1) / 2 # normalize the score

    # print(score)

    return score < .9


# if __name__ == '__main__':
#     print(compare_urls('https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_files=files&do=media&tab_details=edit&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content', 'https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_details=edit&do=media&tab_files=search&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content'))
#     print(compare_urls('https://google.com/something', 'https://google.com/somethingelse'))