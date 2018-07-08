"""Util module."""
import string
import re

LOWER = 1
UPPER = 2
DIGIT = 3
OTHER = 4

def classify_char(char):
    """Classify characters"""
    if char in string.ascii_lowercase:
        return LOWER
    elif char in string.ascii_uppercase:
        return UPPER
    elif char in string.digits:
        return DIGIT
    return OTHER

def split_words(input_string):
    """Split input_string to word"""
    classified = [classify_char(char) for char in input_string]
    result = []
    start = 0
    for current, current_token in enumerate(classified):
        next_pos = current + 1
        if current_token == OTHER:
            if current > start:
                result.append(input_string[start:current])
            start = next_pos
            continue
        rest = classified[current:]
        if len(rest) > 1 and current_token != rest[1]:
            if rest[1] == UPPER or rest[1] == DIGIT:
                result.append(input_string[start:next_pos])
                start = next_pos
        elif len(rest) > 2 and current_token == UPPER and rest[2] == LOWER:
            result.append(input_string[start:next_pos])
            start = next_pos
    if start < len(input_string):
        result.append(input_string[start:])
        return result
    elif not result:
        return [""]
    return result


def get_valid_class_name(input_string: str) -> str:
    """
    Convert input string to valid class name.

    Remove spaces and other unusable character, add capitalize first letters
    of words. Remove anything that is not alphanumeric.

    :param str input_string: The string to convert.
    :returns: Returns a pep8 compatible class name.
    """
    return ''.join([word.capitalize() for word in split_words(input_string)])


def get_valid_function_name(input_string: str) -> str:
    """
    Convert input string to valid function name.

    Remove spaces and other unusable character, add under scores between
    words. Remove anything that is not alphanumeric.

    :param str input_string: The string to convert.
    :returns: Returns a pep8 compatible function name.
    """
    result = '_'.join([word for word in split_words(input_string)])
    return re.sub('_(?=[0-9])', '', result)
