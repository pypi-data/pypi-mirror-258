import pytest
from dataclasses import dataclass
from typing import Union
import idspy_toolkit.simplexml as simplexml


class NotReallyDict(dict):
    pass


test_notreallydict = NotReallyDict({"a": 1, "b": NotReallyDict({"c": 2, })})
test_notreallydict_xml = r'<root><a type="int">1</a><b type="dict"><c type="int">2</c></b></root>'

dict_sample = {
    'data': {
        'id': '123',
        'values': [1, 2, 3],
        'descr': {"a": 1, "b": 2},
        'values_2d': [[1, 2, 3], [1, 2, 3]]
    },
    'offset': 2,
    'id': 123,
}

true_string = r'<root><data type="dict"><id type="str">123</id><values type="list"><item type="int">1</item><item type="int">2</item><item type="int">3</item></values><descr type="dict"><a type="int">1</a><b type="int">2</b></descr><values_2d type="list"><item type="list"><item type="int">1</item><item type="int">2</item><item type="int">3</item></item><item type="list"><item type="int">1</item><item type="int">2</item><item type="int">3</item></item></values_2d></data><offset type="int">2</offset><id type="int">123</id></root>'


def compare_dict(dict1, dict2) -> bool:
    equal = all([dict1[key] == dict2[key]
                 for key in dict1.keys()
                 if ((key in dict2) and (not isinstance(dict2[key], dict)))])
    return equal


def test_write_xml():
    xmlstr = simplexml.dict_to_xml(dict_sample)
    assert xmlstr == true_string


def test_write_derived_xml():
    xmlstr = simplexml.dict_to_xml(test_notreallydict)
    assert xmlstr == test_notreallydict_xml


def test_read_derived_xml():
    xmldict = simplexml.xml_to_dict(test_notreallydict_xml)
    equal = compare_dict(xmldict, test_notreallydict)
    assert equal is True
    equal = compare_dict(xmldict.get('b', {}), test_notreallydict['b'])
    assert equal is True


def test_read_xml():
    xmldict = simplexml.xml_to_dict(true_string)
    equal = compare_dict(xmldict, dict_sample)
    assert equal is True
    equal = compare_dict(xmldict.get('data', {}), dict_sample['data'])
    assert equal is True
    equal = compare_dict(xmldict.get('data', {}).get("descr", {}), dict_sample['data']['descr'])
    assert equal is True
