"""Test indent to spaces conversion function"""
from io import BytesIO

from pytest import mark, param

from indents_to_spaces.convert import convert_indents
from indents_to_spaces.pass_fail_constants import FAIL, PASS

from .file_utils import load_file, load_file_to_buffer


@mark.parametrize(
    "input_file_name,expected_file_name,indent_size",
    [
        param("spaces_2.tf", "spaces_2.tf", 2, id="spaces_2"),
        param("spaces_4.tf", "spaces_4.tf", 4, id="spaces_4"),
        param("indent_error.tf", "indent_error.tf", 2, id="indent_error_2"),
        param("indent_error.tf", "indent_error.tf", 4, id="indent_error_4"),
    ],
)
def test_convert_indents_no_changes(
    input_file_name: str, expected_file_name: str, indent_size: int) -> None:
    """Does converting the input file result in the expected file?"""
    buffer = load_file_to_buffer(input_file_name)
    expected = load_file(expected_file_name)

    return_code = convert_indents([buffer], indent_size)
    buffer.seek(0)

    assert buffer.read() == expected
    assert return_code == PASS


@mark.parametrize(
    "input_file_name,expected_file_name,indent_size",
    [
        param("tabs.tf", "spaces_2.tf", 2, id="tabs_2"),
        param("tabs.tf", "spaces_4.tf", 4, id="tabs_4"),
        param("indent_error_tabs.tf", "indent_error_spaces_2.tf", 2, id="error_tabs_2"),
        param("indent_error_tabs.tf", "indent_error_spaces_4.tf", 4, id="error_tabs_4"),
    ],
)
def test_convert_indents_changes(
    input_file_name: str, expected_file_name: str, indent_size: int
) -> None:
    """Does converting the input file result in the expected file?"""
    buffer = load_file_to_buffer(input_file_name)
    expected = load_file(expected_file_name)

    return_code = convert_indents([buffer], indent_size)
    buffer.seek(0)

    assert buffer.read() == expected
    assert return_code == FAIL
