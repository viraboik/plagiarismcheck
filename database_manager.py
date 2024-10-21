import abc
from collections import defaultdict

from utils import split_text_by_words, make_moving_windows


class Document:
    pass


class SearchResult:
    pass


class SimilarTextsByExactWordsMatch(SearchResult):
    def __init__(self, plagiarism_percentage: float, docs_similarity: list[tuple[int, float]]):
        self.plagiarism_percentage: float = plagiarism_percentage
        self.docs_similarity: list[tuple[int, float]] = docs_similarity


class ABCDatabase(abc.ABC):
    @abc.abstractmethod
    def add_text(self, text: str) -> int:
        pass

    @abc.abstractmethod
    def search_similar_texts_by_distance(self, id, threshold: float = 0.9) -> list[SearchResult]:
        """
        Cosine similarity (Bag of words)
        """
        pass

    @abc.abstractmethod
    def search_similar_texts_by_exact_words_match(self, id, threshold: float = 0.9) -> list[SearchResult]:
        """
        Cosine similarity (Bag of words)
        """
        pass


class InMemoryDocument:
    def __init__(self, _id: int, text: str):
        self.text = text
        self.id = _id

        self.words = split_text_by_words(text)
        self.words_in_moving_window = make_moving_windows(self.words)
        self.plagiarized_words = [[w, False, set()] for w in self.words]


class InMemoryDatabase(ABCDatabase):
    def __init__(self):
        self.current_index = 0
        self.data: dict[int, str] = {}

        self.window_words: dict[tuple[str]: list[InMemoryDocument]] = defaultdict(list)

    def add_text(self, text: str) -> InMemoryDocument:
        document = InMemoryDocument(self.current_index, text)
        self.data[self.current_index] = InMemoryDocument(self.current_index, text)
        self.current_index += 1

        for window in document.words_in_moving_window:
            key = self.get_key_from_window(window)
            self.window_words[key].append(document)

        return document

    @staticmethod
    def get_key_from_window(window):
        key = [w.lower() for w, s, e in window]
        key = tuple(key)
        return key

    def search_similar_texts_by_distance(self, id, threshold: float = 0.9) -> list[SearchResult]:
        pass

    def search_similar_texts_by_exact_words_match(self, id, threshold: float = 0.9) -> list[
        SimilarTextsByExactWordsMatch]:
        document: InMemoryDocument = self.data[id]

        # шукаємо подібні
        similar_ids: set[int] = set()
        for index, window in enumerate(document.words_in_moving_window):
            key = self.get_key_from_window(window)
            list_of_documents = self.window_words[key]
            list_of_documents_ids: set = {doc.id for doc in list_of_documents}
            list_of_documents_ids -= {document.id}

            similar_ids |= set(list_of_documents_ids)

            if not list_of_documents_ids:
                continue

            # TODO: add document mutation
            for word_index, word in enumerate(window):
                document.plagiarized_words[index + word_index][1] = True
                document.plagiarized_words[index + word_index][2] |= list_of_documents_ids

        all_words = len(document.words)
        plagiarized_words = len([word_info[1] for word_info in document.plagiarized_words if word_info[1]])
        plagiarized_metric = plagiarized_words / all_words

        return plagiarized_metric


if __name__ == '__main__':
    dataset = [
        "aa bb cc dd ee",
        "tt yy uu ii this is not plagiarized text qq ww ee"
    ]

    db = InMemoryDatabase()
    for text in dataset:
        db.add_text(text)

    text_for_check = "This  iS  nOt  PlaGiaRized text pp ll qq aa bb cc dd =)"
    document = db.add_text(text_for_check)

    result = db.search_similar_texts_by_exact_words_match(document.id)
    print(result)
