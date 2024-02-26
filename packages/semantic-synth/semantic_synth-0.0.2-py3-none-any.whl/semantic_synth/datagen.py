import pysbd

import yake
import pandas as pd
import spacy

import abc
from abc import ABC, abstractmethod

import random
import uuid

class DatasetGenerator(ABC):

    @abstractmethod
    def generate(self, content: str = None, num_results: int = 5):
        pass

    def generate_as_df(self, content: [str] = None, num_results: int = 5):

        def get_search_terms(text):

            keywords = self.generate(
                content = text,
                num_results = num_results
            )

            return {
                    "text": text,
                    "search_terms": keywords,
                }

        output = list(
            map(
                get_search_terms, content
            )
        )

        df = pd.DataFrame.from_dict(output)

        return df

class KeywordDatasetGenerator(DatasetGenerator):
    def __init__(
        self,
        max_ngram_size: int = 5,
        min_ngram_size: int = 1,
        dedup_threshold = 0.5,
        language: str = "en"
    ):

        self.max_ngram_size = max_ngram_size
        self.min_ngram_size = min_ngram_size
        self.dedup_threshold = dedup_threshold
        self.language = language

    def filter_ents(self, keywords):
        NER = spacy.load("en_core_web_sm")
        
        filtered = []
        for phrase in keywords:
            ents = NER(phrase)
            if len(ents.ents) > 0:
                filtered.append(phrase)
        return filtered

    def generate(
        self,
        content: str = None,
        num_results: int = 5,
        filter_for_entities: bool = True
    ):
        custom_kw_extractor = yake.KeywordExtractor(
            lan=self.language,
            n = self.max_ngram_size,
            dedupLim = self.dedup_threshold,
            top = num_results,
            features=None
            )
        keywords = custom_kw_extractor.extract_keywords(content)
        keywords = [
            keyword[0] for keyword in keywords if (len(keyword[0].split(" ")) <= self.max_ngram_size) and (len(keyword[0].split(" ")) >= self.min_ngram_size)
        ]

        if filter_for_entities:
            keywords = self.filter_ents(keywords)
            
        return keywords

class SentenceDatasetGenerator(DatasetGenerator):
    def generate(
        self,
        content: str = None,
        num_results: int = 3
    ):
        if content is None:
            raise Exception("Content was not provided, please provide content")

        seg = pysbd.Segmenter(language="en", clean=False)

        content = content.replace("\n", "")

        res = seg.segment(content)

        sentence_positions = [random.randint(0, len(res)) for i in range(num_queries)]

        sentences = [res[i] for i in sentence_positions]

        return sentences

