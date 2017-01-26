import collections
from   operator import methodcaller
from   six      import iteritems, itervalues

class NormalizedDict(collections.MutableMapping):
    def __init__(self, data=None, normalizer=methodcaller('lower'), body=None):
        ### Should this do anything special when `data` is a NormalizedDict?
        self._data = {}
        self.normalizer = normalizer
        self.body = body
        if data is not None:
            # Don't call `update` until after `normalizer` is set.
            self.update(data)

    def __getitem__(self, key):
        return self._data[self.normalizer(key)][1]

    def __setitem__(self, key, value):
        self._data[self.normalizer(key)] = (key, value)

    def __delitem__(self, key):
        del self._data[self.normalizer(key)]

    def __iter__(self):
        return (key for key, value in itervalues(self._data))

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if isinstance(other, NormalizedDict):
            if self.normalizer is not other.normalizer or \
                    self.body != other.body:
                return False
        elif isinstance(other, collections.Mapping):
            if self.body is not None:
                return False
            other = NormalizedDict(other, normalizer=self.normalizer)
        else:
            return NotImplemented
        return self.normalized_dict() == other.normalized_dict()

    def __ne__(self, other):
        return not (self == other)

    def normalized(self):
        return NormalizedDict(
            self.normalized_dict(),
            normalizer=self.normalizer,
            body=self.body,
        )

    def normalized_dict(self):
        return dict((key, value) for key, (_, value) in iteritems(self._data))

    def copy(self):
        return self.__class__(self._data.copy(), self.normalizer, self.body)
