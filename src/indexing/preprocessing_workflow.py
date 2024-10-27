from src.indexing.preprocessing.add_pdf_book import save_book_qa_workflow
from src.indexing.preprocessing.unify_qa_files import unify_qa_files
from src.indexing.preprocessing.dataset_cleaning import dataset_cleaning


def preprocessing_workflow():

    save_book_qa_workflow()
    unify_qa_files()
    dataset_cleaning()


if __name__ == "__main__":
    preprocessing_workflow()
