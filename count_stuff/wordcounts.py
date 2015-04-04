import argparse
import codecs
from functools import partial

from base import BaseCountExtractor
from geo_data import ALPHABET, WHITESPACE, PUNCTUATION, DIGITS_ROMAN, DIGITS_LATIN


################
## EXTRACTORS ##
################
class CharCountExtractor(BaseCountExtractor):
    """Counts unique characters"""
    def extract_counts(self):
        for line in self.text:
            for char in line:
                self._counter[char] = self._counter[char] + 1


class WordCountExtractor(BaseCountExtractor):
    """Counts unique words"""
    def extract_counts(self):
        for line in self.text:
            for word in line.split():
                self._counter[word] = self._counter[word] + 1


class BigramCountExtractor(BaseCountExtractor):
    """Counts unique bigrams"""
    def store_bigram(self, first, second):
        """Stores "{first} {second}" in self._counter"""
        index = u'{} {}'.format(first, second)
        self._counter[index] = self._counter[index] + 1

    def extract_counts(self):
        """Get bigrams from text"""
        previous = None
        current = None
        for line in self.text:
            for word in line.split():
                previous = current
                current = word
                if previous is None:
                    continue
                self.store_bigram(previous, current)

########################
## CLEANING FUNCTIONS ##
########################
def all_in_charset(chars, string):
    """Returns true if string's characters are in chars, false otherwise
    :param chars: Set of characters to test characters in string against
    :param string: The string to test
    :return bool: Whether the characters in string are wholly within chars"""
    for c in string:
        if c not in chars:
            return False
    return True


def at_least_one_in_charset(must_chars, limit_chars, string):
    """Returns true if all string's chars are in limit_chars and at least one is in must_chars"""
    found_one = False
    for c in string:
        if c not in limit_chars:
            return False
        if c in must_chars:
            found_one = True
    return found_one

# Output
def output(counter, top_n=None, output_counts=True):
    """Prints a counter with optional formatting
    :param counter: A Counter object to print
    :param top_n: The top N most common terms to print (default print all)
    :param output_counts: If true, prints term followed by count, separated by tab
    """
    if output_counts:
        def printer(n):
            return codecs.encode(u'{term}\t{count}'.format(term=n[0], count=n[1]), 'utf-8')
    else:
        def printer(n):
            return codecs.encode(n[0], 'utf-8')
    for n in counter.most_common(top_n):
        print(printer(n))

EXTRACTOR_CLASSES = {'characters': CharCountExtractor,
                     'words': WordCountExtractor,
                     'bigrams': BigramCountExtractor,
                     'punctuation': WordCountExtractor,
                     'numbers': WordCountExtractor}


def run(args):
    extractor_cls = EXTRACTOR_CLASSES[args.count_what]
    with codecs.open(args.corpus, encoding='utf-8') as text_file:
        if args.clean:
            if args.count_what == 'bigrams':
                clean_charset = ALPHABET | WHITESPACE
                cleaner = partial(all_in_charset, clean_charset)
            elif args.count_what == 'punctuation':
                limit_charset = ALPHABET | WHITESPACE | PUNCTUATION
                must_charset = PUNCTUATION
                cleaner = partial(at_least_one_in_charset, must_charset, limit_charset)
            elif args.count_what == 'numbers':
                clean_charset = DIGITS_LATIN | DIGITS_ROMAN
                cleaner = partial(all_in_charset, clean_charset)
            else:
                clean_charset = ALPHABET
                cleaner = partial(all_in_charset, clean_charset)
            extractor = extractor_cls(text_file, cleaner=cleaner)
        else:
            extractor = extractor_cls(text_file)

        counts = extractor.get_counts()

    output(counts, top_n=args.top_n, output_counts=args.no_counts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str, help='File containing corpus of text to read')
    parser.add_argument('--top-n', type=int, help='Top N terms to output (default all)')
    parser.add_argument('--no-counts', action='store_false',
                        help='Whether to output counts alongside terms (counts are outputted by default)')
    parser.add_argument('--clean', action='store_true',
                        help='Remove any strings containing non-Georgian alphabetic characters')
    parser.add_argument('--count-what', type=str,
                        help='Things to count: "characters", "words", "bigrams"',
                        default='words')
    args = parser.parse_args()

    run(args)
