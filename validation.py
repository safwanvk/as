from __future__ import print_function


def sid(value):
    """
    Get valid Student ID
    Must be a <=7 digit integer
    :param value: sid
    :return: valid sid
    """
    if not value: raise ValueError("sid (Student ID) not specified")

    if not isinstance(value, int):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("sid (Student ID) must be an integer")

    if len(str(value)) > 7:
        raise ValueError("sid (Student ID) must be <=7 digits long")

    return value