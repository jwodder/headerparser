from   six       import itervalues, string_types
from   .         import errors
from   .normdict import NormalizedDict
from   .scanner  import scan_file, scan_lines, scan_string
from   .types    import lower
from   .util     import unfold

class HeaderParser(object):
    def __init__(self, normalizer=None, body=True):
        self.normalizer = normalizer or lower
        self.body = body
        self.headerdefs = dict()
        self.dests = set()

    def add_header(self, name, *altnames, **kwargs):
        kwargs.setdefault('dest', name)
        hd = HeaderDef(name=name, **kwargs)
        normed = set(map(self.normalizer, (name,) + altnames))
        # Error before modifying anything:
        redefs = [n for n in self.headerdefs if n in normed]
        if redefs:
            raise ValueError('header defined more than once: '+repr(redefs[0]))
        if self.normalizer(hd.dest) in self.dests:
            raise ValueError('destination defined more than once: '
                             + repr(hd.dest))
        for n in normed:
            self.headerdefs[n] = hd
        self.dests.add(self.normalizer(hd.dest))

    def parse_stream(self, headers):
        data = NormalizedDict(normalizer=self.normalizer)
        for k,v in headers:
            if k is None:
                assert data.body is None
                data.body = v
            else:
                try:
                    hd = self.headerdefs[self.normalizer(k)]
                except KeyError:
                    raise errors.UnknownHeaderError(k)
                hd.process_value(data, v)
        for hd in itervalues(self.headerdefs):
            if hd.dest not in data:
                if hd.required:
                    raise errors.MissingHeaderError(hd.name)
                elif hasattr(hd, 'default'):
                    data[hd.dest] = hd.default
        return data

    def parse_file(self, fp):
        return self.parse_stream(scan_file(fp))

    def parse_lines(self, iterable):
        return self.parse_stream(scan_lines(iterable))

    def parse_string(self, s):
        return self.parse_stream(scan_string(s))


class HeaderDef(object):
    def __init__(self, name, dest, type=None, multiple=False, required=False,
                 unfold=False, choices=None, **kwargs):
        if not isinstance(name, string_types):
            raise TypeError('header names must be strings')
        self.name = name
        self.dest = dest
        self.type = type
        self.multiple = bool(multiple)
        self.required = bool(required)
        self.unfold = bool(unfold)
        if choices is not None:
            choices = list(choices)
            if not choices:
                raise ValueError('empty list supplied for choices')
        self.choices = choices
        if 'default' in kwargs:
            if self.required:
                raise ValueError('required and default are mutually exclusive')
            self.default = kwargs.pop('default')
        if kwargs:
            raise TypeError('invalid keyword argument: '
                            + repr(next(iter(kwargs))))

    def process_value(self, data, value):
        if self.unfold:
            value = unfold(value)
        if self.type is not None:
            try:
                value = self.type(value)
            except errors.HeaderTypeError:
                raise
            except Exception as e:
                raise errors.HeaderTypeError(self.name, value, e)
        if self.choices is not None and value not in self.choices:
            raise errors.InvalidChoiceError(self.name, value)
        if self.multiple:
            data.setdefault(self.dest, []).append(value)
        elif self.dest in data:
            raise errors.DuplicateHeaderError(self.name)
        else:
            data[self.dest] = value
