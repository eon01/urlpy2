#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) nexB, Inc.
# Copyright (c) 2012-2013 SEOmoz, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import urlpy as url

try:
    # Python 2
    unicode = unicode  # NOQA
    text = unicode
except NameError:  # pragma: nocover
    # Python 3
    unicode = str  # NOQA
    text = str


# Python versions
_sys_v0 = sys.version_info[0]
py2 = _sys_v0 == 2
py3 = _sys_v0 == 3


def assert_equal(a, b):
    assert a == b


def assert_not_equal(a, b):
    assert a != b


def assert_raises(e, f):
    try:
        f()
        raise Exception('Exception not raised')
    except e:
        pass


def test_deparam_sane():
    def test(bad, good):
        assert_equal(url.parse(bad).deparam(['c']).unicode, good)

    examples = [
        ('?a=1&b=2&c=3&d=4', '?a=1&b=2&d=4'),  # Maintains order
        ('?a=1&&&&&&b=2'   , '?a=1&b=2'),  # Removes excess &'s
        (';a=1;b=2;c=3;d=4', ';a=1;b=2;d=4'),  # Maintains order
        (';a=1;;;;;;b=2'   , ';a=1;b=2'),  # Removes excess ;'s
        (';foo_c=2'        , ';foo_c=2'),  # Not overzealous
        ('?foo_c=2'        , '?foo_c=2'),  # ...
        ('????foo=2'       , '?foo=2'),  # Removes leading ?'s
        (';foo'            , ';foo'),
        ('?foo'            , '?foo'),
        (''                , '')
    ]
    base = 'http://testing.com/page'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_deparam_case_insensitivity():
    def test(bad, good):
        assert_equal(url.parse(bad).deparam(['HeLlO']).unicode, good)

    examples = [
        ('?hELLo=2', ''),
        ('?HELLo=2', '')
    ]
    base = 'http://testing.com/page'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)

def test_r_deparam_sane():
    def test(bad, good):
        assert_equal(url.parse(bad).r_deparam(['c']).unicode, good)

    examples = [
        ('?a=1&b=2&c1=3&d=4', '?a=1&b=2&d=4'),  # Maintains order
        ('?a=1&&&&&&b=2'   , '?a=1&b=2'),  # Removes excess &'s
        (';a=1;b=2;c1=3;d=4', ';a=1;b=2;d=4'),  # Maintains order
        (';a=1;;;;;;b=2'   , ';a=1;b=2'),  # Removes excess ;'s
        (';foo_c1=2'        , ';foo_c1=2'),  # Not overzealous
        ('?foo_c1=2'        , '?foo_c1=2'),  # ...
        ('????foo=2'       , '?foo=2'),  # Removes leading ?'s
        (';foo'            , ';foo'),
        ('?foo'            , '?foo'),
        (''                , '')
    ]
    base = 'http://testing.com/page'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)

def test_r_deparam_case_insensitivity():
    def test(bad, good):
        assert_equal(url.parse(bad).r_deparam(['HeLlO.*']).unicode, good)

    examples = [
        ('?hELLo_there=2', ''),
        ('?HELLo_there=2', '')
    ]
    base = 'http://testing.com/page'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)

def test_filter_params():
    def function(name, value):
        '''Only keep even-valued parameters.'''
        return int(value) % 2

    def test(bad, good):
        assert_equal(url.parse(bad).filter_params(function).unicode, good)

    examples = [
        ('?a=1&b=2', '?b=2'),
        (';a=1;b=2', ';b=2')
    ]
    base = 'http://testing.com/page'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_lower():
    def test(bad, good):
        assert_equal(url.parse(bad).unicode, good)

    examples = [
        ('www.TESTING.coM'    , 'www.testing.com/'),
        ('WWW.testing.com'    , 'www.testing.com/'),
        ('WWW.testing.com/FOO', 'www.testing.com/FOO')
    ]
    for bad, good in examples:
        bad = 'http://' + bad
        good = 'http://' + good
        test(bad, good)


