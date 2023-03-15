def trim_text(text: str, max_length: int) -> str:
    """Trim a string to a maximum length

    Args:
        text: The text to trim
        max_length: The maximum length of the text

    Returns:
        The trimmed text
    """
    if len(text) > max_length:
        return text[: max_length - 3] + "..."
    return text
