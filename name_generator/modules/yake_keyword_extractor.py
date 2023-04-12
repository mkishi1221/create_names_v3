#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import yake
import re

def yake_keyword_extractor(sentences: str, keywords_dict: dict = None):

    if keywords_dict is None:
        keywords_dict = {}

    # Set Yake settings
    if sentences is not None:
        language = "en"
        max_ngram_size = 1
        deduplication_thresold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        numOfKeywords = 1000
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
        ranked_keywords_list = custom_kw_extractor.extract_keywords(sentences)
  
        for kw in ranked_keywords_list:
            # Format keyword 
            keyword = re.sub(r"^\W+", "", kw[0]).lower()
            keyword = re.sub(r"\W+$", "", keyword)
            yake_score = kw[1]
            # Add to dict: if the same keyword appears multiple times, get lowest score.
            if keyword not in keywords_dict.keys():
                keywords_dict[keyword] = {"yake_score": yake_score}
            else:
                prev_score = keywords_dict[keyword]["yake_score"]
                if prev_score > yake_score:
                    keywords_dict[keyword] = {"yake_score": yake_score}

    else:
        raise Exception(f"Data: \"{sentences}\" - No sentences detected!")

    return keywords_dict

