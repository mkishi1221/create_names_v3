from classes.keyword_class import Keyword, Keyword_Export
import sys
import orjson as json
from typing import List, Dict
import copy
import os.path
from modules.process_text import process_text
from modules.pull_eng_dict import pull_eng_dict
from modules.shortlist_keywords import shortlist_keywords
from modules.create_modwords import create_modwords
import pandas as pd
import re


def generate_names(project_id):

    project_path: str = f"projects/{project_id}"

    # input file filepaths and filenames:
    sentences_tsv_fp: str = f"{project_path}/data/sentences.txt"
    user_words_tsv_fp: str = f"{project_path}/data/keywords.txt"

    # tmp file filepaths and filenames:
    keyword_list_keywords_json_fp: str = f"{project_path}/tmp/keyword_generator/{project_id}_keywords_from_keyword-list.json"
    sentences_keywords_json_fp: str = f"{project_path}/tmp/keyword_generator/{project_id}_keywords_from_sentences.json"
    rated_kw_tmp_json_fp: str = f"{project_path}/tmp/keyword_generator/{project_id}_all_keywords.json"
    keywords_json_fp: str = f"{project_path}/tmp/logs/{project_id}_keywords.json"

    # output filepaths and filenames:
    excel_output_fp: str = f"{project_path}/results/{project_id}_keywords.xlsx"

    # Open dictionaries and resources:
    eng_dict: dict = pull_eng_dict()
    eng_dict_words: list = list(eng_dict.keys())
    curated_eng_words = set(open("name_generator/curated_eng_words.txt", "r").read().splitlines())
    blacklist = open("name_generator/dict/default_blacklist.txt", "r").read().splitlines()

    # Set variable defaults
    all_keywords: List[Keyword] = []
    sentences: List[str] = []    
    not_valid = [None, ""]
    master_data_dict = {}

    # Check if sentences exists and create keywords from sentences
    block_text = open(sentences_tsv_fp, "r").read() if os.path.exists(sentences_tsv_fp) else ""
    word_list = open(user_words_tsv_fp, "r").read() if os.path.exists(user_words_tsv_fp) else ""
    
    # Extract keywords from sentences
    if len(block_text) != 0:
        # Apply some formatting to block of text
        print("Processing block text...")
        block_text = block_text.replace("/", " / ")
        block_text = re.sub(" +", " ", block_text)

        # Split block text into list of lines
        lines = [ln.strip() for ln in block_text.splitlines() if ln.strip() not in not_valid and len(ln.strip()) > 0]
        line_len = len(lines)

        # Extract sentences and Keywords from each line using Spacy
        for line_count, line in enumerate(lines):
            print(f"Processing line {line_count+1} out of {line_len}...", end="\r")
            all_keywords, sentences = process_text(
                "sentences",
                project_path,
                project_id,
                line,
                all_keywords,
                eng_dict,
                eng_dict_words,
                sentences
            )
        
        # Add extracted sentences to master_data_dict
        sys.stdout.write("\033[K")
        print(f"Processed all {line_len} lines.")
    else:
        print("Skipping block text...")

    # Extract keywords from keyword list
    if len(word_list) != 0:
        print("Processing word_list...")
        all_keywords, ignore = process_text(
            "keywords",
            project_path,
            project_id,
            word_list,
            all_keywords,
            eng_dict,
            eng_dict_words
        )
    else:
        print("Skipping word list...")

    # Check if any keywords have been extracted; if no keywords are extracted, quit program.
    # Sort the keywords to relevancy, occurrance and alphabetical order and add them to master_data_dict.
    # Shortlist relevant keywords and create modwords from shortlisted keywords
    keyword_count = len(all_keywords)
    if keyword_count > 0:
        print(f"{keyword_count} keywords collected....")
        sorted_keywords = sorted(
            all_keywords, key=lambda k: (k.yake_score, -k.occurrence, k.keyword)
        )
        print(f"Shortlisting keywords....")
        # Choose keywords to create names from
        shortlisted_keywords = shortlist_keywords(sorted_keywords)
        # Create modwords from shortlisted keywords
        modwords = create_modwords(shortlisted_keywords, eng_dict, curated_eng_words)
    else:
        print('No keywords extracted! Please add source data to the "data" folder.')
        quit()
    
    

    # Create final output file
    print("Exporting output to excel....")
    master_data_dict["modwords"] = modwords
    master_data_dict["keyword_shortlist"] = shortlisted_keywords
    master_data_dict["keyword_groups"] = sorted_keywords
    master_data_dict["sentences"] = sentences
    writer = pd.ExcelWriter(excel_output_fp, engine='xlsxwriter')
    workbook  = writer.book
    for sheet in list(master_data_dict.keys()):
        df = pd.DataFrame.from_dict(master_data_dict[sheet], orient="columns")
        df.to_excel(writer, sheet_name=sheet)
        worksheet = writer.sheets[sheet]
        worksheet.set_column(1, 19, 15)
    writer.save()

if __name__ == "__main__":
    generate_names(sys.argv[1])