#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from modules.collect_algorithms import collect_algorithms
from modules.keyword_abbreviator import keyword_abbreviator
from classes.keyword_class import Keyword_Export
from classes.keyword_class import Modword

pos_conversion = {
    "adjective": "adje",
    "adverb": "advb",
    "plural_noun": "plrn"
}

def create_Modword(
        word: str,
        pos: str,
        modifier: str,
        modword: str
    ):
    return Modword(
        keyword=word,
        pos=pos,
        modifier=modifier,
        modlen=len(modword),
        modword=modword
    )

def create_modwords(shortlisted_keywords, eng_dict, curated_eng_words):

    # Get list of all the algorithms required
    raw_algorithms = collect_algorithms()

    # Get list of all modifications required for each pos
    required_comps = {}
    for algorithm in raw_algorithms:
        for component in algorithm.components:
            if component.pos not in required_comps.keys():
                required_comps[component.pos] = {component.modifier}
            elif component.modifier not in required_comps[component.pos]:
                required_comps[component.pos].add(component.modifier)

    # Filter to just shortlisted words
    shortlisted_keywords = [kw for kw in shortlisted_keywords if kw.shortlist == "s"]
    modword_list = []

    # Create modwords for each shortlisted keyword
    kw: Keyword_Export
    for kw in shortlisted_keywords:
        word = kw.keyword
        pos = kw.pos
        # If pos is adj or adv, convert to 4 letter format
        if pos in pos_conversion.keys():
            pos = pos_conversion[pos]

        # Add unmodified word
        modword_list.append(
            create_Modword(
                word,
                pos,
                "no_cut",
                word
            )
        )

        # If required, add "cut words"
        # ab_cut stands for abbreviation_cut: more modifiers coming soon!
        if "ab_cut" in required_comps[pos]:
            try:
                components = eng_dict[word]["component_list"]
            except KeyError:
                components = None
            abbreviations = keyword_abbreviator(word, components, curated_eng_words)
            for ab in abbreviations:
                modword_list.append(
                    create_Modword(
                        word,
                        pos,
                        "ab_cut",
                        ab
                    )
                )

    return modword_list