import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class testTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_link_none(self):
        node = TextNode("Node", TextType.LINK, None)
        node2 = TextNode("Node", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_texttype_dif(self):
        node = TextNode("Node", "ougabouga", None)
        node2 = TextNode("Node", "ougabouga", None)
        self.assertEqual(node, node2)

    # Test function text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, { "src": "www.image.com", "alt": "This is an image"})

    def test_link(self):
        node = TextNode("Click Here", TextType.LINK, "www.link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, { "href": "www.link.com" })


if __name__ == "__main__":
    unittest.main()
