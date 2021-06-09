#!/usr/bin/env python
# -*- coding: utf-8-sig -*-
"""
This is a class designed to preprocess data structured as individual textfiles
"""

from os import listdir
from os.path import isfile, join
import re

LOCATE_PATH = False
CONCATENATE = False
CLEAN_UP = False
MAKE_TEXTS_AND_TAGS = False
# CONCATENATE = True
# CLEAN_UP = True
# MAKE_TEXTS_AND_TAGS = True
STATS = False
STATS_TEST = True
BUILD_HUMAN_TESTS = False

dataset = "dataset/full_dataset.txt"
tokens_file = "dataset/tokens.txt"
texts_file = "dataset/texts.txt"
tags_file = "dataset/tags.txt"
text_tab_tags_file = "dataset/texts_tab_tags.txt"
dataset_comma = "dataset/dataset_comma.txt"
batched_file = "dataset/batched.txt"

if LOCATE_PATH:
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)

if CONCATENATE:
    path = "dataset"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    with open(dataset_comma, 'w', encoding="utf-8-sig") as output_file:
        output_file.write("text,label\n")
        for file in files:
            if file[0] == "2":
                # print(file)
                with open("dataset/"+file, encoding="utf-8-sig") as infile:
                    raw_text = infile.read()

                    if CLEAN_UP:
                        raw_text = raw_text.lower()
                        raw_text = raw_text.replace("#", "")
                        raw_text = raw_text.replace(" - ", ", ")
                        raw_text = raw_text.replace("-\n", "")
                        raw_text = raw_text.replace(";", ":")
                        raw_text = raw_text.replace("!", ".")
                        raw_text = raw_text.replace("\"", ",")
                        # Add spacing for subsequent split
                        tokens = re.split('([^a-zåäöA-ZÅÄÖ0-9])', raw_text)
                        unusual = ['', ' ', '\n', '\t', "\uf0b7", "\u202f", "\x84", "\u2002", "\xad", '_', '²', '§', '°', '½', 'à', 'á', 'æ', 'è', 'é', 'ó', 'ú', 'ü', 'ć', 'ţ', '̈', '‐', '‒', '–', '’', '”', '•', '…', '−', '─']
                        tokens = [token for token in tokens if token not in unusual]

                        if MAKE_TEXTS_AND_TAGS:
                            texts = []
                            tags = []
                            for token in tokens:
                                if token == '.':
                                    tags[-1] = "PERIOD"
                                elif token == ',':
                                    tags[-1] = "COMMA"
                                elif token == '?':
                                    tags[-1] = "QUESTION"
                                else:
                                    texts.append(token)
                                    tags.append("EMPTY")
                            for i in range(len(texts)):
                                output_file.write(texts[i]+","+tags[i]+"\n")
                            output_file.write("\n")

if STATS:
    file = open(batched_file, encoding="utf-8")
    text = file.read()
    nb_empty = text.count("EMPTY")
    nb_period = text.count("PERIOD")
    nb_comma = text.count("COMMA")
    nb_question = text.count("QUESTION")
    print("EMPTY: " + str(nb_empty))
    print("PERIOD " + str(nb_period))
    print("COMMA " + str(nb_comma))
    print("QUESTION " + str(nb_question))
    total = (nb_empty + nb_period + nb_comma + nb_question)
    percent_empty = 100 * nb_empty / total
    print("Percent EMPTY: " + str(percent_empty))
    print("Total:", total)

    # IWSLT Ted talk data set
    ted_period = 139619 + 909 + 1100
    ted_comma = 188165 + 1225 + 1120
    ted_question = 10215 + 71 + 46
    ted_empty = 2001462 + 15141 + 16208

    # Szeged Treebank data set
    szeged_period = 81168+9218+3370
    szeged_comma = 120027 + 13781 + 4885
    szeged_question = 1808 + 198 + 75
    szeged_empty = 885451 + 101637 + 36095
    szeged_total = szeged_period + szeged_comma + szeged_question + szeged_empty

    print("Szeged vs SWE")
    print("PERIOD", "\t", szeged_period, "\t", nb_period, "\t", round((nb_period / szeged_period)*100, 1))
    print("COMMA", "\t", szeged_comma, "\t", nb_comma, "\t", round((nb_comma / szeged_comma)*100, 1))
    print("QUESTION", "\t", szeged_question, "\t", nb_question, "\t", round((nb_question / szeged_question)*100, 1))
    print("EMPTY", "\t", szeged_empty, "\t", nb_empty, "\t", round((nb_empty / szeged_empty)*100, 1))
    print("Total", "\t", szeged_total, "\t", total, "\t", round((total / szeged_total)*100, 1))

if STATS_TEST:
    #testset/val_text_file.txt
    # with open('dataset/texts.txt', encoding="utf-8") as file:
    with open('dataset/testset/val_tags_file.txt', encoding="utf-8") as file:
        text = file.read()
    print("nb chars:", len(text))

    words = text.split(" ")
    print("nb words:", len(words))
    print("nb participants needed:", len(words)/650)

    nb_empty = text.count("EMPTY")
    nb_period = text.count("PERIOD")
    nb_comma = text.count("COMMA")
    nb_question = text.count("QUESTION")
    print("EMPTY: " + str(nb_empty))
    print("PERIOD " + str(nb_period))
    print("COMMA " + str(nb_comma))
    print("QUESTION " + str(nb_question))
    total = (nb_empty + nb_period + nb_comma + nb_question)
    percent_empty = 100 * nb_empty / total
    print("Percent EMPTY: " + str(percent_empty))
    print("Total:", total)


if BUILD_HUMAN_TESTS:
    # Assemble human text files
    file = open("dataset/testset/val_text_file.txt", encoding="utf-8")
    text = file.read()
    words = text.split(" ")
    # 1 page = 650 words per human, ca 10-15 minutes
    offset = 0
    word_count = 650
    human_count = 30
    humans = []
    for human in range(human_count):
        humans.append(words[offset:offset+word_count])
        offset += word_count

    for i in range(human_count):
        with open("dataset/testset/human_"+str(i+1)+".txt", 'w', encoding="utf-8") as write_file:
            write_file.write(" ".join(humans[i]))

    # Assemble correct answers (true tags) for humans
    file = open("dataset/testset/val_tags_file.txt", encoding="utf-8")
    text = file.read()
    words = text.split(" ")
    # 1 page = 650 words per human, ca 10-15 minutes
    offset = 0
    word_count = 650
    human_count = 30
    humans = []
    for human in range(human_count):
        humans.append(words[offset:offset+word_count])
        offset += word_count

    for i in range(human_count):
        with open("dataset/testset/human_"+str(i+1)+"_FACIT.txt", 'w', encoding="utf-8") as write_file:
            write_file.write(" ".join(humans[i]))


print("done with...")
if LOCATE_PATH:
    print("* locating path")
if CONCATENATE:
    print("* concatenating")
if CLEAN_UP:
    print("* cleaning")
if STATS:
    print("* stats")
if MAKE_TEXTS_AND_TAGS:
    print("* making texts and tags")