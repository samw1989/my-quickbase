from my_quickbase.helpers import parse_response, check_attr_exists, AttrNotSet
import pytest


@pytest.mark.parametrize('json_input', [{"name": "John", "age": 30, "car": 'honda'}, {}, '2'])
def test_parse_response(mock_response, json_input):
    mock_response = mock_response(json_input)
    if json_input:
        assert parse_response(mock_response) == json_input
    else:
        assert parse_response(mock_response) is None


def test_cls_method_decorator():

    @check_attr_exists('mock_attr')
    class TestClass:

        def __init__(self):
            self.mock_attr = None

        def mock_method_1(self):
            return True

        def get_mock_attr(self):
            self.mock_attr = 1

    instance = TestClass()
    # First, check attr is None and that class raises AttrNotSet error when method is attempted to be called
    assert instance.mock_attr is None
    with pytest.raises(AttrNotSet):
        instance.mock_method_1()
    # Now, set attr to something Truthy, and check that methods can now actually run
    instance.get_mock_attr()
    assert instance.mock_method_1() == 1
