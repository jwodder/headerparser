import pytest
from   headerparser import HeaderParser, HeaderMissingError

def test_simple():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBar: green\nBaz: blue\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == ''

def test_out_of_order():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBaz: blue\nBar: green\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == ''

def test_different_cases():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBAR: green\nbaz: blue\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == ''

def test_empty_body():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBar: green\nBaz: blue\n\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == ''

def test_blank_body():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBar: green\nBaz: blue\n\n\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == '\n'

def test_body():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBar: green\nBaz: blue\n\nThis is a test.')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == 'This is a test.'

def test_headerlike_body():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('''\
Foo: red
Bar: green
Baz: blue

Foo: quux
Bar: glarch
Baz: cleesh
''')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 'blue'}
    assert msg.body == 'Foo: quux\nBar: glarch\nBaz: cleesh\n'

def test_missing():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz')
    msg = parser.parse_string('Foo: red\nBar: green\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green'}
    assert msg.body == ''

def test_missing_required():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz', required=True)
    with pytest.raises(HeaderMissingError):
        parser.parse_string('Foo: red\nBar: green\n')

def test_missing_required_default():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz', required=True, default='still required')
    with pytest.raises(HeaderMissingError):
        parser.parse_string('Foo: red\nBar: green\n')

def test_missing_default():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz', default=42)
    msg = parser.parse_string('Foo: red\nBar: green\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': 42}
    assert msg.body == ''

def test_missing_None_default():
    parser = HeaderParser()
    parser.add_header('Foo')
    parser.add_header('Bar')
    parser.add_header('Baz', default=None)
    msg = parser.parse_string('Foo: red\nBar: green\n')
    assert dict(msg) == {'Foo': 'red', 'Bar': 'green', 'Baz': None}
    assert msg.body == ''
