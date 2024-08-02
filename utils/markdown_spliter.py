import re
from typing import List

chunk_size = 10000


def split_text(text: str) -> List[str]:
    markdown_sections = []
    lines = text.split("\n")

    current_section = ""

    for line in lines:
        header_match = re.match(r"^(#+)\s(.*)", line)
        if header_match:
            if current_section != "":
                markdown_sections.append(current_section.strip())
            current_section = f"{header_match.group(0)}\n"
        else:
            current_section += line + "\n"

    markdown_sections.append(current_section.strip())

    return markdown_sections


def split_text_v1(text: str) -> List[str]:
    markdown_sections = []
    lines = text.split("\n")
    current_section = ""
    # in_code_block = False

    for line in lines:
        # 检查当前行是否为代码块的开始或结束
        if line.strip() == "```":
            # in_code_block = not in_code_block
            current_section += line + "\n"
            continue

        # 如果当前行是标题，且不在代码块内，且当前部分不为空，则添加当前部分到sections
        header_match = re.match(r"^(#{1,3})\s(.*)", line)

        num_of_occurrences = current_section.count("```")
        in_code_block = num_of_occurrences % 2 == 0

        if header_match and in_code_block:
            if current_section != "":
                markdown_sections.append(current_section.strip())

            current_section = f"{header_match.group(0)}\n"
        elif len(current_section) > chunk_size and in_code_block:
            current_section += line + "\n"
            markdown_sections.append(current_section.strip())
            current_section = ""
        else:
            current_section += line + "\n"

    # 添加最后一部分到sections
    if current_section.strip() != "":
        markdown_sections.append(current_section.strip())

    return markdown_sections
