#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def keyword_abbreviator(keyword: str, component_list: str, curated_eng_list: list):
    
    illegal_len = [0, 1, 2, len(keyword)]
    modword_list = set()
    vowels = "aiueo"

    if component_list is not None:
        for components in component_list:
            split_components = components.split("·")
            abbreviation = ""
            for index, component in enumerate(split_components):
                if index != len(split_components)-1:
                    abbreviation = abbreviation + component
                    abbreviations = [abbreviation]
                    try:
                        abbreviations.append(abbreviation[:-1])
                    except IndexError:
                        pass
                    try:
                        i = 0
                        x = split_components[index+1][i]
                        s = split_components[index+1][0:i+1]
                        abbreviations.append(abbreviation + split_components[index+1][0])
                        try:
                            while x not in vowels:
                                i = i + 1
                                x = split_components[index+1][i]
                                s = split_components[index+1][0:i+1]
                            abbreviations.append(abbreviation + s)
                        except IndexError:
                            pass
                    except IndexError:
                        pass
                    for ab in abbreviations:
                        if len(ab) not in illegal_len:
                            modword_list.add(ab)
        if len(keyword) > 4:
            modword_list.add(keyword[:-1])
            modword_list.add(keyword[:-2])
    
    return sorted(modword_list)