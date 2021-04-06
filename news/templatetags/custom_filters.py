import re
from django import template

# Example words for censor filter
BANNED_WORDS = ['warmly', 'cousin', 'her', 'delay']

register = template.Library()


@register.filter(name='censor')
def censor(text, derivatives=False):
    """
    Replace each banned word in a given text with its censored variant:
    [first_letter][...asterisks...][last_letter]
    word -> w**d

    If 'derivatives' is True, the filter triggers on derivative words:
    sword -> sw**d
    Default: False.

    Case-insensitive, min. 3-letter words (shorter ones are improbable).
    """

    def asteriskify(matchobj):
        """
        Switch all letters of a banned word expect the first and
        the last to '*'.
        """
        word = matchobj[0]
        return word[0] + '*' * (len(word)-2) + word[-1]

    censored_text = text
    for banned_word in BANNED_WORDS:
        censored_text = re.sub(
            banned_word
            if derivatives else rf'(^|(?<=\W)){banned_word}((?=\W)|$)',
            asteriskify,
            censored_text,
            flags=re.IGNORECASE
        )
    return censored_text
