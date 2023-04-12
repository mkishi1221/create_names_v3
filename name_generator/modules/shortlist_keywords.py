#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from classes.keyword_class import Keyword
from modules.create_keyword import create_Keyword_Export
from pattern3.text.en import pluralize
from typing import List

limits = {
    "noun": 20,
    "verb": 10,
    "adjective": 10
}

limit_count = {
    "noun": 0,
    "verb": 0,
    "adjective": 0
}

def uniq(raw_list):
    uniq_list = []
    for item in raw_list:
        if item not in uniq_list:
            uniq_list.append(item)
    return uniq_list

required_pos = ["noun", "verb", "adjective", "abbreviation"]
shortlist_pos = ["noun", "verb", "adjective"]

def shortlist_keywords(
        sorted_keywords: List[Keyword]
    ):

    shortlisted_keywords = []

    for kw in sorted_keywords:
        word = kw.keyword
        origin = "/".join(kw.origins)
        pos_list = []
        for p in kw.pos_list:
            if p in required_pos:
                pos_list.append(p)
        try:
            shortlisted_pos = pos_list[0]
            if shortlisted_pos == "abbreviation":
                shortlisted_pos = "noun"
        except IndexError:
            shortlisted_pos = None
        origin = kw.origins

        for pos in pos_list:
            kw_dict = {word:pos}
            # Determine if keyword should be shortlisted
            # If word is user-specified in kw list, then shortlist.
            if pos == shortlisted_pos and "keywords" in origin:
                shortlist = "s"
            elif pos == shortlisted_pos and pos in shortlist_pos:
                shortlist = "s"
                limit_count[pos] = limit_count[pos] + 1
                if limit_count[pos] == limits[pos]:
                    shortlist_pos.remove(pos)
            else:
                shortlist = None

            # If kw is shortlisted ad noun, create plural version
            if pos == "noun":
                plural_noun = pluralize(word)
                if plural_noun[-2:] != "ss":
                    kw_dict[plural_noun] ="plural_noun"

            for w, p in kw_dict.items():
                shortlisted_keywords.append(
                    create_Keyword_Export(
                        origin,
                        p,
                        w, 
                        shortlist
                    )
                )
    return shortlisted_keywords
            
                