import re
import string
from typing import List

from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # type: ignore

factory = StemmerFactory()
stemmer = factory.create_stemmer()


class CleaningParams(object):
    """
    Parameters for text cleaning.

    Attributes:
        to_lower (bool): Convert text to lowercase.
        remove_punctuation (bool): Remove punctuation from text.
        remove_stopwords (bool): Remove stopwords from text.
        remove_numbers (bool): Remove numbers from text.
        remove_urls (bool): Remove URLs from text.
        remove_mentions (bool): Remove mentions from text.
        remove_hashtags (bool): Remove hashtags from text.
        remove_retweet (bool): Remove retweet tags from text.
        remove_extra_whitespace (bool): Remove extra whitespace from text.
        use_stemming (bool): Apply stemming to text.
    """

    to_lower: bool = True
    remove_punctuation: bool = True
    remove_stopwords: bool = True
    remove_numbers: bool = True
    remove_urls: bool = True
    remove_mentions: bool = True
    remove_hashtags: bool = True
    remove_retweet: bool = True
    remove_extra_whitespace: bool = True
    use_stemming: bool = True


def clean_sentence_indonesia(text: str, clean_params: CleaningParams) -> str:
    """Clean a text sentence using the specified parameters.

    Args:
        text (str): The input text sentence.
        clean_params (CleaningParams): The cleaning parameters.

    Returns:
        str: The cleaned text sentence.

    Examples:
        >>> text = "RT @canggih: Mereka lihat ini: https://example.com"
        >>> params = CleaningParams()
        >>> clean_texts(list_of_texts, params)
        mereka lihat ini
    """

    # Remove RT
    if clean_params.remove_retweet:
        if text.startswith("RT "):
            text = text[3:].strip()

    # Remove URLs
    if clean_params.remove_urls:
        text = re.sub(r"http\S+", "", text)

    # Remove mentions
    if clean_params.remove_mentions:
        text = re.sub("@[A-Za-z0-9]+", "", text)

    # Remove hashtags
    if clean_params.remove_hashtags:
        text = re.sub("#", "", text)

    # Remove numbers
    if clean_params.remove_numbers:
        text = re.sub(r"\d+", "", text)

    # Convert to lowercase
    if clean_params.to_lower:
        text = text.lower()

    # Remove extra whitespace
    if clean_params.remove_extra_whitespace:
        text = " ".join(text.split())

    # Remove punctuation
    if clean_params.remove_punctuation:
        text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove stop words
    if clean_params.remove_stopwords:
        stop_words = set(stopwords.words("indonesian"))
        word_tokens = word_tokenize(text)
        filtered_sentence = [word for word in word_tokens if word not in stop_words]
        text = " ".join(filtered_sentence)

    # Stemming
    if clean_params.use_stemming:
        text = stemmer.stem(text)

    return text


def clean_sentences_indonesia(
    list_of_texts: List[str],
    clean_params: CleaningParams,
) -> List[str]:
    """
    Clean a list of text by removing RT, URLs, mentions, hashtags, numbers,
    converting to lowercase, removing extra whitespace, punctuation, and stop words.

    Args:
        list_of_texts (List[str]): A list of input text sentences.
        clean_params (CleaningParams): The cleaning parameters.

    Returns:
        List[str]: A list of cleaned text sentences.

    Examples:
        >>> list_of_texts = ["RT @canggih: Mereka lihat ini: https://example.com", "Halo 123!"]
        >>> params = CleaningParams()
        >>> clean_texts(list_of_texts, params)
        ['mereka lihat ini', 'halo']
    """
    return [clean_sentence_indonesia(text, clean_params) for text in list_of_texts]
