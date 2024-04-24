from manager import Manager

def tokenize(url, text) -> list:
    word = ''
    token_list = []
    
    # iterate over each character in the file 
    for char in text:
        # if the character is a digit, add it to the current word
        if char.isdigit():
            word += char
        # if the character is an uppercase letter, convert it to lowercase and add it to the current word
        elif char >= 'A' and char <= 'Z':
            word += char.lower()
        # if the character is a lowercase letter, add it to the current word
        elif char >= 'a' and char <= 'z':
            word += char
        # if the character is not alphanumeric, append the current word to the token list and reset the word to an empty string
        else:
            if word:
                token_list.append(word)
                word = ''
                
    # after processing all characters, check if there's any remaining word and append it to the token list
    if word:
        token_list.append(word)
    
    # iterate over each token in the token list
    for token in token_list:
        # increment the count of the token in the word_count dictionary
        Manager.tokens[token] = Manager.tokens.get(token, 0) + 1
    
    # return the dictionary containing word frequencies
    if len(token_list) > Manager.longest_page["count"]:
        Manager.longest_page["url"] = url
        Manager.longest_page["count"] = len(token_list)

def output_common_words(tokens: dict):
    stop_words = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", 
    "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", 
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", 
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd",
    "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd","we'll",
    "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
    "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

    if bool(tokens):
        with open("common_words.txt", "w") as file:
            count = 0
            for key, value in sorted(tokens.items(), key = lambda kv: (-kv[1], kv[0])):
                if count == 50:
                    break
                if key not in stop_words:
                    file.write(key + " - " + str(value) + "\n")
                    count += 1
                
    