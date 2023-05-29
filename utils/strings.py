def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        # To find out the exception
        # Exception as e:
        # print(e.__class__.__name__)
        return False
    return number_string > 0


# print(is_positive_number('10'))
# print(is_positive_number('-10'))
# print(is_positive_number('-10.5'))
# print(is_positive_number('-10a'))
