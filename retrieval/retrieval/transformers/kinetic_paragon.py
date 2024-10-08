from typing import List, Tuple
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def byte_pair_encoding_tokenizer(document_data: Tuple[str, str, str], *args, **kwargs) -> Tuple[str, str, str, List[str]]:
    """
    Tokenize text using Byte Pair Encoding to create subword units.

    Args:
        document_data (Tuple[str, str, str]): Tuple containing document_id, document_content, and chunk.
    Returns:
        Tuple[str, str, str, List[str]]: Tuple containing document_id, document_content, chunk, and tokens.
    """
    document_id, document_content, chunk = document_data
    vocab_size = kwargs['vocab_size']
    min_frequency = kwargs.get('min_frequency', 2)
    special_tokens = kwargs.get('special_tokens', ["<s>", "</s>", "<unk>", "<pad>"])

    # Assuming a hypothetical library `byte_pair_encoding` is used here.
    # You would replace this with actual BPE tokenization logic.
    from byte_pair_encoding import BytePairEncoder

    bpe = BytePairEncoder(vocab_size=vocab_size, min_frequency=min_frequency, special_tokens=special_tokens)
    tokens = bpe.encode(chunk)

    return document_id, document_content, chunk, tokens


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'