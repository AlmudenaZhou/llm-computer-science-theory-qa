import os
import json


from mage_ai.shared.files import get_absolute_paths_from_all_files
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def ingest_files(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        path (str): Path to file directory.
        exclude_pattern (str): Exclude pattern for file paths.
        include_pattern (str): Include pattern for file paths.

    Yields:
        str: Content of each file.
    """

    with open(os.path.join(os.getcwd(), "data/intents.json")) as file:
        intents = json.load(file)["intents"]
    return intents


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'