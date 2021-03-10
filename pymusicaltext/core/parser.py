#%%
from typing import List
import re


class Parser:
    def __init__(self, string_to_parse: str, tokens: List[str]) -> None:
        """
        initializes the Parser with it's string, and the tokens
        it's of utermost importance that the tokens go from
        less general, to more general
        so, "bpm+" MUST come before "+", otherwise incorrect matches will happen
        """
        self.__string = string_to_parse.lower()
        self.__tokens = tokens
    
    def parse(self) -> List[str]:
        """
        splits the string with the passed tokens and
        returns a list of strings
        """
        regex_pattern = '|'.join(f'{re.escape(delim)}' for delim in self.__tokens)
        tokens_found = re.findall(regex_pattern, self.__string)
        rest_of_string = re.sub(regex_pattern, "", self.__string)
        return tokens_found + list(rest_of_string)
# %%
