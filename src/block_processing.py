block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown :str):
    lines = markdown.split("\n\n")
    stripped_lines = list(map(lambda l: l.strip(), lines))
    blocks = list(filter(lambda l: l != "", stripped_lines))
    return blocks

def block_to_block_type(block):
    if block[:2] == "# ":
        return "heading"
    if block[:3] == "## ":
        return "heading"
    if block[:4] == "### ":
        return "heading"
    if block[:5] == "#### ":
        return "heading"
    if block[:6] == "##### ":
        return "heading"
    if block[:7] == "###### ":
        return "heading"
    if block[:8] == "####### ":
        return "heading"
    
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    
    lines = block.split("\n")

    if block[0] == ">":
        return "quote"
    
    ordered_list = True
    for i in range(len(lines)):
        if lines[i][:len(f"{i + 1}") + 2] != f"{i + 1}. ":
            ordered_list = False
    if ordered_list:
        return "ordered_list"
    
    if all(map(lambda l: l[:2] == "* " or l[:2] == "- ", lines)):
        return "unordered_list"
    
    return "paragraph"

