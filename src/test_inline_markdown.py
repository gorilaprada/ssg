import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
    extract_markdown_links,
    extract_markdown_images,
)

class testInlineMarkdown(unittest.TestCase):
    # Test function split_nodes_delimiter
    def test_text(self):
        node = TextNode("This is a text node with some `def foo(): return` and more `def foo2(): return`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node2 = TextNode("def foo(): return", TextType.CODE)
        node3 = TextNode("def foo2(): return", TextType.CODE)
        self.assertEqual(new_nodes[1], node2)
        self.assertEqual(new_nodes[3], node3)

    def test_full_output(self):
        node = TextNode("This is a text node with some _italic1_ and more _italic2_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node0 = TextNode("This is a text node with some ", TextType.TEXT)
        node1 = TextNode("italic1", TextType.ITALIC)
        node2 = TextNode(" and more ", TextType.TEXT)
        node3 = TextNode("italic2", TextType.ITALIC)
        self.assertEqual(new_nodes, [node0, node1, node2, node3])

    def test_full_output2(self):
        node = TextNode("This is a text node with some **bold1** and **bold2** more ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node0 = TextNode("This is a text node with some ", TextType.TEXT)
        node1 = TextNode("bold1", TextType.BOLD)
        node2 = TextNode(" and ", TextType.TEXT)
        node3 = TextNode("bold2", TextType.BOLD)
        node4 = TextNode(" more ", TextType.TEXT)
        self.assertEqual(new_nodes, [node0, node1, node2, node3, node4])

    def test_two_nodes(self):
        big_node = TextNode("This is a text node", TextType.TEXT)
        big_node2 = TextNode("This is a text node with some code: `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([big_node, big_node2], "`", TextType.CODE)
        node0 = TextNode("This is a text node", TextType.TEXT)
        node1 = TextNode("This is a text node with some code: ", TextType.TEXT)
        node2 = TextNode("code", TextType.CODE)
        self.assertEqual(new_nodes, [node0, node1, node2])

    def test_node_with_type_CODE(self):
        big_node = TextNode("`def foo(): return`", TextType.CODE)
        new_nodes = split_nodes_delimiter([big_node], "`", TextType.CODE)
        node0 = TextNode("`def foo(): return`", TextType.CODE)
        self.assertEqual(new_nodes[0], node0)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
    # Test split_nodes_image and split_nodes_link
    def test_split_images(self):
        node = TextNode(
            "This is a text with an ![image](www.image.com) and another ![image2](www.image2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "www.image2.com"),

            ],
            new_nodes,
        )

    # Test extract_mardown_links, extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("[to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    # Test text_to_text_nodes
    def test_first(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_second(self):
        text = "Second try of **test_to_text_nodes** function `here is the code`. ![Screenshot](www.screenchot.com) and [see code on Codeberg](https://codeberg.com/gorilaprada/code)"
        new_nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("Second try of ", TextType.TEXT),
                TextNode("test_to_text_nodes", TextType.BOLD),
                TextNode(" function ", TextType.TEXT),
                TextNode("here is the code", TextType.CODE),
                TextNode(". ", TextType.TEXT),
                TextNode("Screenshot", TextType.IMAGE, "www.screenchot.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("see code on Codeberg", TextType.LINK, "https://codeberg.com/gorilaprada/code"),

            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()
