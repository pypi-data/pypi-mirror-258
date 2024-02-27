import uuid
import re

def convert_tag(content: str, tag: str, docstring: str, existing_id: re.Match = None) -> str:
    """Converts a tag to a docstring and replaces it in the content.

    Args:
        content (str): the content of the file
        tag (str): the tag to convert
        docstring (str): the docstring to replace the tag with
        existing_id (re.Match): the existing id of the tag

    Returns:
        str: the content with the tag replaced by the docstring
    """
    if existing_id:
        existing_id = existing_id.group(1)
        # Replace where 
        start_content_tag = f'<AutoDoc.Content id="{existing_id}">'
        end_content_tag = f'</AutoDoc.Content id="{existing_id}">'
        search = f"<!--{start_content_tag}"+r"-->(.*?)<!--"+f"{end_content_tag}-->"
        existing_place = re.search(search, content, re.DOTALL)
        if existing_place:
            existing_place = existing_place.group(0)
            new_docstring = f"<!--{start_content_tag}-->\n{docstring}\n<!--{end_content_tag}-->\n"
            content = content.replace(existing_place, new_docstring)
        else:
            new_docstring = f"\n{tag}\n<!--{start_content_tag}-->\n{docstring}\n<!--{end_content_tag}-->\n"
            content = content.replace(tag, new_docstring)
    else:
        id = str(uuid.uuid4())[:6]
        start_content_tag = f'<AutoDoc.Content id="{id}">'
        end_content_tag = f'</AutoDoc.Content id="{id}">'
        new_tag = tag.replace("/>", f" id=\"{id}\"/>")
        if tag[:4] != "<!--":
            new_tag = f"<!--{new_tag}-->"
        content = content.replace(tag, f"\n{new_tag}\n<!--{start_content_tag}-->\n{docstring}\n<!--{end_content_tag}-->\n")
    return content
