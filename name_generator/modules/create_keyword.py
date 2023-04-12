#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import List
from classes.keyword_class import Keyword, Keyword_Export

not_valid = [None, ""]

def create_keyword(
        origin: str,
        source_word: str, 
        word: str, 
        spacy_pos_str: str, 
        pos_list: List[str],
        word_lemma: str, 
        nltk_lemma: str,
        hard_lemma: dict,
        yake_score: float
    ) -> Keyword:

    return Keyword(
        origins=[origin],
        source_words=[source_word],
        spacy_lemma=word_lemma,
        nltk_lemma=nltk_lemma,
        hard_lemma=hard_lemma,
        keyword_len=len(word),
        yake_score=yake_score,
        spacy_pos=spacy_pos_str,
        pos_list= pos_list,
        occurrence=1,
        keyword=word
    )

def create_Keyword_dict(
        keywords_dict: dict, 
        word, 
        origin, 
        source_word, 
        spacy_pos, 
        pos_list,
        yake_score,
        spacy_lemma=None,
        nltk_lemma=None,
        hard_lemma=None
    ):
    # Create Keyword object or update existing Keyword object
    if word not in not_valid and word not in keywords_dict.keys():
        keywords_dict[word] = create_keyword(
            origin,
            source_word, 
            word, 
            spacy_pos,
            list(pos_list),
            spacy_lemma, 
            nltk_lemma,
            hard_lemma,
            yake_score
        )
    else:
        if source_word not in keywords_dict[word].source_words:
            keywords_dict[word].source_words.append(source_word)
        keywords_dict[word].occurrence += 1
        prev_score = keywords_dict[word].yake_score
        if prev_score > yake_score:
            keywords_dict[word].yake_score = yake_score
        if origin not in keywords_dict[word].origins:
            keywords_dict[word].origins.append(origin)
    return keywords_dict

def create_Keyword_Export(
        origin: str,
        pos: str,
        word: str, 
        shortlist: str
    ) -> Keyword_Export:

    return Keyword_Export(
        origin=origin,
        pos=pos,
        keyword=word,
        shortlist=shortlist
    )

def create_Keyword_shortlist(
        keyword_shortlist: list[Keyword_Export],
        origin: str,
        pos: str,
        word: str, 
        shortlist: str
    ):
    kw_obj = create_Keyword_Export(
        origin,
        pos,
        word, 
        shortlist
    )
    if kw_obj not in keyword_shortlist:
        keyword_shortlist.append(kw_obj)
    return keyword_shortlist