def test_abspath():
    def test(bad, good):
        assert_equal(url.parse(bad).abspath().unicode, good)

    examples = [
        ('howdy'           , 'howdy'),
        ('hello//how//are' , 'hello/how/are'),
        ('hello/../how/are', 'how/are'),
        ('hello//..//how/' , 'how/'),
        ('a/b/../../c'     , 'c'),
        ('../../../c'      , 'c'),
        ('./hello'         , 'hello'),
        ('./././hello'     , 'hello'),
        ('a/b/c/'          , 'a/b/c/'),
        ('a/b/c/..'        , 'a/b/'),
        ('a/b/.'           , 'a/b/'),
        ('a/b/./././'      , 'a/b/'),
        ('a/b/../'         , 'a/'),
        ('.'               , ''),
        ('../../..'        , ''),
        ('////foo'         , 'foo'),
        ('/foo/../whiz.'   , 'whiz.'),
        ('/foo/whiz./'     , 'foo/whiz./'),
        ('/foo/whiz./bar'  , 'foo/whiz./bar')
    ]

    base = 'http://testing.com/'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_escape():
    def test(bad, good):
        assert_equal(url.parse(bad).escape().unicode, good)
        # Escaping should also be idempotent
        assert_equal(url.parse(bad).escape().escape().unicode, good)

    examples = [
        ('hello%20and%20how%20are%20you', 'hello%20and%20how%20are%20you'),
        ('danny\'s pub'                 , 'danny\'s%20pub'),
        ('danny%27s pub'                , 'danny\'s%20pub'),
        ('danny\'s pub?foo=bar&yo'      , 'danny\'s%20pub?foo=bar&yo'),
        ('hello%2c world'               , 'hello,%20world'),
        ('%3f%23%5b%5d'                 , '%3F%23%5B%5D'),
        # Thanks to @myronmarston for these test cases
        ('foo?bar none=foo bar'         , 'foo?bar%20none=foo%20bar'),
        ('foo;a=1;b=2?a=1&b=2'          , 'foo;a=1;b=2?a=1&b=2'),
        ('foo?bar=["hello","howdy"]'    ,
            'foo?bar=%5B%22hello%22,%22howdy%22%5D'),
        # Example from the wild
        ('http://www.balset.com/DE3FJ4Yg/p:h=300&m=2011~07~25~2444705.png&ma=cb&or=1&w=400/2011/10/10/2923710.jpg',
            'http://www.balset.com/DE3FJ4Yg/p:h=300&m=2011~07~25~2444705.png&ma=cb&or=1&w=400/2011/10/10/2923710.jpg'),
        # Example with userinfo
        ('http://user%3Apass@foo.com/', 'http://user:pass@foo.com/')
    ]

    base = 'http://testing.com/'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_userinfo():
    def test(bad, good):
        assert_equal(url.parse(bad).unicode, good)

    examples = [
        ('http://user:pass@foo.com', 'http://user:pass@foo.com'),
        ('http://just-a-name@foo.com', 'http://just-a-name@foo.com')
    ]
    suffix = '/page.html'
    for bad, good in examples:
        bad = bad + suffix
        good = good + suffix
        test(bad, good)


def test_not_equal():
    def test(first, second):
        # None of these examples should evaluate as strictly equal
        assert_not_equal(url.parse(first), url.parse(second))
        # Using a string
        assert_not_equal(url.parse(first), second,)
        # Symmetric
        assert_not_equal(url.parse(second), url.parse(first),)
        # Using a string, symmetric
        assert_not_equal(url.parse(second), first,)
        # Should equal self
        assert_equal(url.parse(first), first,)
        assert_equal(url.parse(second), second,)

    # These examples should not work. This includes all the examples from equivalence
    # test as well.
    examples = [
        ('http://foo.com:80'         , 'http://foo.com/'),
        ('https://foo.com:443'       , 'https://foo.com/'),
        ('http://foo.com/?b=2&&&&a=1', 'http://foo.com/?a=1&b=2'),
        ('http://foo.com/%A2%B3'     , 'http://foo.com/%a2%b3'),
        ('http://foo.com/a/../b/.'   , 'http://foo.com/b/'),
        (u'http://www.kündigen.de/'  , 'http://www.xn--kndigen-n2a.de/'),
        (u'http://www.kündiGen.DE/'  , 'http://www.xn--kndigen-n2a.de/'),
        ('http://foo.com:'           , 'http://foo.co.uk/'),
        ('http://foo.com:8080'       , 'http://foo.com/'),
        ('https://foo.com:4430'      , 'https://foo.com/'),
        ('http://foo.com?page&foo'   , 'http://foo.com/?page'),
        ('http://foo.com/?b=2&c&a=1' , 'http://foo.com/?a=1&b=2'),
        ('http://foo.com/%A2%B3%C3'  , 'http://foo.com/%a2%b3'),
        (u'http://www.kündïgen.de/'  , 'http://www.xn--kndigen-n2a.de/'),
        ('http://user:pass@foo.com/' , 'http://foo.com/'),
        ('http://just-user@foo.com/' , 'http://foo.com/'),
        ('http://user:pass@foo.com/' , 'http://pass:user@foo.com/')
    ]
    for first, second in examples:
        test(first, second)


