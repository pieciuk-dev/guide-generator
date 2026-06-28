"""Tests for map coordinate extraction."""
from guide_generator.maps.extract import parse_coordinates, plain_text


def test_decimal_in_parens():
    text = """
## Location
**Coordinates:** 56°33′09.6″N, 16°38′23.2″E (56.552667, 16.639778)
"""
    r = parse_coordinates(text)
    assert r is not None
    lat, lng, _ = r
    assert abs(lat - 56.552667) < 1e-5
    assert abs(lng - 16.639778) < 1e-5


def test_bare_decimal():
    text = """
## Location
**Coordinates:** 56.52804, 16.51992 WGS84
"""
    r = parse_coordinates(text)
    assert r is not None
    assert r[0] == 56.52804


def test_dms_only():
    text = """
## Location & access
**Coordinates:** 57°22′01″N, 17°05′49″E
"""
    r = parse_coordinates(text)
    assert r is not None
    assert 57.3 < r[0] < 57.4


def test_representative_access():
    text = """
## Location
**Coordinates:** No single point. **Representative access:** parking 56.52804, 16.51992
"""
    r = parse_coordinates(text)
    assert r is not None
    assert r[2] == "representative"


def test_plain_text_strips_wikilinks():
    assert plain_text("See [[sandby-borg|Sandby borg]] here") == "See Sandby borg here"
