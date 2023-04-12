#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import orjson as json
import re

not_valid = [None, ""]

def pull_eng_dict():

    eng_dict_fp = "../wordsAPI/simplified_eng_dict.json"
    with open(eng_dict_fp) as eng_dict_file:
        eng_dict_data = json.loads(eng_dict_file.read())

    return eng_dict_data

def convert_to_nltk_pos(pos_str: str):
    pos_conversion = {
        "noun": "n",
        "verb": "v",
        "adjective": "a",
        "adverb": "r",
    }
    if pos_str in pos_conversion.keys():
        pos_str = pos_conversion[pos_str]
    else:
        print(f"Passed illegal pos_str: {pos_str}")
        quit()
    return pos_str

def convert_spacy_pos(spacy_pos: str):
    pos_conversion = {
        "NOUN": "noun",
        "VERB": "verb",
        "ADJ": "adjective",
        "ADV": "adverb",
        "DET": "definite article",
        "CCONJ": "conjunction",
        "ADP": "adposition",
        "PART": "preposition",
        "PROPN": "noun",
        "PRON": "pronoun",
        "SCONJ":"subordinating_conjunction",
        "AUX":"auxiliary_verb",
        "PUNCT":"punctuation"
    }
    if spacy_pos is not None and spacy_pos.strip() in pos_conversion.keys():
        spacy_pos = pos_conversion[spacy_pos]

    return spacy_pos

def fetch_eng_dict_pos(keyword, eng_dict: dict, eng_dict_words: list) -> list[str]:

    # Get all "parts of speech" (pos) associated with each keyword.
    # If keyword is None or not in eng_dict dictionary, return pos as None.
    numbers_as_str = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"
    ]
    if keyword not in not_valid:
        # Check if keyword is a number (Integer and float). If number, pos is NUM.
        if re.match('.*\d.*', keyword) or keyword.lower() in numbers_as_str:
            all_pos = ["number"]
        elif keyword in eng_dict_words:
            # Check if keyword and it's definition/pos data is in eng_dict dictionary.
            all_pos = eng_dict[keyword]["pos_list"]
        else:
            all_pos = []
    return all_pos