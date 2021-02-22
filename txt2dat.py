#!/usr/bin/env python3
from sys import argv, stdin
import pyperclip
import detect_delimiter
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

FIELD_MODE_TESTS = {'field_mode__size' : \
                    [['size', 'size in bytes'],'size'],
                    
                    'field_mode__crc32' : \
                    [['crc', 'crc32', 'crc-32'],'crc'],
                    
                    'field_mode__md5' : \
                    [['md5', 'md-5', 'md5sum'],'md5'],
                    
                    'field_mode__sha1' : \
                    [['sha1', 'sha-1', 'sha1sum'],'sha1'],
                    
                    'field_mode__sha256' : \
                    [['sha256', 'sha-256', 'sha256sum'],'sha256']}

argv_name_enabled = False
argv_ext_enabled = False
if len(argv) == 3:
    argv_last = argv[-1]
    if argv[-2] == '-n':
        argv_name_value = argv_last
        argv_name_enabled = True
    if argv[-2] == '-e':
        argv_ext_value = argv_last
        argv_ext_enabled = True

def dict_to_xml(mydict):
    game = Element('game')
    subelement = SubElement(game, 'rom')
    for key, value in mydict.items():
        subelement.set(key, value)
    return ElementTree.tostring(game,encoding='unicode')

def test_field_mode(field_mode_label,key):
    key = key.lower()
    for string in FIELD_MODE_TESTS[field_mode_label][0]:
        if string == key:
            return field_mode_label, FIELD_MODE_TESTS[field_mode_label][1]
    return None, None

def text_to_dict(text):
    mydict = {}
    delim = detect_delimiter.detect(text[0], whitelist=[':',' '])
    if delim == None:
        raise ValueError('Cannot detect delimiter.')
    for line in text:
        if line.strip() != '':
            line_split = line.split(sep=delim, maxsplit=1)
            key = line_split[0].strip()
            value = line_split[1].strip()

            field_mode = 'field_mode__size'
            field_test_results = test_field_mode(field_mode,key)
            if field_test_results[0] == field_mode:
                key = field_test_results[1]
                value = value.replace(' ','') \
                             .replace(',','') \
                             .replace('bytes','')

            field_mode = 'field_mode__crc32'
            field_test_results = test_field_mode(field_mode,key)
            if field_test_results[0] == field_mode:
                key = field_test_results[1]
                value = value.upper().replace(' ','')

            field_mode = 'field_mode__md5'
            field_test_results = test_field_mode(field_mode,key)
            if field_test_results[0] == field_mode:
                key = field_test_results[1]
                value = value.upper().replace(' ','')

            field_mode = 'field_mode__sha1'
            field_test_results = test_field_mode(field_mode,key)
            if field_test_results[0] == field_mode:
                key = field_test_results[1]
                value = value.upper().replace(' ','')

            field_mode = 'field_mode__sha256'
            field_test_results = test_field_mode(field_mode,key)
            if field_test_results[0] == field_mode:
                key = field_test_results[1]
                value = value.upper().replace(' ','')
            
            mydict[key] = value
    return mydict

def main(lines_list):
    CORRECT_FIELD_ORDER = ['name', 'size', 'crc', 'md5', 'sha1', 'sha256']
    mydict = text_to_dict(lines_list)
    for key in CORRECT_FIELD_ORDER:
        try:
            mydict[key] = mydict.pop(key)
        except KeyError:
            if key == 'name':
                if argv_name_enabled:
                    mydict['name'] = argv_name_value
                elif argv_ext_enabled:
                    mydict['name'] = 'dummy_name.{}'.format(argv_ext_value)
            else:
                pass
    xml = dict_to_xml(mydict)
    return(xml)
    
if __name__ == '__main__':
    if not stdin.isatty():
        lines_list = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            lines_list.append(line)
        print(main(lines_list))
    else:
        lines_list = stdin.read().splitlines()
        print(main(lines_list))

