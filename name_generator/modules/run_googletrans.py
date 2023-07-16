from googletrans import Translator, LANGUAGES
from typing import List
import re


def get_multi_translation(text_list: list, input_lang: str, output_lang_list: List[str]):
    translations_dict = {}
    translator = Translator()
    for output_lang in output_lang_list:
        translations = translator.translate(text_list, dest=output_lang, src=input_lang)
        for translation in translations:
            translated_text = re.sub(r"^\W+", "", translation.text).lower()
            translated_text = re.sub(r"\W+$", "", translated_text)
            translated_text = translated_text if translation.origin != translated_text else None
            if translation.origin not in translations_dict.keys():
                translations_dict[translation.origin] = {LANGUAGES[output_lang]: translated_text}
            else:
                translations_dict[translation.origin][LANGUAGES[output_lang]] = translated_text
    return translations_dict

def get_single_translation(text: str, input_lang: str, output_lang: str):
    translator = Translator()
    # translate into Latin
    translation = translator.translate(text, dest=output_lang, src=input_lang)
    translated_text = re.sub(r"^\W+", "", translation.text).lower()
    translated_text = re.sub(r"\W+$", "", translated_text)
    if translation.origin == translated_text:
        translated_text = None
    language = LANGUAGES[output_lang]
    return translated_text, language