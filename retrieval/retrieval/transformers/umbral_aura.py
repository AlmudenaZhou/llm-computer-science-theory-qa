from typing import List, Tuple

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def fixed_chunker(document_data: Tuple[str, str], *args, **kwargs) -> List[Tuple[str, str, str]]:
    """
    Template for fixed length chunking of a document.

    Args:
        document_data (Tuple[str, str]): Tuple containing document_id and document_content.
        max_length (int, optional): Maximum length of each chunk from kwargs.

    Returns:
        List[Tuple[str, str, str]]: List of tuples containing document_id, document_content, and chunk_text.
    """
    document_id, document_content = document_data
    max_length = kwargs.get('max_length', 1000)  # Default value if not provided
    chunks = []

    for i in range(0, len(document_content), max_length):
        chunk = document_content[i:i+max_length]
        chunks.append((document_id, document_content, chunk))

    return chunks


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'