import streamlit as st
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(),override=True)
os.environ.get('GOOGLE_API_KEY')

def ask_and_get_answer(prompt): 
    # Creating a GenerativeModel instance using the Gemini-Pro-Vision model
    model = genai.GenerativeModel('gemini-pro')
    format="""json{"quiz": [{
   "question": "Which of the following is NOT a type of network topology?",
   "options": [
    "Bus",
    "Star",
    "Ring",
    "Tree"
   ],
   "answer": "Tree"
  },
  {
   "question": "Which layer of the OSI model is responsible for data transmission?",
   "options": [
    "Physical Layer",
    "Data Link Layer",
    "Network Layer",
    "Transport Layer"
   ],
   "answer": "Physical Layer"
  },
  
 ]
}
"""


    modified_prompt=f"always in the following format only {format}+{prompt}"

    # Generate a text response based on the prompt and image
    response = model.generate_content([prompt])

    return response.text

# Session state for user input and score
if 'subjet' not in st.session_state:
    st.session_state['subjet'] = ""
if 'topics' not in st.session_state:
    st.session_state['topics'] = ""
if 'no_of_questions' not in st.session_state:
    st.session_state['no_of_questions'] = 0
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'quiz_questions' not in st.session_state:
    st.session_state['quiz_questions'] = []

subjet = st.text_input("Enter subject name", key="subjet")
topics = st.text_input("Enter subject topics", key="topics")
no_of_questions = st.number_input("Enter number of questions for the test", min_value=1, max_value=10, step=1, key="no_of_questions")


def get_quiz(prompt):
     if prompt:
            with st.spinner('Running ...'):
                answer = ask_and_get_answer(prompt)
                print(answer)

                # Clean and process the response
                answer = (answer.replace("json", "").replace("JSON", "")
                          .lstrip("`").rstrip("`"))
                return answer

def generate_questions(answer):
     try:
                questions_data = eval(answer)
                print(questions_data)

                # Check if "quiz" or "questions" key exists and is a dictionary
                if isinstance(questions_data, dict) and ("quiz" in questions_data or "questions" in questions_data):
                    quiz_data = questions_data["quiz"] if "quiz" in questions_data else questions_data['questions']
                
                print(quiz_data)
                return quiz_data

            

               
     except SyntaxError:
                st.write("Error: Invalid JSON format in response")          
clicked = st.button("Start Quiz")
if __name__ == '__main__':
    if clicked:
        # Configure the generative AI model using the GOOGLE_API_KEY
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
        st.subheader('Dynamic Quiz ✨')
        prompt = f"Create a quiz in JSON format with {no_of_questions} multiple choice questions with four options and answers on {subjet} covering topics like {topics} ."
        answer=get_quiz(prompt)
        st.session_state['quiz_questions'] = generate_questions(answer)
        
    if st.session_state['quiz_questions']:
        for index, question_data in enumerate(st.session_state['quiz_questions']):
            st.write(f"Question {index+1}: {question_data['question']}")
            selected_option_index = st.radio(f"Options for Question {index+1}", options=question_data["options"], key=f"radio_{index}")
            st.session_state[f"selected_option_{index}"] = selected_option_index
    

    if st.session_state['quiz_questions']:
        if st.button("Submit"):
            st.session_state['score'] = 0  # Reset score
            st.write("answers")
            for index, question_data in enumerate(st.session_state['quiz_questions']):
                selected_option_index = st.session_state[f"selected_option_{index}"]
                correct_answer = question_data["answer"]
                st.write(f"question no{index+1}  {correct_answer}")
                
                

                # Check if selected answer is correct
                if selected_option_index == correct_answer:
                    st.session_state['score'] += 1  # Increment score for correct answer
                

            # Display final score
            st.write(f"Your final score: {st.session_state['score']}/{len(st.session_state['quiz_questions'])}")
