# %%
import re
from typing import List


class Parser:
    def __init__(
        self,
        string_to_parse: str,
        tokens: List[str],
        return_not_matched: bool = False,
    ) -> None:
        """
        initializes the Parser with it's string, and the tokens
        it's of uttermost importance that the tokens go from
        less general, to more general
        so, "bpm+" MUST come before "+",
        otherwise incorrect matches will happen
        """
        self.__string = string_to_parse
        self.__tokens = tokens
        self.__return_not_matched = return_not_matched

    def parse(self) -> List[str]:
        """
        splits the string with the passed tokens and
        returns a list of strings
        non matched characters are ignored
        """
        regex_pattern = "|".join(
            f"{re.escape(delim)}" for delim in self.__tokens
        )
        if self.__return_not_matched:
            regex_pattern += "|."
        tokens_found = re.findall(regex_pattern, self.__string)
        return tokens_found


# %%
