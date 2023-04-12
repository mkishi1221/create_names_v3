from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List

@dataclass_json
@dataclass
class Keyword:
    """
    A simple helper class for keywords adding a comparator for better readability
    """
    origins: List[str] = None
    source_words: List[str] = None
    spacy_lemma: str = None
    nltk_lemma: str = None
    hard_lemma: dict = None
    spacy_pos: str = None
    pos_list: List[str] = None
    keyword_len: int = 0
    yake_score: float = None
    occurrence: str = None
    keyword: str = None

    def __eq__(self, o: object) -> bool:
        return self.keyword == o.keyword

    def __ne__(self, o: object) -> bool:
        return self.keyword != o.keyword

    def __hash__(self) -> int:
        return hash((self.keyword))

    def __repr__(self) -> str:
        return str(
            {
                key: self.__dict__[key]
                for key in self.__dict__
                if self.__dict__[key] is not None
            }
        )

@dataclass_json
@dataclass
class Keyword_Export:
    origin: str = None
    pos: str = None
    keyword: str = None
    shortlist: str = None

    def __eq__(self, o: object) -> bool:
        return self.keyword == o.keyword and self.pos == o.pos

    def __ne__(self, o: object) -> bool:
        return self.keyword != o.keyword and self.pos != o.pos

    def __hash__(self) -> int:
        return hash((self.keyword, self.pos))

    def __repr__(self) -> str:
        return str(
            {
                key: self.__dict__[key]
                for key in self.__dict__
                if self.__dict__[key] is not None
            }
        )

@dataclass_json
@dataclass
class Modword:
    keyword: str = None
    pos: str = None
    modifier: str = None
    modlen: int = None
    modword: str = None

    def __eq__(self, o: object) -> bool:
        return self.modword == o.modword and self.keyword == o.keyword and self.pos == o.pos

    def __ne__(self, o: object) -> bool:
        return self.modword != o.modword and self.keyword != o.keyword and self.pos != o.pos

    def __hash__(self) -> int:
        return hash((self.source_word, self.keyword_len, self.keyword, self.modword, self.pos))

    def __repr__(self) -> str:
        return str(
            {
                key: self.__dict__[key]
                for key in self.__dict__
                if self.__dict__[key] is not None
            }
        )