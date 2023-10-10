def dict_to_cheat_sheet(data: dict, depth: int = 1) -> str:
    """Convert a nested dictionary to a markdown cheat sheet"""
    markdown_str = ""

    for key, value in data.items():
        if depth == 1:
            markdown_str += f"# {key}\n\n"
        else:
            markdown_str += f"{'  ' * (depth - 2)}- {key}\n"

        if isinstance(value, dict):
            markdown_str += dict_to_cheat_sheet(value, depth + 1)
        else:
            markdown_str += f"{'  ' * (depth - 1)}- {value}\n\n"

    return markdown_str


def print_markdown(md_str: str):
    for line in md_str.split("\n"):
        if line.startswith("#"):
            print("-" * 50)
        print(line)