def test_equiv():
    def test(first, second):
        # Equiv with another URL object
        assert url.parse(first).equiv(url.parse(second))
        # Equiv with a string
        assert url.parse(first).equiv(second)
        # Make sure it's also symmetric
        assert url.parse(second).equiv(url.parse(first))
        # Symmetric with string arg
        assert url.parse(second).equiv(first)
        # Should be equivalent to self
        assert url.parse(first).equiv(first)
        assert url.parse(second).equiv(second)

    # Things to consider here are:
    #
    #   - default ports (https://foo.com/ == https://foo.com:443/)
    #   - capitalization of the hostname
    #   - capitalization of the escaped characters in the path
    examples = [
        ('http://foo.com:80'         , 'http://foo.com/'),
        ('https://foo.com:443'       , 'https://foo.com/'),
        ('http://foo.com/?b=2&&&&a=1', 'http://foo.com/?a=1&b=2'),
        ('http://foo.com/a/../b/.'   , 'http://foo.com/b/'),
        ('http://user:pass@foo.com/' , 'http://foo.com/'),
        ('http://just-user@foo.com/' , 'http://foo.com/')
    ]
    if py3:
        examples += [
        ('http://foo.com/%A2%B3'     , 'http://foo.com/%a2%b3'),
        (u'http://www.kündigen.de/'  , 'http://www.xn--kndigen-n2a.de/'),
        (u'http://www.kündiGen.DE/'  , 'http://www.xn--kndigen-n2a.de/'),

    ]
    for first, second in examples:
        test(first, second)


def test_not_equiv():
    def test(first, second):
        # Equiv with another URL object
        assert not url.parse(first).equiv(url.parse(second))
        # Equiv with a string
        assert not url.parse(first).equiv(second)
        # Make sure it's also symmetric
        assert not url.parse(second).equiv(url.parse(first))
        # Symmetric with string arg
        assert not url.parse(second).equiv(first)
        # Should be equivalent to self
        assert url.parse(first).equiv(first)
        assert url.parse(second).equiv(second)

        # None of these examples should evaluate as strictly equal
        assert_not_equal(url.parse(first), url.parse(second))
        # Using a string
        assert_not_equal(url.parse(first), second,)
        # Symmetric
        assert_not_equal(url.parse(second), url.parse(first),)
        # Using a string, symmetric
        assert_not_equal(url.parse(second), first,)
        # Should equal self
        assert_equal(url.parse(first), first,)
        assert_equal(url.parse(second), second,)

    # Now some examples that should /not/ pass
    examples = [
        ('http://foo.com:'           , 'http://foo.co.uk/'),
        ('http://foo.com:8080'       , 'http://foo.com/'),
        ('https://foo.com:4430'      , 'https://foo.com/'),
        ('http://foo.com?page&foo'   , 'http://foo.com/?page'),
        ('http://foo.com/?b=2&c&a=1' , 'http://foo.com/?a=1&b=2')
    ]
    if py3:
        examples += [
            ('http://foo.com/%A2%B3%C3'  , 'http://foo.com/%a2%b3'),
            (u'http://www.kündïgen.de/'  , 'http://www.xn--kndigen-n2a.de/')
        ]
    for first, second in examples:
        test(first, second), (first, second)


