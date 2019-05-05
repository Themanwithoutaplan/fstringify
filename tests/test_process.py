import pytest

from fstringify.process import (
    no_skipping,
    rebuild_transformed_lines,
)

def test_no_skipping():
    code = """
    class Foo:
        def __init__(self):
            self.a = '1'
            sys.exit(
                "Exiting due to receiving %d status code when expecting %d."
                % (r.status_code, expected_status)
            )
    """
    lines, scope = no_skipping(code)
    assert lines == [4, 5, 6, 7]
    scoped = scope[4]
    assert scoped['indent'] == '            '
    assert scoped['raw_scope'] == [
       '            sys.exit(',
       '                "Exiting due to receiving %d status code '
       'when expecting %d."',
       '                % (r.status_code, expected_status)',
       '            )'
   ]
    assert "\n".join(scoped["strip_scope"]) == """sys.exit(
"Exiting due to receiving %d status code when expecting %d."
% (r.status_code, expected_status)
)"""


@pytest.mark.xfail
def test_indent():
    code = """
    def write_row(self, xf, row, row_idx):

        attrs = {'r': '%d' % row_idx}
            """
    lines, scope = no_skipping(code)
    scoped = scope[2]
    assert lines == [2, 3]
    assert scoped['raw_scope'] == [
        '',
         "        attrs = {'r': '%d' % row_idx}"
    ]
    assert scoped['indent'] == "        "
    assert "\n".join(scoped["strip_scope"]) == """\nattrs = {'r': '%d' % row_idx}"""


def test_rebuild_transformed_lines():
    code_block = """\nattrs = {'r': '%d' % row_idx}"""
    lines = rebuild_transformed_lines(code_block, "    ")
    assert lines == """    attrs = {'r': '%d' % row_idx}"""

