#%%
from typing import List
import re


class Parser:
    def __init__(self, string_to_parse: str, tokens: List[str], return_not_matched=True) -> None:
        """
        initializes the Parser with it's string, and the tokens
        it's of utermost importance that the tokens go from
        less general, to more general
        so, "bpm+" MUST come before "+", otherwise incorrect matches will happen
        """
        self.__string = string_to_parse.lower()
        self.__tokens = tokens
        self.__return_not_matched = return_not_matched
    
    def parse(self) -> List[str]:
        """
        splits the string with the passed tokens and
        returns a list of strings
        non matched characters are returned as single characters at the end of the list
        if the return_not_matched flag is True (default)
        """
        regex_pattern = '|'.join(f'{re.escape(delim)}' for delim in self.__tokens)
        tokens_found = re.findall(regex_pattern, self.__string)
        if self.__return_not_matched:
            rest_of_string = re.sub(regex_pattern, "", self.__string)
            return tokens_found + list(rest_of_string)
        else:
            return tokens_found
# %%
