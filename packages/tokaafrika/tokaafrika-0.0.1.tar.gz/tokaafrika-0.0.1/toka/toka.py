import re
import pickle
from collections import Counter
from typing import List, Dict, Tuple, Any, Union
from toka.utils import STOPWORDS, LANGUAGE_CODES_DESCRIPTIONS, \
LANGUAGE_DESCRIPTIONS_CODES

class TokaAPI:
    
    def __init__(self):
        """
        """
        pass 
    
    def get_stopwords(self, language: str = "", default_all: bool = False)\
     -> Union[frozenset, Dict[str, List[str]]]:
        """ Prebuild stop words accross all languages in South Africa

            Attributes
            ----------
            language: this require language name or code
                    (refer to langauge code and name)
            default_all: False, True return all stopwords for all SA 
                        languages including N|uu
            
            Returns
            ----------
            stopwords : stopwords for a language or all
                
            Notes
            ----------
            This can be complemented with some of the stopwords known or can 
            be customized.

            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> stopwords = api.get_stopwords('tshivenda') # use fullname
            >>> print(stopwords)
            frozenset({'a', 'vha', 'u', 'na', 'tshi', 'nga', 'ya', 'ndi',
            ... 'o', 'khou', 'ni', 'uri', 'hu', 'ha', 'kha', 'i',
            ... 'zwi', 'tsha', 'ri', 'yo', 'wa', 'ho', 'vho', 'musi',
            ... 'ḽa', 'zwa', 'ḓo', 'amba', 'nahone', 'no'})
            >>> stopwords = api.get_stopwords('ven') # use shotname/code
            >>> print(stopwords)
            frozenset({'a', 'vha', 'u', 'na', 'tshi', 'nga', 'ya', 'ndi',
            ... 'o', 'khou', 'ni', 'uri', 'hu', 'ha', 'kha', 'i',
            ... 'zwi', 'tsha', 'ri', 'yo', 'wa', 'ho', 'vho', 'musi',
            ... 'ḽa', 'zwa', 'ḓo', 'amba', 'nahone', 'no'})
            >>> .
        """

        if language is not None:
            language = language.lower()
        else:
            raise TypeError("language must be (str), cannot be 'NoneType'")

        if default_all:
            return STOPWORDS
        try:
            if len(language) == 3:
                lang_code = language
            else:
                lang_code = LANGUAGE_DESCRIPTIONS_CODES[language]
            return frozenset(STOPWORDS[lang_code])
        except KeyError:
            raise ValueError(f"language '{language}' name or code not found!")
    

    def clean_symbols(self, text: str) -> str:
        """ Clean symbols in a text like punctuations 
            Attributes
            ----------
            text: text given to clean
            
            Returns
            ----------
            clean_text : removed symbol text
                
            Notes
            ----------
            Assumes the text is not empty 
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> clean_text = \
            ...    toka_object.clean_symbols('Hello! This is an example\
            ...     text with numbers like 123 ')
            >>> print(clean_text)
            hello this is an example text with numbers like 
            >>> .
        """
        if text is not None:
            clean_text = re.sub(r'[!@#$(),\n"%^*?\:;~`’0-9\[\]]', '', text)
            return clean_text
        else:
            raise TypeError('text must be string!')

    
    def get_frequent_words(self, text: str, clean_symbols: bool = True)\
     -> Dict[str, int]:
        """Count frequent words in a given text
        
            Attributes
            ----------
            text: text to split and count words
            
            Returns
            ----------
            dictionary object with count of each word
                
            Notes
            ----------
            This assumes text is string type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> toka_object = TokaAPI()
            >>> english = toka_object.get_frequent_words('Hello test')
            >>> print(english) 
            {'hello': 1, 'test': 1}
            >>> .
            
        """
        if text is not None:
            if clean_symbols:
                text = self.clean_symbols(text.lower()).split()
            else:
                text = text.lower().split()
            frequency = Counter(text)
            return frequency
        else:
            raise TypeError('text must be string!')
    

    def compute_stopwords(self, text: str, n_words: int) -> List[str]:
        """ This function get the top n most frequent words
            
            Attributes
            ----------
            text: text to use to process the frequency and stopwords
            n_words: number of words to limit
            
            Returns
            ----------
            self : object
                Fitted estimator.
                
            Notes
            ----------
            This assumes text is string and not empty
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> stopwords = api.compute_stopwords(
            ...    "the the are are the are on the on", 3)
            >>> print(stopwords)
            ['the', 'are', 'on']
            >>> .
            
        """
        top_words = self.get_frequent_words(text)
        top_words = top_words.most_common(n_words)
        top_words = list(list(zip(*top_words))[0])
        return top_words
    
    def load_model_from_pickle(self, model_filename: str, 
                vectorizer_filename: str) -> Tuple[Any, Any]:
        """ Loads pickle files for both vector and its model 
            Attributes
            ----------
            model_filename: path and file name for model
            vectorizer_filename: path and filename for vectorizer
            
            Returns
            ----------
            Tuple : object
                Fitted estimator.
                
            Notes
            ----------
            Model and Vector filename should be of model and vector type
            
            Examples
            ----------
            >>> from toka.toka import TokaAPI
            >>> api = TokaAPI()
            >>> model = 'model.pkl'
            >>> vector = 'vector.pkl'
            >>> clf, vector = api.load_model_from_pickle(model,
            ...                     vector)
            >>> .

        """
        # Load the trained model from the pickle file
        with open(model_filename, "rb") as model_file:
            loaded_model = pickle.load(model_file)

        # Load the vectorizer from the pickle file
        with open(vectorizer_filename, "rb") as vectorizer_file:
            loaded_vectorizer = pickle.load(vectorizer_file)

        return loaded_model, loaded_vectorizer