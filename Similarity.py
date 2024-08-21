
def counter(array, w, word_dict):
    '''
    This function takes the word_dict of the current word from wlist and updates it.
    Precondition: The old dict for the word from wlist
    Postcondition: The updated version of the dict for the word from wlist
    :param array: The array with the words from on line from the original document (no set)
    :param w: The word from wlist that is being examined
    :param word_dict: The dictionary for one word from wlist that contains all the words that have been found previously in the region of w and the number of findings
    :return: The updated word_dict
    '''
    stopwords = set(["s", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])
    word_set = set(list(word_dict.keys())) # extract the words that were already saved to the given dictionary and make it a set
    for i in range(int(len(array))): # go through the words in the given list of words (former line)
        if array[i] != w and (not(array[i] in stopwords)) and len(array[i]) > 2: # if this respective word is not equal to the word from wlist and doesn't appear in stopwords and is longer than 2 letters, then
            if array[i] in word_set: # if the word already exists in the dictionary of the current word from wlist
                word_dict[array[i]] = word_dict[array[i]] + 1 # increase its current "counter" by one
            else: # if not
                word_dict[array[i]] = 1 # create a new entry in this dictionary and set the counter to 1

    return word_dict # return the updated word_dict for the current word from wlist

def get_and_prepare():
    '''
    This function reads the data and returns an array with all the lines of the initial file in it.
    Precondition: The textfile has not been read and is not available
    Postcondition: The textfile has been read and is available for further scrutiny
    :return: Reads the initial document and returns an array with lists with the words of the respective line from the original document
    '''
    import re
    import numpy as np
    text = open("ref-sentences.txt", encoding="utf8") # open the text source file
    ar = np.array([None] * 100001) # create an empty array to store all the lines

    i = 0 # set the counter variable to 0
    for line in text: # go through every line in the text
        i = i + 1 # increase i by 1
        ar[i] = re.split("[ ,;:\"\"\?!]+", line) # split the strings into words and assign these words in form of a list to a position in the array
        ar[i] = list(map(lambda x: x.lower(), ar[i])) # make all words lowercase
    text.close() # close the text source file
    return ar # return the array

def make_set(ar):
    '''
    This function returns an array with sets of word instead of lists of words (as in the array that is given to the function).
    Precondition: The text source file has been read and is in an array in form of a list for every line in one position of the array
    Postcondition: A second array with sets of the lists instead of the lists
    :param ar: The array, that contains lists, each list with the words of one line
    :return: An array with the former lists converted to sets
    '''
    import numpy as np
    ar_set = np.array([None] * 100001) # create a new empty array in the length of the number of lines in the text source document
    for i in range(int(len(ar)-1)): # go through every line of the array
        i = i + 1 # increase i by 1
        ar_set[i] = set(ar[i]) # fill the recently created array with sets instead of lists of words

    return ar_set # return the array with the sets

def get_numbers(ar_set, ar, wlist):
   '''
   This function creates a dictionary with every word in wlist as a key and another dictionary as values for the key where the number of appearances of each word that has ever been found in the word from wlist's environment is saved.
   Precondition: The dictionary that saves the occurences of words in the surrounding of every word from wlist does not exist
   Postcondition: This dictionary does exist and is complete according to the text source file
   :param ar_set: The array where each entry contains the set of words of its corresponding line in the text source document
   :param ar: The array where each entry contain the list of words of its corresponding line in the text source document
   :param wlist: The words that are to be examined regarding similarity
   :return: words: The set that contains a set for every word in wlist that contains every word that has been
                    found in the word's context throughout the text source document and the number of its occurrences
   '''
   words = {} # create an empty dictionary
   for word in wlist: # go through the wordlist
       words[word] = {} # create a new empty dictionary
       for i in range(100000): # go through all lines/positions in ar_set that was given to the function
           if word in ar_set[i+1]: # if the current word from wlist is in the respective set, then
               words[word] = counter(ar[i+1], word, words[word]) # create a new dictionary or update it, using the function counter

   return words # return a dictionary with a dictionary of word appearances for every word from wlist

