import re
from extract_markdown_images import extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        print(sections)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = r'(\[.*?\]\(.*?\))'

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            continue

        parts = re.split(link_pattern, old_node.text)

        for part in parts:
            if not part:
                continue
            
            if re.match(link_pattern, part):
                link_text, link_url = extract_markdown_links(part)[0]
                new_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
                
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def extract_title(markdown):
    """
    Extracts the H1 header from the Markdown text.

    Args:
        markdown (str): The input Markdown string.

    Returns:
        str: The text of the H1 header, with the # and whitespace removed.

    Raises:
        ValueError: If no H1 header is found.
    """
    # Regular expression to find a single H1 header
    match = re.search(r'^#\s*(.+)', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise ValueError("No H1 header found in the Markdown text.")

def block_to_block_type(block):
    """
    Determines the type of a Markdown block.

    Args:
        block (str): A single block of Markdown text, stripped of leading/trailing whitespace.

    Returns:
        str: The type of the block ("heading", "code", "quote", "unordered_list",
             "ordered_list", "paragraph").
    """
    if re.match(r'^#{1,6}\s', block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.splitlines()):
        return "quote"
    elif all(re.match(r'^[*-]\s', line) for line in block.splitlines()):
        return "unordered_list"
    elif all(re.match(r'^\d+\.\s', line) for line in block.splitlines()):
        return "ordered_list"
    else:
        return "paragraph"



class HTMLNode:
    def __init__(self, tag, content=None, children=None):
        self.tag = tag
        self.content = content if content else ""
        self.children = children if children else []

    def __str__(self):
        if self.children:
            children_str = "".join(str(child) for child in self.children)
            return f"<{self.tag}>{children_str}</{self.tag}>"
        return f"<{self.tag}>{self.content}</{self.tag}>"

def block_to_block_type(block):
    """
    Takes a single block of markdown text as input and returns a string representing the type of block it is.
    """
    lines = block.splitlines()

    # Check for heading
    if block.startswith("#"):
        if len(lines) == 1 and block.lstrip('#').startswith(' '):
            return "heading"

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code block"

    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return "quote block"

    # Check for unordered list block
    if all(line.startswith(('* ', '- ')) for line in lines):
        return "unordered list block"

    # Check for ordered list block
    try:
        numbers = [int(line.split(".")[0]) for line in lines]
        if all(line.startswith(f"{num}. ") for num, line in zip(range(1, len(lines) + 1), lines)):
            return "ordered list block"
    except (ValueError, IndexError):
        pass

    # Default to normal paragraph
    return "normal paragraph"

def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode.
    """
    lines = markdown.strip().split("\n\n")
    root = HTMLNode("div")

    for block in lines:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            level = block.count("#", 0, block.find(" "))
            content = block.lstrip("# ")
            root.children.append(HTMLNode(f"h{level}", content=content))
        elif block_type == "code block":
            content = block.strip("```")
            root.children.append(HTMLNode("pre", children=[HTMLNode("code", content=content)]))
        elif block_type == "quote block":
            content = "\n".join(line.lstrip("> ") for line in block.splitlines())
            root.children.append(HTMLNode("blockquote", content=content))
        elif block_type == "unordered list block":
            ul = HTMLNode("ul")
            for line in block.splitlines():
                ul.children.append(HTMLNode("li", content=line[2:]))
            root.children.append(ul)
        elif block_type == "ordered list block":
            ol = HTMLNode("ol")
            for line in block.splitlines():
                ol.children.append(HTMLNode("li", content=line[line.find(".") + 2:]))
            root.children.append(ol)
        else:  # Normal paragraph
            root.children.append(HTMLNode("p", content=block))

    return root


    
