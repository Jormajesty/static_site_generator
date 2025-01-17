import re

def extract_markdown_images(text):
    """
    Extracts all markdown images from the given text.

    Args:
        text (str): Raw markdown text.

    Returns:
        list: A list of tuples where each tuple contains the alt text and the URL of an image.
    """
    # Regular expression to match markdown image syntax: ![alt text](URL)
    pattern = r'!\[(.*?)\]\((.*?)\)'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text):
    """
    Extracts all markdown links from the given text.

    Args:
        text (str): Raw markdown text.

    Returns:
        list: A list of tuples where each tuple contains the link text and the URL of a link.
    """
    # Regular expression to match markdown link syntax: [link text](URL)
    pattern = r'\[(.*?)\]\((.*?)\)'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    return matches