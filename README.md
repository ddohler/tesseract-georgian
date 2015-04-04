# tesseract-georgian
 A set of files used to train [tesseract](https://code.google.com/p/tesseract-ocr/) to read Georgian
 Mkhedruli script.

## File manifest

- **kat.word.bigrams.clean**: A list of the 40,000 most frequent word bigrams in the text of the Georgian-language Wikipedia, in descending order of frequency
- **kat.wordlist.clean**: A list of all unique words in the text of the Georgian-language Wikipedia, in descending order of frequency.
- **kat.unicharambigs**: A manually generated file of character ambiguities following tesseract's [unicharambigs](https://tesseract-ocr.googlecode.com/git/doc/unicharambigs.5.html) format
- **kat.training_text**: A text to use with tesstrain.sh or text2image to generation training images for tesseract.
- **font_properties**: A manually generated file containing the attributes of the fonts that I used to train tesseract, in tesseract's [font\_properties](https://code.google.com/p/tesseract-ocr/wiki/TrainingTesseract3) format
- **count_stuff**: Folder of Python scripts for generating bigrams and wordlists

## Procedure
Steps I took to generate the training files

### kat.training\_text
This file is based off the
[text](https://code.google.com/p/tesseract-ocr/source/browse/kat/kat.training_text?repo=langdata)
available in the langdata repository, with the following manual modifications:

- As noted [here](https://code.google.com/p/tesseract-ocr/issues/detail?id=1376), the text in the langdata repository contains characters from archaic Georgian scripts that are not used in modern Georgian. These characters have been removed.
- Several samples of the numero character (№), which is fairly frequent in modern Georgian texts, have been added.
- Examples of Roman numerals have been added; these are often used in Georgian texts for ordinal numbers.

### kat.wordlist.clean / kat.word.bigrams.clean
These files were generated using a database dump from Wikipedia roughly as follows:

1. Download latest Georgian database dump from Wikipedia:
https://dumps.wikimedia.org/backup-index.html

2. Run [WikiExtractor.py](https://github.com/bwbaugh/wikipedia-extractor) to extract the Georgian
text

3. Concatenate output into a single file with `find -type f <extraction_folder> | xargs cat >
kawikitext.txt`

4. Remove remaining <doc> tags with `sed -i '/^<doc/ d'` and `sed -i '/^<\/doc/ d'`

5. Run `python count_stuff/word_counts.py --count-what [words|bigrams] --clean --no-counts
kawikitext.txt > [kat.wordlist.clean|kat.word.bigrams.clean.full]` to extract words and/or bigrams from
the Wikipedia text

6. Run `head -n 40000 kat.word.bigrams.clean.full > kat.word.bigrams.clean` in order to limit the
number of bigrams, which would otherwise be very large (~2 million)

### font\_properties
I selected fonts that were freely licensed, and which included monospace, serif, and sans-serif
fonts. In addition, there are several Georgian letters which can be written with different glyphs,
so I made sure to include fonts which cover both glyphs (see
[here](https://code.google.com/p/tesseract-ocr/issues/detail?id=1376) for details). A good selection
of freely-licensed, Unicode Georgian fonts is available from [BPG
InfoTech](https://bpgfonts.wordpress.com). Other fonts are available in various places, but note
that many commonly used Georgian fonts, such as AcadNusx and LitNusx, map Georgian glyphs onto Latin
letters, making them unsuitable for automatically generating training images.

## Training tesseract
Tesseract was trained using
[tesstrain.sh](https://tesseract-ocr.googlecode.com/git/training/tesstrain.sh) without any
modifications (except manual application of [this
patch](https://code.google.com/p/tesseract-ocr/issues/detail?id=1311)).

The specific command executed to train tesseract was:

```
./tesstrain.sh \
        --bin_dir /usr/local/bin/ \
        --fonts_dir /usr/share/fonts/ \
        --lang kat \
        --langdata_dir /home/pi/tesseract/kat_train/staging/ \
        --output_dir /home/pi/tesseract/kat_train/output/ \
        --training_text /home/pi/tesseract/kat_train/staging/kat.training_text \
        --wordlist /home/pi/tesseract/kat_train/staging/kat.wordlist.clean \
        --tessdata_dir /usr/local/share/tessdata \
        --fontlist "BPG Chkoni+BPG Chveulebrivi GPL&GNU+BPG Classic Medium,+BPG Courier GPL&GNU+BPG DedaEna+BPG Elite GPL&GNU+BPG Glaho GPL&GNU+BPG Glaho Traditional Arial+BPG Lia+BPG Rioni+Sylfaen"
```
(Yes, this was done on a Raspberry Pi.)

## Other notes
The `count\_stuff.py` script can theoretically also generate files containing punctuation and
numeral patterns, which tesstrain.sh can use to create DAWG files for punctuation and numbers.
However, I decided to forgo using these files in order to simplify the first pass at training, and
the results ended up being good enough that I haven't seen the need to add the punctuation and
number pattern files so far, so this feature of count\_stuff.py may not work perfectly / at all.

## License
Copyright 2015, Derek Dohler.
I do not claim any copyright over kat.wordlist.clean or kat.word.bigrams.clean.
I claim copyright over only the alterations which I made to kat.training_text, and not over the remainder of the file.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
