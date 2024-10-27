import json
from collections import Counter
import numpy as np


def load_qa_json():

    with open("../../data/all_qa.json") as file:
        intents = json.load(file)

    return intents


def prepare_patterns_responses_lists(intents):

    combined_list = []
    questions_list = []
    responses_list = []

    for intent in intents:
        combined = f"{intent['document']} {'\n'.join(intent['patterns'])}-{'\n'.join(intent['responses'])}"
        combined_list.append(combined)
        questions_list.append('\n'.join(intent['patterns']))
        responses_list.append('\n'.join(intent['responses']))

    combined_list = np.array(combined_list)
    questions_list = np.array(questions_list)
    responses_list = np.array(responses_list)

    return combined_list, questions_list, responses_list


def clean_same_combined_qa_from_intents(intents, combined_list):

    queries_with_same_qa = list(filter(lambda x: x[1] > 1, Counter(combined_list).most_common()))

    if queries_with_same_qa:
        qa_index_to_delete = [np.where(combined_list == qa[0])[0][1:] for qa in queries_with_same_qa]
        qa_index_to_delete = np.concatenate(qa_index_to_delete)

    questions_list = np.delete(questions_list, qa_index_to_delete)
    responses_list = np.delete(responses_list, qa_index_to_delete)

    qa_index_to_delete.sort()

    for ind_index in qa_index_to_delete[::-1]:
        intents.pop(ind_index)
    return intents


def clean_same_question_from_intents(intents, questions_list):
    queries_with_same_q = list(filter(lambda x: x[1] > 1, Counter(questions_list).most_common()))

    if queries_with_same_q:
        if isinstance(questions_list, np.ndarray):
            same_q_index = [np.where(questions_list == q[0])[0] for q in queries_with_same_q]

            q_index_to_delete = []
            for same_q_index_batch in same_q_index:
                responses_same_q = [intents[index]['responses'] for index in same_q_index_batch[1:]]
                responses_same_q = [x for xs in responses_same_q for x in xs]
                intents[same_q_index_batch[0]]['responses'].extend(responses_same_q)
                q_index_to_delete.extend(same_q_index_batch[1:])
    responses_list = np.delete(responses_list, q_index_to_delete)

    q_index_to_delete.sort()

    for ind_index in q_index_to_delete[::-1]:
        intents.pop(ind_index)
    return intents


def clean_same_answer_from_intents(intents, responses_list):
    queries_with_same_a = list(filter(lambda x: x[1] > 1, Counter(responses_list).most_common()))

    if queries_with_same_a:
        same_a_index = [np.where(responses_list == a[0])[0] for a in queries_with_same_a]
        same_a_index = np.concatenate(same_a_index)

    intents.pop(same_a_index[0])
    return intents


def save_cleaned_qa(intents):
    with open("../../data/all_qa_cleaned.json", "w") as file:
        json.dump(intents, file)


def dataset_cleaning():

    intents = load_qa_json()
    combined_list, questions_list, responses_list = prepare_patterns_responses_lists(intents)
    intents = clean_same_combined_qa_from_intents(intents, combined_list)
    intents = clean_same_question_from_intents(intents, questions_list)
    intents = clean_same_answer_from_intents(intents, responses_list)
    save_cleaned_qa(intents)
