import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag

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

    dist = 1 - levenshtein(parsed_url1.path, parsed_url2.path) / max(len(parsed_url1.path), len(parsed_url2.path))
    score = (dist + 1) / 2 # normalize the score

    return score < .9

# calculate the levenshtein distance between two url paths as a measure of similarity

def levenshtein(url_path1, url_path2):
    d = [[0] * (len(url_path2) + 1) for j in range(len(url_path1) + 1)] # make the matrix to help calculate the levenshtein distance

    for i in range(len(url_path1) + 1): # distances
        d[i][0] = i

    for j in range(len(url_path2) + 1): # first row of matrix
        d[0][j] = j

    # fill out the distance matrix with options for deletion, insertion, and substitution
    for i in range(1, len(url_path1) + 1):
        for j in range(1, len(url_path2) + 1):
            if url_path1[i - 1] == url_path2[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost) # cost of deletion, insertion, and substitution respectively

    return d[len(url_path1)][len(url_path2)]


if __name__ == '__main__':
    print(compare_urls('https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_files=files&do=media&tab_details=edit&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content', 'https://swiki.ics.uci.edu/doku.php/virtual_environments:virtualbox?tab_details=edit&do=media&tab_files=search&image=virtual_environments%3Ajupyterhub%3Avscode.jpg&ns=wiki#dokuwiki__content'))
    print(compare_urls('https://google.com/something', 'https://google.com/somethingelse'))