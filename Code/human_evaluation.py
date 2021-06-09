#!/usr/bin/env python
# -*- coding: utf-8-sig -*-
"""
Calculates accuracy, precision, recall and f1-score of human evaluated text files
"""
from os import listdir
from os.path import isfile, join
import re
import numpy as np

BUILD = False
COMPARE = True

# human_tags_file = "dataset/testset/val_tags_file_HUMAN.txt"
tags_file = "dataset/testset/val_tags_file.txt"

if BUILD:
    path = "dataset/testset/done"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    for file in files:
        print(file)
        with open(path + "/" + file, encoding="utf-8") as infile:
            with open("dataset/testset/human_tags/" + file[:-4] + "_tags.txt", 'w', encoding="utf-8") as output_file:
                raw_text = infile.read()
                # words = re.split('([^a-zåäöA-ZÅÄÖ0-9])', raw_text)
                words = raw_text.split(" ")

                for word in words:
                    if "." in word:
                        output_file.write("PERIOD")
                    elif "," in word:
                        output_file.write("COMMA")
                    elif "?" in word:
                        output_file.write("QUESTION")
                    else:
                        output_file.write("EMPTY")

                    output_file.write(" ")

if COMPARE:
    classes = ["PERIOD", "COMMA", "QUESTION", "EMPTY"]
    human_to_res = dict()
    path = "dataset/testset/human_tags"
    human_tag_files = [f for f in listdir(path) if isfile(join(path, f))]
    human_tag_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    # View results for a specific test
    # human_tag_files = [human_tag_files[8]]
    confusion_matrix = {
            "PERIOD": {"PERIOD": 0, "COMMA": 0, "QUESTION": 0, "EMPTY": 0},
            "COMMA": {"PERIOD": 0, "COMMA": 0, "QUESTION": 0, "EMPTY": 0},
            "QUESTION": {"PERIOD": 0, "COMMA": 0, "QUESTION": 0, "EMPTY": 0},
            "EMPTY": {"PERIOD": 0, "COMMA": 0, "QUESTION": 0, "EMPTY": 0}
        }

    path = "dataset/testset/true_tags"
    true_tag_files = [f for f in listdir(path) if isfile(join(path, f))]
    true_tag_files.sort(key=lambda f: int(re.sub('\D', '', f)))

    for human_tag_file in human_tag_files:
        index = int(''.join(char_ for char_ in human_tag_file if char_.isdigit())) - 1
        true_tag_file = true_tag_files[index]
        punct_to_res = {
            "PERIOD": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
            "COMMA": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
            "QUESTION": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0,
                         "f1": 0.0},
            "EMPTY": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
        }

        with open("dataset/testset/true_tags/" + true_tag_file, encoding="utf-8") as infile:
            print(human_tag_file, true_tag_file)
            raw_text = infile.read()
            true_tags = raw_text.split(" ")
            with open("dataset/testset/human_tags/" + human_tag_file, encoding="utf-8") as infile2:
                raw_text = infile2.read()
                human_tags = raw_text.split(" ")[:-1] # Removes trailing space

                for i in range(len(human_tags)):
                    human_tag = human_tags[i]
                    true_tag = true_tags[i]
                    confusion_matrix[human_tag][true_tag] = confusion_matrix[human_tag][true_tag] + 1

                    if human_tag == true_tag:
                        punct_to_res[human_tag]["TP"] = punct_to_res[human_tag]["TP"] + 1
                        for class_ in [class_ for class_ in classes if class_ not in [human_tag]]:
                            punct_to_res[class_]["TN"] = punct_to_res[class_]["TN"] + 1
                    else:
                        punct_to_res[human_tag]["FP"] = punct_to_res[human_tag]["FP"] + 1
                        punct_to_res[true_tag]["FN"] = punct_to_res[true_tag]["FN"] + 1
                        for class_ in [class_ for class_ in classes if class_ not in [human_tag, true_tag]]:
                            punct_to_res[class_]["TN"] = punct_to_res[class_]["TN"] + 1

        for key in punct_to_res:
            TP = punct_to_res[key]["TP"]
            TN = punct_to_res[key]["TN"]
            FP = punct_to_res[key]["FP"]
            FN = punct_to_res[key]["FN"]
            punct_to_res[key]["accuracy"] = (TP + TN) / (TP + TN + FP + FN)
            if TP != 0 or FP != 0:
                punct_to_res[key]["precision"] = TP / (TP + FP)
            if TP != 0 or FN != 0:
                punct_to_res[key]["recall"] = TP / (TP + FN)
            precision = punct_to_res[key]["precision"]
            recall = punct_to_res[key]["recall"]
            if precision != 0 or recall != 0:
                punct_to_res[key]["f1"] = 2 * ((precision*recall) / (precision+recall))
            print(key, punct_to_res[key])

        human_to_res[human_tag_file[:8]] = punct_to_res

    overall_res = {
        "PERIOD": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
        "COMMA": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
        "QUESTION": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
        "EMPTY": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
    }
    # Sum stats for each human into overall score
    for human in human_to_res:
        for key in human_to_res[human]:
            overall_res[key]["TP"] = overall_res[key]["TP"] + human_to_res[human][key]["TP"]
            overall_res[key]["TN"] = overall_res[key]["TN"] + human_to_res[human][key]["TN"]
            overall_res[key]["FP"] = overall_res[key]["FP"] + human_to_res[human][key]["FP"]
            overall_res[key]["FN"] = overall_res[key]["FN"] + human_to_res[human][key]["FN"]

    for key in overall_res:
        TP = overall_res[key]["TP"]
        TN = overall_res[key]["TN"]
        FP = overall_res[key]["FP"]
        FN = overall_res[key]["FN"]
        overall_res[key]["accuracy"] = (TP + TN) / (TP + TN + FP + FN)
        if TP != 0 or FP != 0:
            overall_res[key]["precision"] = TP / (TP + FP)
        if TP != 0 or FN != 0:
            overall_res[key]["recall"] = TP / (TP + FN)
        precision = overall_res[key]["precision"]
        recall = overall_res[key]["recall"]
        if precision != 0 or recall != 0:
            overall_res[key]["f1"] = 2 * ((precision * recall) / (precision + recall))

    for key in overall_res:
        print(key, overall_res[key])

    overall_precision = 0
    overall_recall = 0
    overall_f1 = 0
    string = "Human evalution & "
    for key in ['COMMA', 'PERIOD', 'QUESTION']:
        # print(key, overall_res[key])
        # print(key)
        table = overall_res[key]
        precision = round(table['precision']*100, 1)
        recall = round(table['recall']*100, 1)
        f1 = round(table['f1'] * 100, 1)
        # print(precision, recall, f1, end=' ')
        string += str(precision)+" & "
        string += str(recall) + " & "
        string += str(f1) + " & "

        overall_precision += precision
        overall_recall += recall
        overall_f1 += f1

    overall_precision = round(overall_precision/3, 1)
    overall_recall = round(overall_recall/3, 1)
    overall_f1 = round(overall_f1/3, 1)
    # print(overall_precision, overall_recall, overall_f1)
    string += str(overall_precision) + " & "
    string += str(overall_recall) + " & "
    string += str(overall_f1) + " \\\\"
    print(string)

    for key in confusion_matrix:
        string = "{"
        for class_ in confusion_matrix[key]:
            val = confusion_matrix[key][class_]
            string += str(val)
            string += ", "
        string = string[:-2]
        string += "},"
        print(string)

    f1_puncs = []
    f1_commas = []
    overall_f1s = []
    for human in human_to_res:
        f1_punc = human_to_res[human]["PERIOD"]["f1"]
        f1_comma = human_to_res[human]["COMMA"]["f1"]
        overall_f1 = (f1_punc + f1_comma)/2
        overall_f1s.append(overall_f1)
        f1_puncs.append(f1_punc)
        f1_commas.append(f1_comma)
        # print(human_to_res[human]["QUESTION"]["f1"])

    print(overall_f1s)
    print(f1_commas)
    print(np.std(np.array(f1_puncs)))
    print(np.std(np.array(f1_commas)))
    print(np.std(np.array(overall_f1s)))
