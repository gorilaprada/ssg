import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class testHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "Some text content")
        node2 = HTMLNode("<p>", "Some text content")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("<p>", "Some text content")
        node2 = HTMLNode("<h1>", "Some Title")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("<img>", "Some text content", None,  { "href": "www.image.com" })
        self.assertEqual(' href="www.image.com"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("<div>", None, None, { "url": "www.world.com"})
        self.assertEqual("HTMLNode(<div>, None, children: None, {'url': 'www.world.com'})", repr(node))

    # LeafNode Tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # ParentNode test
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("img", "the image", { "href": "www.boot.dev" })
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><img href="www.boot.dev">the image</img></span></div>',
        )



if __name__ == "__main__":
    unittest.main()
