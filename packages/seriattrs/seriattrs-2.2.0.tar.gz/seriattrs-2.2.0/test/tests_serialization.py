import json
import sys
from enum import Enum

from attrs import define
from datetime import datetime
from decimal import Decimal

from src.seriattrs import DbClass
from src.seriattrs import DbClassLiteral


def test_serialize_literal():
    class Color(Enum):
        RED = 'red'

    @define
    class Bar(DbClassLiteral):
        dictionary: dict
        date: datetime
        decimal: Decimal
        color: Color

    @define
    class Foo(DbClass):
        dictionary: dict
        date: datetime
        decimal: Decimal
        bar: Bar
        color: Color

    foo = Foo({}, datetime.now(), Decimal(1), Bar({}, datetime.now(), Decimal(1), Color.RED), Color.RED)
    serialized = foo.serialize()
    try:
        json.dump(serialized, sys.stdout)
    except:
        assert False
    deserialized = Foo.deserialize(serialized)
    assert deserialized == foo


def test_serialize():
    class Color(Enum):
        RED = 'red'

    @define
    class Bar(DbClass):
        dictionary: dict
        date: datetime
        decimal: Decimal
        color: Color

    @define
    class Foo(DbClass):
        dictionary: dict
        date: datetime
        decimal: Decimal
        bar: Bar
        bars: tuple[Bar, Bar]
        bars_dict: dict[Bar, Bar]
        color: Color

    foo = Foo({}, datetime.now(), Decimal(1), Bar({}, datetime.now(), Decimal(1), Color.RED),
              (Bar({}, datetime.now(), Decimal(1), Color.RED), Bar({}, datetime.now(), Decimal(1), Color.RED),),
              {Bar({}, datetime.now(), Decimal(1), Color.RED): Bar({}, datetime.now(), Decimal(1), Color.RED)},
              Color.RED)
    serialized = foo.serialize()
    foo.bar = foo.bar.id
    try:
        json.dump(serialized, sys.stdout)
    except:
        assert False
    deserialized = Foo.deserialize(serialized)
    assert deserialized == foo


def test_id():
    @define
    class Foo(DbClass):
        id: str

    foo = Foo("")
    serialized = foo.serialize()
    try:
        json.dump(serialized, sys.stdout)
    except:
        assert False
    deserialized = Foo.deserialize(serialized)
    assert deserialized == foo

    @define
    class Foo(DbClassLiteral):
        id: str

    foo = Foo("")
    serialized = foo.serialize()
    try:
        json.dump(serialized, sys.stdout)
    except:
        assert False
    deserialized = Foo.deserialize(serialized)
    assert deserialized == foo
