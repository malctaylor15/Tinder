import nltk
from Helpers import fileIO
import string
import re

# nltk.download('punkt')
# nltk.download('stopwords')

APOSTROPHE = '\u2019'
EMOTICONS_REGEX = r'[\U0001f600-\U0001f64f]+'
DINGBATS_REGEX = r'[\U00002702-\U000027b0]+'
TRANSPORT_AND_MAP_REGEX = r'[\U0001f680-\U0001f6c0]+'
ENCLOSED_CHARS_REGEX = r'[\U000024c2-\U0001f251]+'
MISC_REGEX = r'[\U000000a9-\U0001f999]'


def tokenize(data):
    return nltk.tokenize.word_tokenize(data)


def make_lowercase(data):
    return [word.lower() for word in data]


def remove_punctuation(data):
    table = str.maketrans('', '', string.punctuation)
    data = [word.translate(table) for word in data]
    ### Remove apostraphes not caught by string.punctuation
    return [word for word in data if word != APOSTROPHE]


def remove_emojis(data):
    result = []
    for word in data:
        match = []
        match += re.findall(EMOTICONS_REGEX, word)
        match += re.findall(ENCLOSED_CHARS_REGEX, word)
        match += re.findall(DINGBATS_REGEX, word)
        match += re.findall(TRANSPORT_AND_MAP_REGEX, word)
        match += re.findall(MISC_REGEX, word)
        if not match == []:
            for item in match:
                word = word.replace(item, '')
        result.append(word)
    return result


def remove_empty_strings(data):
    return [word for word in data if word != '']


def remove_stop_words(data):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    stop_words.add('nt')
    stop_words.add('na')
    return [word for word in data if word not in stop_words]


def remove_numbers(data):
    return [word for word in data if not word.isdigit()]


def clean_text(data, attribute):
    text = [tokenize(data[i][attribute]) for i in range(len(data))]
    text = [make_lowercase(entry) for entry in text]
    text = [remove_punctuation(entry) for entry in text]
    text = [remove_emojis(entry) for entry in text]
    text = [remove_empty_strings(entry) for entry in text]
    text = [remove_stop_words(entry) for entry in text]
    text = [remove_numbers(entry) for entry in text]
    return text


def main():
    data = fileIO.load_json_file('../TestData/TestProfiles.json')
    clean_bios = clean_text(data, 'bio')
    print(clean_bios)


# main()
