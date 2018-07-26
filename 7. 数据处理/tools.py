import re

def str2num(string):
    if not isinstance(string, str):
        string = str(string)
    string = string.replace(',','')
    regular_expression = '\d+\.?\d*'
    pattern = re.compile(regular_expression)
    match = pattern.search(string)
    if match:
        return float(match.group())
    else:
        return float('nan')