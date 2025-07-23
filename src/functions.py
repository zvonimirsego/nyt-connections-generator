import pandas as pd
from src.w2vmodel import model
from nltk.corpus import wordnet

# function which tells how similar two words are, in percentage to the longer word.
# e.g. LCS of saturday and sunday is suday, length is 5. LCS similarity would then be 5/8 = 0.625
def LCS_similarity(x : str, y : str):
    table = []
    n = len(x)
    m = len(y)
    for i in range(n+1):
        row = []
        for j in range(m+1):
            row.append(-1)
        table.append(row)
    for i in range(m+1):
        table[0][i] = 0
    for i in range(n+1):
        table[i][0] = 0
    for i in range(1, n+1, 1):
        for j in range(1, m+1, 1):
            if x[i-1] == y[j-1]:
                table[i][j] = table[i-1][j-1] + 1
            else:
                table[i][j] = max(table[i-1][j], table[i][j-1])
    return table[n][m] / max(n, m)

# an auxiallry function which generates a similarity matrix
def make_sim_matrix(words):
    return [[model.similarity(w1, w2) for w2 in words] for w1 in words]

# the function which displayes the similarity matrix
def display_similarity_matrix(words):
    similarity_matrix = make_sim_matrix(words)
    df = pd.DataFrame(similarity_matrix, index=words, columns=words)
    print(df.round(2).to_string())

# an axualliary function which transforms universal tags to wordnet tags, based on the given nltk.org data
def get_wordnet_pos(tag):
    if tag == 'ADJ':
        return wordnet.ADJ
    elif tag == 'VERB':
        return wordnet.VERB
    elif tag == 'NOUN':
        return wordnet.NOUN
    elif tag == 'ADV':
        return wordnet.ADV
    else:
        return wordnet.NOUN