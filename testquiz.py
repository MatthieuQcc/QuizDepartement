import streamlit as st
import pandas as pd
import random

def run():
    st.set_page_config(
        page_title="Devine le département",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
</style>
""", unsafe_allow_html=True)

# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'score': 0, 'user_input': '', 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load department data
departments_df = pd.read_csv('departement.csv', encoding='utf-8', delimiter=',')
departments_data = departments_df[['N°', 'Département']].rename(columns={'N°': 'number', 'Département': 'department'}).to_dict('records')

# Shuffle the questions at the start
if 'shuffled_data' not in st.session_state:
    st.session_state.shuffled_data = random.sample(departments_data, len(departments_data))

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.user_input = ''
    st.session_state.answer_submitted = False
    st.session_state.shuffled_data = random.sample(departments_data, len(departments_data))

def submit_answer():
    # Check if an input has been provided
    if st.session_state.user_input:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        # Check if the input is correct
        if st.session_state.user_input == str(st.session_state.shuffled_data[st.session_state.current_index]['number']):
            st.session_state.score += 1
    else:
        # If no input, show a message and do not mark as submitted
        st.warning("Entrez un numéro avant de valider...")

def next_question():
    st.session_state.current_index += 1
    st.session_state.user_input = ''
    st.session_state.answer_submitted = False

# Title and description
st.title("Devine le département")

# Progress bar
progress_bar_value = (st.session_state.current_index + 1) / len(st.session_state.shuffled_data)
st.metric(label="Score", value=f"{st.session_state.score} / {len(st.session_state.shuffled_data)}")
st.progress(progress_bar_value)

# Display the question
current_item = st.session_state.shuffled_data[st.session_state.current_index]
st.subheader(f"Question {st.session_state.current_index + 1}")
st.title(f"Quel numéro correspond à ce département: {current_item['department']}?")

# User input for the answer
if not st.session_state.answer_submitted:
    st.session_state.user_input = st.text_input("Entre le numéro du département:", value=st.session_state.user_input)

# Submission button and response logic
if st.session_state.answer_submitted:
    correct_answer = str(current_item['number'])
    if st.session_state.user_input == correct_answer:
        st.success(f"{st.session_state.user_input} est la bonne réponse! Gg!")
    else:
        st.error(f"{st.session_state.user_input} n'est pas la bonne réponse. La réponse est {correct_answer}. Trolleur.")
    if st.session_state.current_index < len(st.session_state.shuffled_data) - 1:
        st.button('Next', on_click=next_question)
    else:
        st.write(f"Quiz finito! Ton score final: {st.session_state.score} / {len(st.session_state.shuffled_data) * 10}")
        if st.button('Rejouer', on_click=restart_quiz):
            pass
else:
    st.button('Valider', on_click=submit_answer)
