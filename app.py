#=====================================================
#IMPORTS
#=====================================================
import requests
import random
import html
import time
import streamlit as st

#=====================================================
# CATEGORY ID TRANSLATION LIST
#=====================================================

category_id_dic = {
"General Knowledge" : 9,
"Film" : 11,
"Music" : 12,
"Television" : 14,
"Video Games" : 15,
"Board Games" : 16,
"Sports":21,
"Geography":22,
"History":23,
"Politics":24,
"Art":25,
"Celebrities":26,
"Animals":27,
"Vehicles":28
}

category_id_list = list(category_id_dic.keys())

#=====================================================
# CATEGORY SELECTION FUNCTION
#=====================================================
def SELECT_CATEGORY(rounds):
    st.write("The categories you can choose from are:")

    cols = st.columns(3)
    for i, category_name in enumerate(st.session_state.category_id_list):
        with cols[i % 3]:
            if st.button(category_name, key=f"cat_{category_name}", use_container_width=True):
                chosen_category_key = category_name
                chosen_category_id = category_id_dic[chosen_category_key]
                st.session_state.selected_category_name = chosen_category_key
                st.session_state.selected_category_id = chosen_category_id
                st.session_state.category_id_list.remove(chosen_category_key)

                questions = FETCH_TRIVIA_QUESTIONS(chosen_category_id)
                st.session_state.questions = questions
                st.session_state.q_index = 0
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.session_state.last_selected_answer = None
                st.session_state.last_correct_answer = None
                st.session_state.last_was_correct = None

                if len(st.session_state.questions) > 0:
                    q = st.session_state.questions[0]
                    st.session_state.correct_answer = html.unescape(q["correct_answer"])
                    incorrect_raw = q["incorrect_answers"]
                    incorrect_clean = [html.unescape(a) for a in incorrect_raw]
                    options = incorrect_clean + [st.session_state.correct_answer]
                    random.shuffle(options)
                    st.session_state.options = options

                st.rerun()

#=====================================================
# API CALL TO FETCH TRIVIA QUESTIONS
#=====================================================
def FETCH_TRIVIA_QUESTIONS(category_id):
    url = f"https://opentdb.com/api.php?amount=4&category={category_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and isinstance(data["results"], list):
            return data["results"]
        return []
    else:
        return []



#=====================================================
# VARIABLES USED IN THE QUIZ APPLICATION
#=====================================================
score = 0

#=====================================================
# PROGRAM START
#=====================================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "rounds" not in st.session_state:
    st.session_state.rounds = 0

if "category_id_list" not in st.session_state:
    st.session_state.category_id_list = list(category_id_dic.keys())

if "selected_category_id" not in st.session_state:
    st.session_state.selected_category_id = None

if "selected_category_name" not in st.session_state:
    st.session_state.selected_category_name = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "options" not in st.session_state:
    st.session_state.options = []

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = ""

if "answered" not in st.session_state:
    st.session_state.answered = False

if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

if "last_selected_answer" not in st.session_state:
    st.session_state.last_selected_answer = None

if "last_correct_answer" not in st.session_state:
    st.session_state.last_correct_answer = None

if "last_was_correct" not in st.session_state:
    st.session_state.last_was_correct = None


st.title("Welcome to my quiz game")
st.write("The quiz will have 4 rounds, and each round has 4 questions.")
st.write("To start you must select a category.")

if st.session_state.rounds >= 4:
    st.success(f"Quiz complete! Your final score is: {st.session_state.score}")
    if st.button("Restart"):
        st.session_state.score = 0
        st.session_state.rounds = 0
        st.session_state.category_id_list = list(category_id_dic.keys())
        st.session_state.selected_category_id = None
        st.session_state.selected_category_name = None
        st.session_state.questions = []
        st.session_state.q_index = 0
        st.session_state.options = []
        st.session_state.correct_answer = ""
        st.session_state.answered = False
        st.session_state.user_choice = None
        st.session_state.last_selected_answer = None
        st.session_state.last_correct_answer = None
        st.session_state.last_was_correct = None
        st.rerun()
else:
    st.write(f"Round {st.session_state.rounds + 1} of 4")
    st.write(f"Score: {st.session_state.score}")

    if st.session_state.selected_category_id is None:
        SELECT_CATEGORY(st.session_state.rounds)
    else:
        if not st.session_state.questions or len(st.session_state.questions) == 0:
            st.error("No questions returned. Please pick a different category.")
            if st.button("Pick another category"):
                st.session_state.selected_category_id = None
                st.session_state.selected_category_name = None
                st.session_state.questions = []
                st.session_state.q_index = 0
                st.session_state.options = []
                st.session_state.correct_answer = ""
                st.session_state.answered = False
                st.session_state.user_choice = None
                st.session_state.last_selected_answer = None
                st.session_state.last_correct_answer = None
                st.session_state.last_was_correct = None
                st.rerun()
        else:
            question = st.session_state.questions[st.session_state.q_index]
            question_text = html.unescape(question["question"])

            st.write("Thank you, you have chosen the following category " + st.session_state.selected_category_name)
            st.write(f"Question {st.session_state.q_index + 1}:")
            st.write(question_text)

            st.session_state.user_choice = st.radio(
                "select your answer:",
                st.session_state.options,
                index=None,
                key=f"radio_{st.session_state.rounds}_{st.session_state.q_index}",
                disabled=st.session_state.answered
            )

            if st.button("Submit", disabled=st.session_state.answered, key=f"submit_{st.session_state.rounds}_{st.session_state.q_index}"):
                if st.session_state.user_choice is None:
                    st.warning("Invalid")
                    st.stop()

                selected_answer = st.session_state.user_choice
                st.session_state.last_selected_answer = selected_answer
                st.session_state.last_correct_answer = st.session_state.correct_answer

                if selected_answer == st.session_state.correct_answer:
                    st.session_state.score += 1
                    st.session_state.last_was_correct = True
                else:
                    st.session_state.last_was_correct = False

                st.session_state.answered = True
                st.rerun()

            if st.session_state.answered:
                if st.session_state.last_was_correct is True:
                    st.success("Correct!")
                elif st.session_state.last_was_correct is False:
                    st.error("Incorrect.")

                if st.session_state.last_correct_answer is not None:
                    st.info(f"The correct answer was: {st.session_state.last_correct_answer}")

                if st.button("Next", key=f"next_{st.session_state.rounds}_{st.session_state.q_index}"):
                    st.session_state.q_index += 1
                    st.session_state.answered = False
                    st.session_state.user_choice = None
                    st.session_state.last_selected_answer = None
                    st.session_state.last_correct_answer = None
                    st.session_state.last_was_correct = None

                    if st.session_state.q_index >= len(st.session_state.questions):
                        st.session_state.rounds += 1
                        st.session_state.selected_category_id = None
                        st.session_state.selected_category_name = None
                        st.session_state.questions = []
                        st.session_state.q_index = 0
                        st.session_state.options = []
                        st.session_state.correct_answer = ""
                        st.rerun()
                    else:
                        q = st.session_state.questions[st.session_state.q_index]
                        st.session_state.correct_answer = html.unescape(q["correct_answer"])
                        incorrect_raw = q["incorrect_answers"]
                        incorrect_clean = [html.unescape(a) for a in incorrect_raw]
                        options = incorrect_clean + [st.session_state.correct_answer]
                        random.shuffle(options)
                        st.session_state.options = options
                        st.rerun()
