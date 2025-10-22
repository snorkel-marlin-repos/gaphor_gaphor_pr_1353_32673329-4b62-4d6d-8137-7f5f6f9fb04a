import pytest

from gaphor import UML
from gaphor.diagram.copypaste import copy, paste_link
from gaphor.diagram.grouping import Group
from gaphor.diagram.tests.fixtures import copy_clear_and_paste_link
from gaphor.UML.components import ComponentItem, NodeItem


@pytest.fixture
def node_with_component(diagram, element_factory):
    node = element_factory.create(UML.Node)
    comp = element_factory.create(UML.Component)
    node_item = diagram.create(NodeItem, subject=node)
    comp_item = diagram.create(ComponentItem, subject=comp)

    Group(node_item, comp_item).group()
    comp_item.change_parent(node_item)

    assert comp_item.parent is node_item

    return node_item, comp_item


def test_copy_paste_of_nested_item(diagram, element_factory, node_with_component):
    node_item, comp_item = node_with_component

    buffer = copy({comp_item})

    (new_comp_item,) = paste_link(buffer, diagram, element_factory.lookup)

    assert new_comp_item.parent is node_item


def test_copy_paste_of_item_with_nested_item(
    diagram, element_factory, node_with_component
):
    node_item, comp_item = node_with_component

    buffer = copy(set(node_with_component))

    new_items = paste_link(buffer, diagram, element_factory.lookup)

    new_node_item = next(i for i in new_items if isinstance(i, NodeItem))
    new_comp_item = next(i for i in new_items if isinstance(i, ComponentItem))

    assert new_comp_item.parent is new_node_item


def test_copy_remove_paste_of_item_with_nested_item(
    diagram, element_factory, node_with_component
):

    new_items = copy_clear_and_paste_link(
        set(node_with_component), diagram, element_factory
    )

    new_node_item = next(i for i in new_items if isinstance(i, NodeItem))
    new_comp_item = next(i for i in new_items if isinstance(i, ComponentItem))

    assert new_comp_item.parent is new_node_item
