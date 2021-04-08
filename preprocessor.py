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

dataset = "dataset/full_dataset.txt"
tokens_file = "dataset/tokens.txt"
texts_file = "dataset/texts.txt"
tags_file = "dataset/tags.txt"
text_tab_tags_file = "dataset/texts_tab_tags.txt"
dataset_comma = "dataset/dataset_comma.txt"

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
    file = open(tokens_file, encoding="utf-8-sig")
    # file = open(dataset, encoding="utf-8-sig")
    text = file.read()
    nb_period = text.count(".")
    nb_comma = text.count(",")
    nb_question = text.count("?")
    nb_exclaim = text.count("!")
    print(". " + str(nb_period))
    print(", " + str(nb_comma))
    print("? " + str(nb_question))
    print("! " + str(nb_exclaim))

file = open(text_tab_tags_file, encoding="utf-8")
text = file.read()
with open("dataset/batched.txt", 'w', encoding="utf-8") as batch_file:
    batch_file.write(text.replace("PERIOD", "PERIOD\n").replace("\n\n\n", "\n\n"))


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