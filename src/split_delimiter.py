from textnode import TextType, TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    start_index, end_index = None, None
    inside_delimiter = False
    text = old_nodes[0].text
    split_string = text.split(delimiter)
    
    for i, char in enumerate(text):
        if char == delimiter:
            if not inside_delimiter:
                start_index = i + 1  # Capture the index after the opening backtick
                inside_delimiter = True
            else:
                end_index = i  # Capture the index of the closing backtick
                break 
    
    if start_index is not None and end_index is not None:
        captured_text = text[start_index:end_index]
        print(split_string)
        textNodes = []
        for string in split_string:
            if string == captured_text:
                textNodes.append(TextNode(string, text_type))
            else:
                textNodes.append(TextNode(string, TextType.TEXT))
        return textNodes

    else:
        print(f"Start index: {start_index}, End index: {end_index}")
