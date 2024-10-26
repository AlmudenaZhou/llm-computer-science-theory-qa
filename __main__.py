import streamlit as st
import time
import uuid

from src.app.assistant import get_answer
from src.app.db import (
    init_db,
    save_conversation,
    save_feedback,
    get_recent_conversations,
    get_feedback_stats,
)


def print_log(message):
    print(message, flush=True)


def main():
    print_log("Starting the Interview Assistant application")
    st.title("Interview Assistant")

    st.session_state.disabled_feedback = True
    st.session_state.feedback_conversation_id = None

    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )
    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    if "first_flag" not in st.session_state:
        print_log("Database Initizalizing")
        init_db()
        st.session_state.first_flag = True

    model_choice = st.selectbox(
        "Select a model:",
        ["ollama/gemma:2b", "openai/gpt-35-turbo", "openai/gpt-4o"],
    )
    print_log(f"User selected model: {model_choice}")

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Ask"):
        print_log(f"User asked: '{user_input}'")
        with st.spinner("Processing..."):
            print_log(
                f"Getting answer from assistant using {model_choice} model"
            )
            start_time = time.time()
            answer_data = get_answer(user_input, model_choice)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(answer_data["answer"])

            st.caption("Chat Metrics")
            st.write(f"Response time: {answer_data['response_time']:.2f} seconds")
            st.write(f"Relevance: {answer_data['relevance']}")
            st.write(f"Model used: {answer_data['model_used']}")
            st.write(f"Total tokens: {answer_data['total_tokens']}")
            if answer_data["openai_cost"] > 0:
                st.write(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

            # Save conversation to database
            print_log("Saving conversation to database")
            save_conversation(
                st.session_state.conversation_id, user_input, answer_data
            )
            print_log("Conversation saved successfully")
            # Generate a new conversation ID for next question
            st.session_state.disabled_feedback = False
            st.session_state.feedback_conversation_id = st.session_state.conversation_id
            st.session_state.conversation_id = str(uuid.uuid4())

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1", disabled=st.session_state.disabled_feedback):
            st.session_state.count += 1
            print_log(
                f"Positive feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.feedback_conversation_id, 1)
            print_log("Positive feedback saved to database")
    with col2:
        if st.button("-1", disabled=st.session_state.disabled_feedback):
            st.session_state.count -= 1
            print_log(
                f"Negative feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.feedback_conversation_id, -1)
            print_log("Negative feedback saved to database")

    st.write(f"Current count: {st.session_state.count}")

    # Display recent conversations
    st.subheader("Recent Conversations")
    relevance_filter = st.selectbox(
        "Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]
    )
    recent_conversations = get_recent_conversations(
        limit=5, relevance=relevance_filter if relevance_filter != "All" else None
    )
    for conv in recent_conversations:
        st.write(f"Q: {conv['question']}")
        st.write(f"A: {conv['answer']}")
        st.write(f"Relevance: {conv['relevance']}")
        st.write(f"Model: {conv['model_used']}")
        st.write("---")

    # Display feedback stats
    feedback_stats = get_feedback_stats()
    st.subheader("Feedback Statistics")
    st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
    st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")


print_log("Streamlit app loop completed")


if __name__ == "__main__":
    print_log("Interview Assistant application started")
    main()
