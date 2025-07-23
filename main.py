import random
import pandas as pd
import time
import os
from src.w2vmodel import *
from src.functions import *
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

if __name__ == "__main__":
    sentences = brown.sents()[:10000]

    filtered_words = [
        word.lower() for sent in sentences for word in sent if word.isalnum() and word.lower() not in stop_words
    ]
    random.shuffle(filtered_words)

    # if an error occurs here because index "j" is out of range, just run again.

    lemmatizer = WordNetLemmatizer()
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