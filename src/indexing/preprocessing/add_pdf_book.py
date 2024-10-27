import os
import re
import json
import pymupdf4llm


def load_book_qa():
    pdf_name = "500 Data Science Interview Questions.pdf"
    md_text = pymupdf4llm.to_markdown(f"../../data/books/{pdf_name}", write_images=True,
                                    image_path=os.path.join("..", "..", "data", "books", pdf_name.split(".")[0]), 
                                    page_chunks=False, hdr_info=False)
    return md_text


def extract_regex_patterns_from_md_text(markdown_text, patterns):
    question_answer_pairs = []

    for pattern in patterns:
        match = pattern.findall(markdown_text)
        for id, question, answer in match:
            question = question.replace("**", "")
            question = question.replace("\n", " ")
            answer = answer.replace("\n", " ")
            question_answer_pairs.append((id, question.strip(), answer.strip()))

    return question_answer_pairs


def get_qa_from_book_md(md_text):

    question_patterns = r"\*\*Question|\*\*[0-9]{1,3}\)|\*\*\d{1,3}\.|\*\*\[?Q\d{1,3}\.|\[toggle_content|$"
    preanswer_patterns = r"\*\*\s*"
    answer_patterns = r"\n[^\*][^\*].*?"

    # Pattern 1: **Question [0-9]{1,3}. Question text** **Answer:** Answer text
    pattern1 = re.compile(rf"\*\*Question ([0-9]{{1,3}})\.?\s*(.+?){preanswer_patterns}\*?\*?Answer:\*?\*?(.*?)(?={question_patterns})", re.DOTALL)

    # Pattern 2: **[0-9]{1,3}) Question text** Answer text
    pattern2 = re.compile(rf"\*\*([0-9]{{1,3}})\)(.+?){preanswer_patterns}({answer_patterns})(?={question_patterns})", re.DOTALL)

    # Pattern 3: **Q?[0-9]{1,3}. Question text** Answer text
    pattern3 = re.compile(rf"\*\*Q?(\d{{1,3}})\.\s*(.+?){preanswer_patterns}({answer_patterns})(?={question_patterns})", re.DOTALL)

    # Pattern 4: **[Q?[0-9]{1,3}. Question text](Answer image)**
    pattern4 = re.compile(rf"\*\*\[Q?(\d{{1,3}})\.\s*(.+?)\]\s*\(({answer_patterns})\)\*\*(?={question_patterns})", re.DOTALL)

    # Pattern 5: toggle_content ... Q.[0-9]{1,3} Question text? Answer text
    pattern5 = re.compile(rf"toggle_content.*Q?(\d{{1,3}})\.\s*(.+?\?)\s*({answer_patterns})(?={question_patterns})", re.DOTALL)

    patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]
    question_answer_pairs = extract_regex_patterns_from_md_text(md_text.replace("\n\n-----\n\n", ""), patterns)

    book_qa = []
    for i, question, answer in question_answer_pairs:
        book_qa.append({"question_n": i,
        "question": question,
        "answer": answer})
    
    return book_qa


def write_book_qa(book_qa):
    with open("../../data/500 Data Science Interview Questions.json", "w") as file:
        json.dump(book_qa, file)


def save_book_qa_workflow():
    md_text = load_book_qa()
    book_qa = get_qa_from_book_md(md_text)
    write_book_qa(book_qa)
