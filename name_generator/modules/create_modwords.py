#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from modules.collect_algorithms import collect_algorithms
from modules.keyword_abbreviator import keyword_abbreviator
from modules.run_googletrans import get_single_translation
from classes.keyword_class import Keyword_Export
from classes.keyword_class import Modword
from transliterate import translit

pos_conversion = {
    "adjective": "adje",
    "adverb": "advb",
    "plural_noun": "plrn"
}

def create_Modword(
        word: str,
        yake_score: float,
        modifier: str,
        pos: str,
        modword: str,
        lang: str = "English"
    ):
    return Modword(
        keyword=word,
        relevance=yake_score,
        modifier=modifier,
        lang=lang,
        pos=pos,
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
    all_modwords = set()

    # Create modwords for each shortlisted keyword
    kw: Keyword_Export
    for kw in shortlisted_keywords:
        word = kw.keyword
        pos = kw.pos
        yake_score = kw.relevance
        # If pos is adj or adv, convert to 4 letter format
        if pos in pos_conversion.keys():
            pos = pos_conversion[pos]

        # Add unmodified word
        if word not in all_modwords:
            all_modwords.add(word)
            modword_list.append(create_Modword(
                    word,
                    yake_score,
                    "no_cut",
                    pos,
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
                        yake_score,
                        "ab_cut",
                        pos,
                        ab
                    )
                )

        output_lang_list = ["la", "el"]
        for output_lang in output_lang_list:
            translation, language = get_single_translation(word, "en", output_lang)
            if translation is not None and " " not in translation:
                if output_lang == "el":
                    translation = translit(translation, 'el', reversed=True)
                modword_list.append(
                    create_Modword(
                        word,
                        yake_score,
                        "no_cut",
                        pos,
                        translation,
                        lang=language
                    )
                )

    return modword_list