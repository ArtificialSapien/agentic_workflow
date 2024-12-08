def ensure_markdown_format(text):
    # Split the text into lines
    lines = text.split("\n")

    # Initialize a list to hold the formatted lines
    formatted_lines = []

    # Iterate through each line
    for line in lines:
        # Check if the line starts with a markdown header or list item
        if line.startswith("#") or line.startswith("-") or line.startswith("["):
            formatted_lines.append(line)
        else:
            # Add a newline before and after paragraphs
            if line.strip() == "":
                formatted_lines.append("")
            else:
                formatted_lines.append(line)

    # Join the formatted lines back into a single string
    formatted_text = "\n".join(formatted_lines)

    return formatted_text