def similarity_matrix(words, wlist):
    '''
    This function gets the previously created dictionary of dictionaries and the wordlist and calculated on this basis a cosine-similarity matrix of all
    words from this wordlist.
    Precondition: The similarity matrix does not exist
    Postcondition: The similarity matrix with all similarities between words from wlist does exist and is returned
    :param words: The set of words where each set contains a set of all words and their number of occurrences throughout the text source document
    :param wlist: The list of word that are examined regarding their similarity
    :return: sim_matrix: The matrix that stores the cosine-similarity of two words
    '''
    import numpy as np
    import math
    dimensions = (int(len(wlist)), int(len(wlist))) # set the dimensions of the similarity matrix (number of words in wlist * number of words in wlist)
    # create four matrices with these dimensions with 0s
    sim_matrix = np.zeros(dimensions)
    mix_matrix = np.zeros(dimensions)
    one_matrix = np.zeros(dimensions)
    two_matrix = np.zeros(dimensions)

    # fill these matrices with similarity values
    for i in range(int(len(wlist))): # go through every row
        for j in range(int(len(wlist))): # go through every column
            inner_array_i = words[wlist[i]] # take the dictionary of similar words from wlist[i]
            inner_array_j = words[wlist[j]] # take the dictionary of similar words from wlist[j]
            for word in inner_array_i: # go through the first created dictionary
                mix_matrix[i, j] += inner_array_i[word] * inner_array_j.get(word,0) # add to its respective place the product of the "counter" of every word from inner_array_i with the respective one of inner_array_j, if found, else multiply it with 0
                one_matrix[i, j] += inner_array_i[word] * inner_array_i[word] # add to its respective place the product of every inner_array_i's "counter" with itself
            for word in inner_array_j: # go through the second created dictionary
                two_matrix[i, j] += inner_array_j[word] * inner_array_j[word] # add to its respective place the product of every inner_array_j's "counter" with itself
            sim = mix_matrix[i, j] / (math.sqrt(one_matrix[i, j] * two_matrix[i, j])) # calculate all the potential entries of the similarity matrix
            if sim < 1: # if this potential entry is smaller than 1, then
                sim_matrix[i, j] = sim # add it to its place
            else: # if not
                sim_matrix[i, j] = 0 # set its place to 0

    return sim_matrix # return the similarity matrix

def show_similar_words(wlist, sim_matrix):
    '''
    This function searches the highest similarity value for a word, returns this similar word and the respective value.
    Precondition: The word with the highest cosine similarity for another word from wlist and the similarity value are unknown
    Postcondition: The word with the highest cosine similarity for another word from wlist and the similarity value are known and returned
    :param wlist: The list of words that are to be examined regarding their similarities
    :param sim_matrix: The matrix that stores the cosine-similarity values of all words
    :return: Nothing, but shows for each word the word from wlist with the highest cosine-similarity value
    '''
    import numpy as np
    for i in range(int(len(wlist))): # go through wordlist with the iterator i
        print(wlist[i], "   ->   ", wlist[np.argmax(sim_matrix[i])], ", ", max(sim_matrix[i])) # print the respective word from wlist, the word with the highest similarity and the highest similarity value

def main() :
    '''
    calls several functions to calculate the cosine-similarity values between words from a given list, based on a sample text
    :return: Nothing but shows for each word from the given list the other word from that list that has the highest cosine-similarity value
    '''
    # define the word lists
    #wlist = ["spain", "anchovy", "france", "internet", "china", "mexico", "fish", "industry", "agriculture", "fishery", "tuna", "transport", "italy", "web", "communication", "labour", "fish", "cod"]
    wlist = ['canada', 'disaster', 'flood', 'car', 'road', 'train', 'rail', 'germany', 'switzerland', 'technology', 'industry', 'conflict']

    # call the functions defined above
    ar = get_and_prepare()
    ar_set = make_set(ar)
    words = get_numbers(ar_set, ar, wlist)
    sim_matrix = similarity_matrix(words, wlist)
    show_similar_words(wlist, sim_matrix)


if __name__ == "__main__":
    main()
