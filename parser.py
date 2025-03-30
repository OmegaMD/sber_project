from difflib import SequenceMatcher

class Parser:
    def __init__(self, words):
        self.words = words

    def parse(self, query):
        scores = {}
        query_lower = query.lower()

        for word in self.words:
            scores[word] = 0

            variants = self.words[word]

            for var in variants:
                ratio = SequenceMatcher(None, var, query_lower).ratio()
                if scores[word] < ratio:
                    scores[word] = ratio

        result = 'None'
        best_score = 0

        for score_word in scores:
            if best_score < scores[score_word]:
                result = score_word
                best_score = scores[score_word]
                
        return result