def test_str_repr():
    def test(first, second):
        assert_equal(str(url.parse(toparse)), strng)
        assert_equal(repr(url.parse(toparse)), '<urlpy.URL object "%s">' % strng)

    examples = [
        ('http://foo.com/', 'http://foo.com/'),
        ('http://FOO.com/', 'http://foo.com/')
    ]

    for toparse, strng in examples:
        test(toparse, strng)


def test_canonical():
    def test(bad, good):
        assert_equal(url.parse(bad).canonical().unicode, good)

    examples = [
        ('?b=2&a=1&c=3', '?a=1&b=2&c=3'),
        (';b=2;a=1;c=3', ';a=1;b=2;c=3')
    ]

    base = 'http://testing.com/'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_defrag():
    def test(bad, good):
        assert_equal(url.parse(bad).defrag().unicode, good)

    examples = [
        ('foo#bar', 'foo')
    ]

    base = 'http://testing.com/'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_deuserinfo():
    def test(bad, good):
        assert_equal(url.parse(bad).deuserinfo().unicode, good)

    examples = [
        ('http://user:pass@foo.com/', 'http://foo.com/'),
        ('http://just-user@foo.com/', 'http://foo.com/')
    ]
    for bad, good in examples:
        test(bad, good)


def test_punycode():
    def test(uni, puny):
        assert_equal(url.parse(uni).escape().punycode().unicode, puny)
        # Also make sure punycode is idempotent
        assert_equal(url.parse(uni).escape().punycode().punycode().unicode, puny)
        # Make sure that we can reverse the procedure correctly
        assert_equal(url.parse(uni).escape().punycode().unpunycode().unescape(), uni)
        # And we get what we'd expect going the opposite direction
        assert_equal(url.parse(puny).unescape().unpunycode().unicode, uni)

    examples = [
        (u'http://www.kündigen.de/',
            u'http://www.xn--kndigen-n2a.de/'),
        (u'http://россия.иком.museum/',
            u'http://xn--h1alffa9f.xn--h1aegh.museum/'),
        (u'http://россия.иком.museum/испытание.html',
            u'http://xn--h1alffa9f.xn--h1aegh.museum/%D0%B8%D1%81%D0%BF%D1%8B%D1%82%D0%B0%D0%BD%D0%B8%D0%B5.html')
    ]

    for uni, puny in examples:
        test(uni, puny)


def test_punycode_relative_urls():
    def test(relative):
        assert_raises(TypeError, url.parse(relative).punycode)
        assert_raises(TypeError, url.parse(relative).unpunycode)

    # Make sure that we can't punycode or unpunycode relative urls
    examples = ['foo', '../foo', '/bar/foo']
    for relative in examples:
        test(relative)


def test_relative():
    def test(rel, absolute):
        assert_equal(base.relative(rel).unicode, absolute)

    base = url.parse('http://testing.com/a/b/c')
    examples = [
        (u'../foo'            , u'http://testing.com/a/foo'),
        (u'./foo'             , u'http://testing.com/a/b/foo'),
        (u'foo'               , u'http://testing.com/a/b/foo'),
        (u'/foo'              , u'http://testing.com/foo'),
        (u'http://foo.com/bar', u'http://foo.com/bar'),
        (u'/foo'              , u'http://testing.com/foo'),
        (u'/\u200Bfoo'        , u'http://testing.com/\u200Bfoo'),
        (u'http://www\u200B.tiagopriscostudio.com',
            u'http://www\u200B.tiagopriscostudio.com/')
    ]

    for rel, absolute in examples:
        test(rel, absolute)


def test_sanitize():
    def test(bad, good):
        assert_equal(url.parse(bad).sanitize().unicode, good)

    examples = [
        ('../foo/bar none', 'foo/bar%20none')
    ]

    base = 'http://testing.com/'
    for bad, good in examples:
        bad = base + bad
        good = base + good
        test(bad, good)


def test_remove_default_port():
    def test(query, result):
        assert_equal(url.parse(query).remove_default_port().unicode, result)

    examples = [
        ('http://foo.com:80/'  , 'http://foo.com/'),
        ('https://foo.com:443/', 'https://foo.com/'),
        ('http://foo.com:8080/', 'http://foo.com:8080/')
    ]

    for query, result in examples:
        test(query, result)


