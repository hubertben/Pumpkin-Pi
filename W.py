
import copy
import math

VARIABLES = {}

_BASE_DUNDER_METHODS = [
    '__new__', '__init__', '__del__', '__repr__', '__str__',    
    '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__',
    '__add__', '__sub__', '__mul__', '__matmul__', '__truediv__',
    '__floordiv__', '__mod__', '__divmod__', '__pow__',
    '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',
    '__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__',
    '__rfloordiv__', '__rmod__', '__rdivmod__', '__rpow__',
    '__rlshift__', '__rrshift__', '__rand__', '__rxor__', '__ror__',
    '__iadd__', '__isub__', '__imul__', '__imatmul__', '__itruediv__',
    '__ifloordiv__', '__imod__', '__ipow__',
    '__ilshift__', '__irshift__', '__iand__', '__ixor__', '__ior__',
    '__neg__', '__pos__', '__abs__', '__invert__',
    '__complex__', '__int__', '__float__', '__index__',
    '__round__', '__trunc__', '__floor__', '__ceil__',
    '__len__', '__getitem__', '__setitem__', '__delitem__',
    '__iter__', '__reversed__', '__contains__',
    '__enter__', '__exit__',
    '__call__', '__reduce__', '__reduce_ex__', '__sizeof__', '__dir__',
    '__hash__', '__format__'
]

_DELEGATED_METHODS = {
    int: _BASE_DUNDER_METHODS + ['bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes'],
    float: _BASE_DUNDER_METHODS + ['as_integer_ratio', 'conjugate', 'fromhex', 'hex', 'imag', 'is_integer', 'real'],
    str: _BASE_DUNDER_METHODS + [
        '__getitem__', '__len__', '__contains__',
        'capitalize', 'casefold', 'center', 'count', 'encode',
        'endswith', 'expandtabs', 'find', 'format', 'format_map',
        'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit',
        'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace',
        'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
        'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition',
        'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip',
        'swapcase', 'title', 'translate', 'upper', 'zfill'
    ],
    list: _BASE_DUNDER_METHODS + [
        '__getitem__', '__setitem__', '__delitem__', '__len__',
        '__contains__', '__iter__', '__reversed__', 'append', 'clear',
        'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'
    ],
    tuple: _BASE_DUNDER_METHODS + ['__getitem__', '__len__', '__contains__', '__iter__', '__add__', 'count', 'index'],
    range: _BASE_DUNDER_METHODS + ['__getitem__', '__len__', '__contains__', '__iter__', '__reversed__', 'count', 'index', 'start', 'stop', 'step'],
    set: _BASE_DUNDER_METHODS + ['add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection',
            'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference',
            'symmetric_difference_update', 'union', 'update'],
    dict: _BASE_DUNDER_METHODS + [
        '__getitem__', '__setitem__', '__delitem__', '__len__', '__contains__', '__iter__',
        'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'
    ],
    bool: _BASE_DUNDER_METHODS + [],
}

_DEEP_COPY_METHODS = {
    list: ['append', 'extend', 'insert', '__setitem__'],
    dict: ['__setitem__', 'update'],
    set: ['add', 'update']
}

