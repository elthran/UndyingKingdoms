import pytest

from lib.controller_utils import convert_to_view_function
from tests.lib.controller.fake_controller import FakeController


# NOTE: the controller class must be in a different file else the
# dynamic lookup with cause infinite recursion.
@pytest.mark.usefixtures("ctx")
class TestControllerUtils:
    def test_string_response(self):
        view_function = convert_to_view_function(FakeController.string_response)
        assert view_function()

    def test_string_with_status_response(self):
        view_function = convert_to_view_function(FakeController.string_with_status_response)
        assert view_function()

    def test_dictionary_response(self):
        view_function = convert_to_view_function(FakeController.dictionary_response)
        assert view_function()

    def test_dictionary_with_status_response(self):
        view_function = convert_to_view_function(FakeController.dictionary_with_status_response)
        assert view_function()

    def test_json_response(self):
        view_function = convert_to_view_function(FakeController.json_response)
        assert view_function()

    def test_json_with_status_response(self):
        view_function = convert_to_view_function(FakeController.json_with_status_response)
        assert view_function()