def test_absolute():
    def test(query, result):
        assert_equal(url.parse(query).absolute, result)

    examples = [
        ('http://foo.com/bar', True),
        ('foo/'              , False),
        ('http://foo.com'    , True),
        ('/foo/bar/../'      , False)
    ]

    for query, result in examples:
        test(query, result)


def test_hostname():
    def test(query, result):
        assert_equal(url.parse(query).hostname, result)

    examples = [
        ('http://foo.com/bar', 'foo.com'),
        ('http://bar.foo.com/bar', 'bar.foo.com'),
        ('/foo', '')
    ]
    for query, result in examples:
        test(query, result)


def test_pld():
    def test(query, result):
        assert_equal(url.parse(query).pld, result)

    examples = [
        ('http://foo.com/bar'    , 'foo.com'),
        ('http://bar.foo.com/bar', 'foo.com'),
        ('/foo'                  , '')
    ]
    for query, result in examples:
        test(query, result)


def test_tld():
    def test(query, result):
        assert_equal(url.parse(query).tld, result)

    examples = [
        ('http://foo.com/bar'    , 'com'),
        ('http://bar.foo.com/bar', 'com'),
        ('/foo'                  , '')
    ]
    for query, result in examples:
        test(query, result)


def test_empty_hostname():
    def test(example):
        # Equal to itself
        assert_equal(url.parse(example), example)
        # String representation equal to the provided example
        assert_equal(url.parse(example).unicode, example)

    examples = [
        'http:///path',
        'http://userinfo@/path',
        'http://:80/path',
    ]
    for example in examples:
        test(example)

def test_copy():
    def test(example):
        original = url.parse(example)
        copy = original.copy()
        assert_equal(original, copy)
        assert_not_equal(id(original), id(copy))

    examples = [
        'http://testing.com/danny%27s pub',
        'http://testing.com/this%5Fand%5Fthat',
        'http://user:pass@foo.com',
        u'http://José:no way@foo.com',
        'http://oops!:don%27t@foo.com'
        u'española,nm%2cusa.html?gunk=junk+glunk&foo=bar baz',
        'http://foo.com/bar\nbaz.html\n',
        'http://foo.com/bar.jsp?param=\n/value%2F',
        'http://user%3apass@foo.com/'
    ]
    for example in examples:
        test(example)


def test_unknown_protocol():
    '''Can parse unknown protocol links.'''
    parsed = url.parse('unknown:0108202201')
    assert_equal(parsed.scheme, '')
    assert_equal(parsed.path, 'unknown:0108202201')


def test_component_assignment():
    parsed = url.parse('http://user@example.com:80/path;params?query#fragment')
    parsed.scheme = 'https'
    parsed.userinfo = 'username'
    parsed.host = 'foo.example.com'
    parsed.port = 443
    parsed.path = '/another/path'
    parsed.params = 'no-params'
    parsed.query = 'no-query'
    parsed.fragment = 'no-fragment'
    assert_equal(
        parsed.unicode,
        'https://username@foo.example.com:443/another/path;no-params?no-query#no-fragment'
    )


def test_component_assignment_unicode():
    parsed = url.parse('http://user@example.com:80/path;params?query#fragment')
    parsed.scheme = u'https'
    parsed.userinfo = u'username'
    parsed.host = u'foo.example.com'
    parsed.port = 443
    parsed.path = u'/another/path'
    parsed.params = u'no-params'
    parsed.query = u'no-query'
    parsed.fragment = u'no-fragment'
    assert_equal(
        parsed.unicode,
        'https://username@foo.example.com:443/another/path;no-params?no-query#no-fragment'
    )


def test_string_url():
    parsed = url.URL.parse('http://user@example.com:80/path;params?query#fragment')

    assert isinstance(parsed.scheme, (str, unicode,))
    assert isinstance(parsed.host, (str, unicode,))
    assert isinstance(parsed.params, (str, unicode,))
    assert isinstance(parsed.query, (str, unicode,))
    assert isinstance(parsed.fragment, (str, unicode,))
    assert isinstance(parsed.userinfo, (str, unicode,))
