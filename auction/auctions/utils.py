import re


def extract_int(str):
    return int(re.search("\d+", str)[0])


def extract_float(str):
    return float(re.search("\d+", str)[0])


def filter_str(str, regex = "\w.+\w"):
    return re.search(regex, str)[0]

def is_auction_equal(left, right):
    return left["name"] == right["name"] \
            and left["location"] == right["location"] \
            and left["image_url"] == right["image_url"] \
            and left["current_bid"] == right["current_bid"] \
            and left["unit_size"] == right["unit_size"] \
            and left["unit_content"] == right["unit_content"]