import string

PATH_TO_RESOURCES = "/Users/rotemwald/PycharmProjects/FinalProject/resources/"


def add_word_and_context_to_dict(dictionary, context, word):
    if context not in dictionary:
        dictionary[context] = []
    dictionary[context].append(word)


def check_if_expression_is_in_hebrew(expression):
    return type(expression).__name__ == 'str' and "\u0590" <= expression[0] <= "\u05EA"


def create_string_from_list(lst):
    result = ""
    for i in range(0, len(lst)):
        result += lst[i]
        if i < len(lst) - 1:
            result += ", "
    return result


def init_dict_in_set(dict_in_set, dict_in_file):
    for word in dict_in_file:
        dict_in_set.add(word)


def get_all_values_by_key(list_of_dict, key):
    result = []
    for dictionary in list_of_dict:
        for k, v in dictionary.items():
            if key in k:
                result.extend(v)
    return result


def remove_punctuation_from_str(s):
    exclude = set(string.punctuation)
    return ''.join(c for c in s if c not in exclude)
