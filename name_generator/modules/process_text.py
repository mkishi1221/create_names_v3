#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.keyword_class import Keyword
from modules.yake_keyword_extractor import yake_keyword_extractor
from modules.generate_hard_lemma import generate_hard_lemma,fetch_pos_w_hardlemma
from modules.pull_eng_dict import fetch_eng_dict_pos, convert_spacy_pos
from modules.create_keyword import create_Keyword_dict
import regex as re
import spacy
from nltk.stem import WordNetLemmatizer

nlp = spacy.load(
    "en_core_web_lg",
    exclude=[
        "ner",
        "entity_linker",
        "entity_ruler",
        "textcat",
        "textcat_multilabel",
        "morphologizer",
        "senter",
        "sentencizer",
        "transformer",
    ],
)

def uniq(raw_list):
    uniq_list = []
    for item in raw_list:
        if item not in uniq_list:
            uniq_list.append(item)
    return uniq_list

def process_text(
        origin,
        project_path, 
        project_id, 
        line: str, 
        keywords: List[Keyword], 
        eng_dict, 
        eng_dict_words,
        sentences: List[str]=None
    ):

    invalid = [None, "", []]
    illegal_char = re.compile(r"[^a-zA-Z]")
    removed_keywords = set()

    # Convert Keyword list into Dict for easier management
    keywords_dict = {}
    if len(keywords) > 0:
        for kw in keywords:
            keywords_dict[kw.keyword] = kw

    # Process each line using Spacy
    # Spacy divides sentences ("sent") into words ("tokens").
    # Tokens can also be symbols and other things that are not full words.
    doc = nlp(line)
    not_valid = [None, ""]
    for sent in doc.sents:

        if origin == "sentences":
            # Run sent through Yake to find most relevant keywords.
            yake_scores = yake_keyword_extractor(str(sent))
            # Break down line into sentences and add them to list of sentences
            sentences.append({"sentence": str(sent)})
    
        # Loop through each word in sentence
        for token in sent:

            # Format word
            source_word = token.text
            word = re.sub(r"^\W+", "", source_word).lower()
            word = re.sub(r"\W+$", "", word)

            # Filter words that are shorter than 3 letters
            # Filter words that have characters other than alphabet
            if len(word) > 2 and not bool(illegal_char.search(word)):
                spacy_pos = token.pos_
                spacy_lemma = token.lemma_
                nltk_lemma = None
                hard_lemma = None

                # Fetch yake score. If word not in yake keyword list, yake_score = 1
                # If word is from word_list, yake score = 0
                if origin == "sentences":
                    try:
                        yake_score = yake_scores[word]["yake_score"]
                    except KeyError:
                        yake_score = 1
                else:
                    yake_score = 0

                # Get all possible pos using word and spacy lemma
                pos_list = []
                pos_list.extend(fetch_eng_dict_pos(word, eng_dict, eng_dict_words))
                pos_list.extend(fetch_eng_dict_pos(spacy_lemma, eng_dict, eng_dict_words))
                pos_list = uniq(pos_list)
                
                # If pos list is still empty, try using nltk lemma
                if len(pos_list) == 0:
                    lemmatizer = WordNetLemmatizer()
                    nltk_lemma = lemmatizer.lemmatize(word)
                    fetched_pos_list = fetch_eng_dict_pos(nltk_lemma, eng_dict, eng_dict_words)
                    if len(fetched_pos_list) > 0:
                        word = nltk_lemma
                        pos_list.extend(fetched_pos_list)
                        pos_list = uniq(pos_list)

                # If pos list is still empty, create extra keyword using hard_lemma.
                # If spacy_pos is valid, use Spacy Pos, else add pos as invalid.
                if len(pos_list) == 0:
                    hard_lemma = generate_hard_lemma(word)
                    if hard_lemma is not None:
                        fetched_pos_list, hard_lemma_str = fetch_pos_w_hardlemma(hard_lemma, eng_dict, eng_dict_words)
                        if len(fetched_pos_list) > 0:
                            pos_list.extend(fetched_pos_list)
                            pos_list = uniq(pos_list)
                            keywords_dict = create_Keyword_dict(
                                keywords_dict, 
                                hard_lemma_str, 
                                origin, 
                                source_word, 
                                spacy_pos, 
                                fetched_pos_list,
                                yake_score,
                                spacy_lemma,
                                nltk_lemma,
                                hard_lemma
                            )
                
                # If pos list is still empty, use Spacy's POS
                if len(pos_list) == 0:
                    if spacy_pos not in invalid:
                        pos_list.append(convert_spacy_pos(spacy_pos))
                    else:
                        pos_list.append("invalid")

                keywords_dict = create_Keyword_dict(
                    keywords_dict, 
                    word, 
                    origin, 
                    source_word, 
                    spacy_pos, 
                    pos_list,
                    yake_score,
                    spacy_lemma,
                    nltk_lemma
                )

            else:
                removed_keywords.add(source_word)

    # Convert keyword dict back to list
    keywords = list(keywords_dict.values())

    if origin == "sentences":
        # Export removed keywords list from sentences for bug fix
        with open(f"{project_path}/tmp/keyword_generator/{project_id}_removed_keywords.json", "wb+") as out_file:
            out_file.write(str('\n'.join(removed_keywords)).encode())

    return keywords, sentences
