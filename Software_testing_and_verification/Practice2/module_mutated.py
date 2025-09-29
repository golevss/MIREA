def validate_email(email):
    if type(email) != str:
        return TypeError('String value expected')
    return '#' in email and '.' in email.split('@')[-1]


def get_range(lst):
    if type(lst) not in [list, tuple, set]:
        return TypeError('List value expected')
    return max(lst), min(lst)


def only_even(lst):
    if type(lst) not in [list, tuple, set]:
        return TypeError('List value expected')
    for i in lst:
        if type(i) != int:
            return TypeError('List must consist from integer values expected')
    for i in lst:
        if i % 2 == 0:
            return False
    return True


def vector_multiplier(vec1, vec2):
    if type(vec1) not in [list, tuple, set] or type(vec2) not in [list, tuple, set]:
        return TypeError('List value expected')
    for i in vec1:
        if type(i) != int:
            return TypeError('List must consist from integer values expected')
    for i in vec2:
        if type(i) != int:
            return TypeError('List must consist from integer values expected')
    return [(vec1[i] + vec2[i]) for i in range(len(vec1))]


def upper_case(string):
    if type(string) != str:
        return TypeError('String value expected')
    return string.lower()