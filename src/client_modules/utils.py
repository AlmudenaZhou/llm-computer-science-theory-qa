import os
import importlib


def get_parent_folders_inside_project():
    """
    It considers snake_case folder names.

    Returns the parent folder of this file that are inside the project folder.
    """
    cwd = os.getcwd().lower()
    current_file = os.path.abspath(__file__).lower()

    parent_directory = os.path.dirname(current_file)
    
    parent_directory = parent_directory.replace(cwd, '')
    parent_folders = parent_directory.split(os.sep)[1:]
    
    return parent_folders


def to_camel_case(snake_str):
    snake_str = snake_str.lower()
    camel_str = "".join(x.capitalize() for x in snake_str.split("_"))
    camel_str = camel_str.replace("Openai", "OpenAI")
    return camel_str


def import_module_from_name(parent_folders: list, module_name):
    module_path = '.'.join(parent_folders) + f'.{module_name}'
    module = importlib.import_module(module_path)
    return module


def import_class_from_name_in_module(class_name, parent_folders, module_name):
    module = import_module_from_name(parent_folders, module_name)
    class_obj = getattr(module, class_name)
    return class_obj


def import_openai_llms(module_name):
    parent_folders = get_parent_folders_inside_project()
    parent_folders += ["llms", "openai"]
    
    class_name = f"{to_camel_case(module_name)}Client"
    llm_class = import_class_from_name_in_module(class_name, 
                                                 parent_folders,
                                                 module_name)
    return llm_class


def import_embeddings(module_name):
    parent_folders = get_parent_folders_inside_project()
    parent_folders += ["embeddings"]
    class_name = f"{to_camel_case(module_name)}EmbeddingModel"
    emb_class = import_class_from_name_in_module(class_name, 
                                                 parent_folders,
                                                 module_name)
    return emb_class



def check_model_client_name(valid_list, client_name, env_var_name):
    if client_name not in valid_list:
        raise ValueError(f"{env_var_name} in .env must belong" 
                         f"to {valid_list}. {client_name} is not a valid name.")


def check_embedding_model(emb_name):
    valid_list = ["transformer", "azure_openai"]
    check_model_client_name(valid_list, emb_name, "EMBEDDING_CLIENT")


def check_llm_model(emb_name):
    valid_list = ["openai", "azure_openai", "ollama"]
    check_model_client_name(valid_list, emb_name, "LLM_CLIENT")


print(get_parent_folders_inside_project())
