"""
Test the namedict
"""
import pytest

from gopher_render.rendering import Renderer, InlineRenderer, BlockRenderer


def test_create():
    r = Renderer(None)
    i = InlineRenderer(None)
    b = BlockRenderer(None)
