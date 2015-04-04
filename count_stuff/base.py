from collections import Counter


class BaseCountExtractor(object):
    """Extract something from a text corpus and store counts of uniques"""
    def __init__(self, corpus, cleaner=None):
        """Construct a CountExtractor
        :param corpus: File-like object providing lines of strings to extract data from
        :param cleaner: callable that determines whether a key should be removed
        """
        self.should_clean = False
        if hasattr(cleaner, '__call__'):
            self.should_clean = True
        self.keep_key = cleaner
        self._counter = Counter()
        self.text = corpus

    def extract_counts(self):
        """Override in subclasses to extract and count"""
        pass

    def _clean_counts(self):
        for key in self._counter.keys():
            if not self.keep_key(key):
                del self._counter[key]

    def get_counts(self):
        self.extract_counts()
        if self.should_clean:
            self._clean_counts()
        return self._counter
