from lib.namers import to_mixed_case


def test_to_mixed_case():
    assert to_mixed_case("foo_bar_baz") == "fooBarBaz"
    assert to_mixed_case("fooCAPS") == "fooCAPS"
    assert to_mixed_case("FooBar") == "fooBar"
    assert to_mixed_case("HTML") == "HTML"
    assert to_mixed_case("M") == 'M'
