from contextlib import ExitStack

import pytest
from assertpy import assert_that

from obsidian_support.conversion.abstract_conversion import AbstractConversion
from obsidian_support.conversion.admonition.admonition_backquotes import AdmonitionBackquotesConversion
from obsidian_support.conversion.admonition.admonition_callout import AdmonitionCalloutConversion
from obsidian_support.conversion.comment.comment import CommentConversion
from obsidian_support.conversion.image_link.image_internal_link import ImageInternalLinkConversion
from obsidian_support.conversion.image_link.image_web_link import ImageWebLinkConversion
from obsidian_support.conversion.tags.tags import TagsConversion
from obsidian_support.markdown_convert import markdown_convert

"""
unit tests for `obsidian syntax` to `mkdocs-material syntax` conversion
"""


@pytest.mark.parametrize("test", ['indent', 'complex', 'edgecase', 'collapsible'])
def test_admonition_callout_conversion(test):
    assert_template("admonition/admonition_callout", test, AdmonitionCalloutConversion())


@pytest.mark.parametrize("test", ['basic'])
def test_admonition_backquotes_conversion(test):
    assert_template("admonition/admonition_backquotes", test, AdmonitionBackquotesConversion())


@pytest.mark.parametrize("test", ['basic', 'size', 'caption', 'size_caption'])
def test_image_internal_link_conversion(test):
    assert_template("image_link/image_internal_link", test, ImageInternalLinkConversion())


@pytest.mark.parametrize("test", ['basic', 'escape'])
def test_image_web_link_conversion(test):
    assert_template("image_link/image_web_link", test, ImageWebLinkConversion())


@pytest.mark.parametrize("test", ['basic'])
def test_tag_conversion(test):
    assert_template("tags", test, TagsConversion())


@pytest.mark.parametrize("test", ['basic'])
def test_comment_conversion(test):
    assert_template("comment", test, CommentConversion())


def assert_template(conversion_name: str, test: str, conversion: AbstractConversion):
    with ExitStack() as stack:
        src = stack.enter_context(open(f"markdowns/{conversion_name}/given/{test}.md", 'r'))
        dest = stack.enter_context(open(f"markdowns/{conversion_name}/expected/{test}.md", 'r'))
        given = src.read()
        expected = dest.read()

        # when
        actual = markdown_convert(given, None, conversion)

        # then
        assert_that(expected).is_equal_to(actual)
