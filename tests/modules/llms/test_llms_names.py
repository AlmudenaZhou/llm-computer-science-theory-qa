import os
import glob

from src.client_modules.utils import get_parent_folders_inside_project, import_module_from_name, to_camel_case


def test_names():
    parent_folders = get_parent_folders_inside_project()
    parent_folders += ["llms", "openai"]
    path = os.path.join(*parent_folders)
    python_files = glob.glob(os.path.join(path, '*.py'))

    python_filenames = [os.path.basename(file) for file in python_files]

    for py_filename in python_filenames:
        py_filename = py_filename.replace('.py', '')
        if py_filename != 'base':
            module = import_module_from_name(parent_folders, py_filename)
            class_name = to_camel_case(py_filename) + 'Client'
            error_msg = f"""{py_filename}.py must have a class named 
                        {py_filename}Client"""
            assert hasattr(module, class_name), error_msg
