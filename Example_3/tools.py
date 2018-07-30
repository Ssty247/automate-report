# -*- coding: utf-8 -*-
import re
import logging, os

def str2num(string):
    """
    str2num(string)
    
    Get number for a string.
    
    Parameters
    ----------
    string : a string with the format like '$2.1', '$1, 333' or '&4,3'
    
    Returns
    -------
    out : float
    
    Examples
    --------
    >>> str2num('$2.3')
    2.3
    """
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

def check_folder(folder_name):
    if os.path.exists(folder_name):
        logging.info("文件夹已创立：{}".format(folder_name))
    else:
        logging.warning("文件夹未创立：{}".format(folder_name))
        os.makedirs(folder_name)
        logging.info("文件夹创立完毕：{}".format(folder_name))