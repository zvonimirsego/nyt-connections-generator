import random
import nltk
import pandas as pd
import time
import os
from w2vmodel import model, stop_words
from nltk.corpus import brown, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

sentences = brown.sents()[:10000]

filtered_words = [
    word.lower() for sent in sentences for word in sent if word.isalnum() and word.lower() not in stop_words
]
random.shuffle(filtered_words)

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

# if an error occurs here because index "j" is out of range, just run this window again.

lemmatizer = WordNetLemmatizer()

# an axualliary function which transforms universal tags to wordnet tags, based on the given nltk.org data

cluster = []
clusters = []
words = []
solutions = {}
i = 0

# the main programm which generates one Connections instance
while len(clusters) < 4:
    cluster = []
    j = 0
    main_word = random.choice(filtered_words).lower()
    if main_word in model:
        most_sim = model.most_similar(positive=[main_word], topn = 500)
        if i == 0 and 0.8 <= most_sim[0][1]:
            while len(cluster) < 4:
                similar = False
                word = most_sim[j][0].lower()
                pair = pos_tag([word], tagset='universal')
                word, pos = pair[0][0], pair[0][1]
                word = lemmatizer.lemmatize(word, get_wordnet_pos(pos))
                for w in cluster:
                    if LCS_similarity(word, w) >= 0.75:
                        similar = True
                if similar:
                    j += 1
                    continue
                sim = most_sim[j][1]
                if word.isalnum() and word not in words:
                    cluster.append(word)
                    words.append(word)
                j += 1
            clusters.append(cluster)
            solutions[main_word] = cluster
            i += 1
        elif i == 1 and 0.6 <= most_sim[0][1]:
            while len(cluster) < 4:
                similar = False
                word = most_sim[j][0].lower()
                pair = pos_tag([word], tagset='universal')
                word, pos = pair[0][0], pair[0][1]
                word = lemmatizer.lemmatize(word, get_wordnet_pos(pos))
                for w in cluster:
                    if LCS_similarity(word, w) >= 0.75:
                        similar = True
                if similar:
                    j += 1
                    continue
                sim = most_sim[j][1]
                if (word.isalnum() and word not in words and 0.6 <= sim < 0.8 and len(cluster) == 0) or (word.isalnum() and word not in words):
                    cluster.append(word)
                    words.append(word)
                j += 1
            clusters.append(cluster)
            solutions[main_word] = cluster
            i += 1
        elif i == 2 and 0.5 <= most_sim[0][1]:
            while len(cluster) < 4:
                similar = False
                word = most_sim[j][0].lower()
                pair = pos_tag([word], tagset='universal')
                word, pos = pair[0][0], pair[0][1]
                word = lemmatizer.lemmatize(word, get_wordnet_pos(pos))
                for w in cluster:
                    if LCS_similarity(word, w) >= 0.75:
                        similar = True
                if similar:
                    j += 1
                    continue
                sim = most_sim[j][1]
                if (word.isalnum() and word not in words and 0.5 <= sim < 0.6 and len(cluster) == 0) or (word.isalnum() and word not in words):
                    cluster.append(word)
                    words.append(word)
                j += 1
            clusters.append(cluster)
            solutions[main_word] = cluster
            i += 1
        elif i == 3 and 0 <= most_sim[0][1]:
            while len(cluster) < 4:
                similar = False
                word = most_sim[j][0].lower()
                pair = pos_tag([word], tagset='universal')
                word, pos = pair[0][0], pair[0][1]
                word = lemmatizer.lemmatize(word, get_wordnet_pos(pos))
                for w in cluster:
                    if LCS_similarity(word, w) >= 0.75:
                        similar = True
                if similar:
                    j += 1
                    continue
                sim = most_sim[j][1]
                if word.isalnum() and word not in words and sim < 0.5:
                    cluster.append(word)
                    words.append(word)
                j += 1
            clusters.append(cluster)
            solutions[main_word] = cluster
            i += 1

for clus in clusters:
    clus.sort()

random.shuffle(words)

word_table = [[words[4*i+j] for j in range(4)] for i in range(4)]
df = pd.DataFrame(word_table)
df.columns = [''] * df.shape[1]
df.index = [''] * df.shape[0]
print(df.to_string())

# How to play:
# Write your guess in the appropriate area as 4 words, seperated by space. 
# Extra spaces will be removed.
# If you type in 'hint', the similarity matrix will show up

attempts_left = 4
solved = False
guessed = 0
hints_used = 0

wordss = []
for word in words:
    wordss.append(word)

for key, value in solutions.items():
    value.sort()

while attempts_left > 0 and not solved:
    wordss_table = [[wordss[4*i+j] for j in range(4)] for i in range(int(len(wordss)/4))]
    wt = pd.DataFrame(wordss_table)
    wt.columns = [''] * wt.shape[1]
    wt.index = [''] * wt.shape[0]
    print(wt.to_string())
    print(f"Attempts left: {attempts_left}")
    attempt = input().split(" ")
    attempt.sort()
    if attempt == ['hint']:
        display_similarity_matrix(wordss)
        hints_used += 1
        continue
    for word in attempt:
        if word == '':
            attempt.remove(word)
    time.sleep(1)
    if attempt in clusters:
        guessed += 1
        print("Correct! You've guessed a cluster!")
        for key, value in solutions.items():
            if value == attempt:
                print(f"{key} : {value}")
        for word in attempt:
            wordss.remove(word)
        time.sleep(1)
        random.shuffle(wordss)
    else:
        print("Wrong! Try again!")
        attempts_left -= 1
        time.sleep(1)
    if len(wordss) == 0 or guessed == 4:
        solved = True
    print()
print("GAME OVER!")
if solved:
    print("Congrats! You're so good at this!")
else:
    print("Better luck next time!")
print()
for key, cluster in solutions.items():
    for word in cluster:
        print(word, end=" ")
    print(f"- {key}")
print(f"Hints used: {hints_used}")
os.system("pause")