class W:

    def __init__(self, **kwargs):
        if(len(kwargs) != 1):
            return
        
        self.key, self.value = list(kwargs.items())[0]
        self.process(self.value)
        
    def process(self, value, sameType = False):
        self.value = value
        self.type_ = type(value)
        
        if(not sameType):
            type_methods = _DELEGATED_METHODS.get(self.type_, [])

            for method_name in type_methods:
                if hasattr(self.type_, method_name):
                    def _make_delegator(name):

                        def delegate_method(*args, **kwargs):
                            args = tuple(self._unwrap_value(arg) for arg in args)
                            kwargs = {self._unwrap_value(k): self._unwrap_value(v) for k, v in kwargs.items()}

                            method = getattr(self.value, name)

                            if name in _DEEP_COPY_METHODS.get(self.type_, []):
                                args = tuple(copy.deepcopy(arg) for arg in args)
                                kwargs = {k: copy.deepcopy(v) for k, v in kwargs.items()}

                            return method(*args, **kwargs)

                        return delegate_method
                    
                    setattr(self, method_name, _make_delegator(method_name))

        VARIABLES[self.key] = value

    def _unwrap_value(self, other):
        return other.value if isinstance(other, W) else other

    def equal(self, value):
        value = self._unwrap_value(value)
        validate_type = type(value) == self.type_
        self.process(value, validate_type)
        
    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    def __del__(self):
        del self.value

    def __lt__(self, other):
        return W(kwargs = {self.key: self.value < self._unwrap_value(other)})

    def __le__(self, other):
        return W(kwargs = {self.key: self.value <= self._unwrap_value(other)})

    def __eq__(self, other):
        return W(kwargs = {self.key: self.value == self._unwrap_value(other)})

    def __ne__(self, other):
        return W(kwargs = {self.key: self.value != self._unwrap_value(other)})

    def __gt__(self, other):
        return W(kwargs = {self.key: self.value > self._unwrap_value(other)})

    def __ge__(self, other):
        return W(kwargs = {self.key: self.value >= self._unwrap_value(other)})

    def __add__(self, other):
        return W(kwargs = {self.key: self.value + self._unwrap_value(other)})

    def __sub__(self, other):
        return W(kwargs = {self.key: self.value - self._unwrap_value(other)})

    def __mul__(self, other):
        return W(kwargs = {self.key: self.value * self._unwrap_value(other)})

    def __matmul__(self, other):
        return W(kwargs = {self.key: self.value @ self._unwrap_value(other)})

    def __truediv__(self, other):
        return W(kwargs = {self.key: self.value / self._unwrap_value(other)})

    def __floordiv__(self, other):
        return W(kwargs = {self.key: self.value // self._unwrap_value(other)})

    def __mod__(self, other):
        return W(kwargs = {self.key: self.value % self._unwrap_value(other)})

    def __divmod__(self, other):
        return W(kwargs = {self.key: divmod(self.value, self._unwrap_value(other))})

    def __pow__(self, other):
        return W(kwargs = {self.key: pow(self.value, self._unwrap_value(other))})

    def __lshift__(self, other):
        return W(kwargs = {self.key: self.value << self._unwrap_value(other)})

    def __rshift__(self, other):
        return W(kwargs = {self.key: self.value >> self._unwrap_value(other)})

    def __and__(self, other):
        return W(kwargs = {self.key: self.value & self._unwrap_value(other)})

    def __xor__(self, other):
        return W(kwargs = {self.key: self.value ^ self._unwrap_value(other)})

    def __or__(self, other):
        return W(kwargs = {self.key: self.value | self._unwrap_value(other)})

    def __radd__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) + self.value})

    def __rsub__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) - self.value})

    def __rmul__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) * self.value})

    def __rmatmul__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) @ self.value})

    def __rtruediv__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) / self.value})

    def __rfloordiv__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) // self.value})

    def __rmod__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) % self.value})

    def __rdivmod__(self, other):
        return W(kwargs = {self.key: divmod(self._unwrap_value(other), self.value)})

    def __rpow__(self, other):
        return W(kwargs = {self.key: pow(self._unwrap_value(other), self.value)})

    def __rlshift__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) << self.value})

    def __rrshift__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) >> self.value})

    def __rand__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) & self.value})

    def __rxor__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) ^ self.value})

    def __ror__(self, other):
        return W(kwargs = {self.key: self._unwrap_value(other) | self.value})

    def __iadd__(self, other):
        self.value += self._unwrap_value(other)
        return self

    def __isub__(self, other):
        self.value -= self._unwrap_value(other)
        return self

    def __imul__(self, other):
        self.value *= self._unwrap_value(other)
        return self

    def __imatmul__(self, other):
        self.value @= self._unwrap_value(other)
        return self

    def __itruediv__(self, other):
        self.value /= self._unwrap_value(other)
        return self

    def __ifloordiv__(self, other):
        self.value //= self._unwrap_value(other)
        return self

    def __imod__(self, other):
        self.value %= self._unwrap_value(other)
        return self

    def __ipow__(self, other):
        self.value **= self._unwrap_value(other)
        return self

    def __ilshift__(self, other):
        self.value <<= self._unwrap_value(other)
        return self

    def __irshift__(self, other):
        self.value >>= self._unwrap_value(other)
        return self

    def __iand__(self, other):
        self.value &= self._unwrap_value(other)
        return self

    def __ixor__(self, other):
        self.value ^= self._unwrap_value(other)
        return self

    def __ior__(self, other):
        self.value |= self._unwrap_value(other)
        return self

    def __neg__(self):
        return W(kwargs = {self.key: -self.value})

    def __pos__(self):
        return W(kwargs = {self.key: +self.value})

    def __abs__(self):
        return W(kwargs = {self.key: abs(self.value)})

    def __invert__(self):
        return W(kwargs = {self.key: ~self.value})

    def __complex__(self):
        return W(kwargs = {self.key: complex(self.value)})

    def __int__(self):
        return W(kwargs = {self.key: int(self.value)})

    def __float__(self):
        return W(kwargs = {self.key: float(self.value)})

    def __index__(self):
        return W(kwargs = {self.key: self.value.__index__()})

    def __round__(self, n=None):
        return W(kwargs = {self.key: round(self.value, n)})

    def __trunc__(self):
        return W(kwargs = {self.key: math.trunc(self.value)})

    def __floor__(self):
        return W(kwargs = {self.key: math.floor(self.value)})

    def __ceil__(self):
        return W(kwargs = {self.key: math.ceil(self.value)})
    
    def __len__(self):
        return W(kwargs = {self.key: len(self.value)})

    def __getitem__(self, key):
        return W(kwargs = {self.key: self.value[key]})

    def __setitem__(self, key, value):
        self.value[key] = W(kwargs = {self.key: value})

    def __delitem__(self, key):
        del self.value[key]

    def __iter__(self):
        return iter(W(kwargs = {self.key: [W(val) for val in self.value]}))

    def __reversed__(self):
        return reversed(W(kwargs = {self.key: [W(val) for val in self.value]}))

    def __contains__(self, item):
        return W(kwargs = {self.key: item in self.value})

    def __call__(self, *args, **kwargs):
        return W(kwargs = {self.key: self.value(*args, **kwargs)})

    def __sizeof__(self):
        return W(kwargs = {self.key: self.value.__sizeof__()})

    def __dir__(self):
        return W(kwargs = {self.key: dir(self.value)})

    def __hash__(self):
        return W(kwargs = {self.key: hash(self.value)})

    def __format__(self, format_spec):
        return W(kwargs = {self.key: format(self.value, format_spec)})
    




    def append(self, value):
        return self.value.append(self._unwrap_value(value))

    def extend(self, iterable):
        return self.value.extend(map(self._unwrap_value, iterable))

    def insert(self, index, value):
        return self.value.insert(index, self._unwrap_value(value))

    def remove(self, value):
        return self.value.remove(self._unwrap_value(value))

    def pop(self, index=-1):
        return self.value.pop(index)

    def index(self, value, start=0, end=None):
        return self.value.index(self._unwrap_value(value), start, end if end is None else self._unwrap_value(end))

    def count(self, value):
        return self.value.count(self._unwrap_value(value))

    def sort(self, key=None, reverse=False):
        if key:
            self.value.sort(key=lambda x: key(self._unwrap_value(x)), reverse=reverse)
        else:
            self.value.sort(reverse=reverse)

    def reverse(self):
        return W(kwargs = {self.key: self.value.reverse()})

    def copy(self):
        return W(kwargs = {self.key: self.value.copy()})

    def clear(self):
        return W(kwargs = {self.key: self.value.clear()})





    def get(self, key, default=None):
        return self.value.get(self._unwrap_value(key), self._unwrap_value(default))

    def items(self):
        return self.value.items()

    def keys(self):
        return self.value.keys()

    def values(self):
        return self.value.values()

    def pop(self, key, default=None):
        return self.value.pop(self._unwrap_value(key), self._unwrap_value(default))

    def popitem(self):
        return self.value.popitem()

    def setdefault(self, key, default=None):
        return self.value.setdefault(self._unwrap_value(key), self._unwrap_value(default))

    def update(self, other):
        return self.value.update({k: self._unwrap_value(v) for k, v in other.items()})

    def clear(self):
        return self.value.clear()





    def add(self, value):
        return W(kwargs = {self.key: self.value.add(self._unwrap_value(value))})

    def remove(self, value):
        return W(kwargs = {self.key: self.value.remove(self._unwrap_value(value))})

    def discard(self, value):
        return W(kwargs = {self.key: self.value.discard(self._unwrap_value(value))})

    def pop(self):
        return W(kwargs = {self.key: self.value.pop()})

    def union(self, *others):
        return W(kwargs = {self.key: self.value.union(*map(self._unwrap_value, others))})

    def intersection(self, *others):
        return W(kwargs = {self.key: self.value.intersection(*map(self._unwrap_value, others))})



# G = W(G = 'Hello, World!')
# H = W(H = 9.7)
# I = W(I = {"a": 1, "b": 2, "c": 3})
# J = W(J = [4, 5, 6, 7, "W"])
# K = W(K = (True, False))


# for key, value in VARIABLES.items():
#     print(key, value)


# H *= -81.4
# I["a"] = I["b"] + I["c"]

# G.equal( G[:len(G) // 2:-1] )
# J.equal( [str(hash(str(item)))[-3:] for item in J[::-1]] )
# K.equal( (K[0] or K[1]) )

# print("\n----------------------------\n")

# for key, value in VARIABLES.items():
#     print(key, value)


Z = W(Z = 0)
Y = W(Y = 1)
X = W(X = 1)

L = W(L = [])

for index in range(10):
    
    Z.equal(X + Y)
    X.equal(Y)
    Y.equal(Z)
    L.append(X)
    
    print(VARIABLES)


    