import streamlit as st
import time
from styles import get_custom_css
from screener import Screener

# Page Configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    layout="centered"
)

# Apply Custom Styles
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Screener
if 'screener' not in st.session_state:
    st.session_state.screener = Screener()

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'step' not in st.session_state:
    st.session_state.step = 'greeting'
if 'candidate_data' not in st.session_state:
    st.session_state.candidate_data = {}
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'info_field_index' not in st.session_state:
    st.session_state.info_field_index = 0

# Info Collection Fields
INFO_FIELDS = [
    ("full_name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "What is your phone number?"),
    ("location", "Where are you currently located?"),
    ("experience", "How many years of professional experience do you have?"),
    ("desired_role", "What position are you applying for?")
]

def add_message(role, content):
    st.session_state.history.append({"role": role, "content": content})

def bot_speak(content):
    add_message("assistant", content)

def process_input():
    user_input = st.session_state.user_input
    if not user_input.strip():
        return

    add_message("user", user_input)
    st.session_state.user_input = ""  # Clear input

    # Handle Exit
    if user_input.lower() in ['exit', 'quit', 'bye', 'stop', 'end']:
        st.session_state.step = 'finished'
        bot_speak("Thank you for your time. Our recruitment team will review your responses and reach out if there’s a match. Have a great day!")
        return

    # Logical Flow
    step = st.session_state.step
    screener = st.session_state.screener

    if step == 'greeting':
        st.session_state.step = 'collect_info'
        # Ask first info question
        field_key, field_q = INFO_FIELDS[0]
        bot_speak(f"Great! Let's get started. {field_q}")

    elif step == 'collect_info':
        idx = st.session_state.info_field_index
        current_field, _ = INFO_FIELDS[idx]
        
        # Validation
        valid = True
        if current_field == 'email' and not screener.validate_email(user_input):
            bot_speak("That doesn't look like a valid email. Please try again.")
            valid = False
        elif current_field == 'phone' and not screener.validate_phone(user_input):
            bot_speak("Please enter a valid phone number (digits only).")
            valid = False
        elif current_field == 'experience':
            if not screener.validate_experience(user_input):
                bot_speak("Please enter a valid number for years of experience.")
                valid = False
        
        if valid:
            st.session_state.candidate_data[current_field] = user_input
            st.session_state.info_field_index += 1
            
            if st.session_state.info_field_index < len(INFO_FIELDS):
                # Ask next question
                _, next_q = INFO_FIELDS[st.session_state.info_field_index]
                bot_speak(next_q)
            else:
                # Move to Tech Stack
                st.session_state.step = 'tech_stack'
                bot_speak("Thanks! Now, could you please list your tech stack (Programming languages, frameworks, databases, etc.)?")

    elif step == 'tech_stack':
        # Analyze Tech Stack
        tech_items = [t.strip() for t in user_input.replace('and', ',').split(',') if t.strip()]
        
        if len(user_input) < 3:
             bot_speak("Could you be a bit more specific about your tech stack?")
             return
             
        # Feature: Tech Stack Expansion
        # If user provides very few items (e.g. just "Python"), prompt for more.
        if len(tech_items) < 2:
            st.session_state.candidate_data['tech_temp'] = user_input
            st.session_state.step = 'tech_stack_expansion'
            bot_speak(f"You mentioned {user_input}. Do you also use any specific frameworks, libraries, or databases with it?")
            return

        # Proceed normally
        start_screening(user_input)

    elif step == 'tech_stack_expansion':
        # Combine previous and current input
        previous = st.session_state.candidate_data.get('tech_temp', '')
        combined_stack = f"{previous}, {user_input}"
        start_screening(combined_stack)

    elif step == 'screening':
        # Feature: Fallback on Bad Answers
        if not screener.validate_answer(user_input):
            bot_speak("It looks like your response may be incomplete. Could you please elaborate?")
            return

        # Sentiment Check & Encouragement
        sentiment = screener.analyze_sentiment(user_input)
        if sentiment == "uncertain":
            bot_speak(screener.get_encouragement())
        elif sentiment == "confident":
            # Occasional positive reinforcement
            import random
            if random.random() > 0.7:
                bot_speak(screener.get_confidence_acknowledgement())

        # Store answer
        info = st.session_state.candidate_data
        idx = st.session_state.current_question_index
        q_key = f"answer_q{idx+1}"
        info[q_key] = user_input
        
        st.session_state.current_question_index += 1
        
        if st.session_state.current_question_index < len(st.session_state.questions):
            next_q = st.session_state.questions[st.session_state.current_question_index]
            bot_speak(f"{st.session_state.current_question_index + 1}. {next_q}")
        else:
            st.session_state.step = 'finished'
            bot_speak("That concludes the technical screening. Thank you for your responses!")
            bot_speak("Our team will review your profile. Have a wonderful day!")

    elif step == 'finished':
        bot_speak("The interview is complete. You can close this window.")

def start_screening(stack_input):
    screener = st.session_state.screener
    st.session_state.candidate_data['tech_stack'] = stack_input
    
    # Feature: Personalization Message
    exp_years = st.session_state.candidate_data.get('experience', '1')
    bot_speak(screener.get_experience_level_message(exp_years))
    
    bot_speak("I'm generating some technical questions for you... please wait a moment.")
    
    questions = screener.generate_questions(stack_input, exp_years)
    
    # Feature: Limit Questions
    questions = questions[:6]
    
    st.session_state.questions = questions
    st.session_state.step = 'screening'
    
    if questions:
        bot_speak(f"Okay, I have {len(questions)} questions for you. Let's start.")
        bot_speak(f"1. {questions[0]}")
    else:
        bot_speak("I couldn't generate specific questions, but let's proceed. Tell me about your most challenging project.")
        st.session_state.questions = ["Tell me about your most challenging project."]

# --- UI Layout ---

st.title("TalentScout 🤖")
st.markdown("### AI Recruitment Assistant")

# Sidebar for Status
with st.sidebar:
    st.header("Screening Progress")
    if st.session_state.step == 'greeting':
        st.info("👋 Introduction")
    elif st.session_state.step == 'collect_info':
        progress = st.session_state.info_field_index / len(INFO_FIELDS)
        st.progress(progress)
        st.write(f"Collecting Details ({st.session_state.info_field_index}/{len(INFO_FIELDS)})")
    elif st.session_state.step == 'tech_stack':
        st.warning("🛠 Tech Stack Analysis")
    elif st.session_state.step == 'screening':
        q_prog = st.session_state.current_question_index / max(1, len(st.session_state.questions))
        st.progress(q_prog)
        st.write("📝 Technical Interview")
    elif st.session_state.step == 'finished':
        st.success("✅ Completed")

    if st.session_state.candidate_data:
        st.divider()
        st.caption("Candidate Summary")
        if 'full_name' in st.session_state.candidate_data:
            st.write(f"**Name:** {st.session_state.candidate_data['full_name']}")
        if 'desired_role' in st.session_state.candidate_data:
            st.write(f"**Role:** {st.session_state.candidate_data['desired_role']}")

# Initial Greeting
if not st.session_state.history:
    bot_speak("Hello! I’m TalentScout, an AI hiring assistant. I’ll be collecting some basic details and asking a few technical questions to understand your skill set. Your information is used only for screening purposes.")

# Display Chat History
chat_container = st.container()
with chat_container:
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Input Area
if st.session_state.step != 'finished':
    st.text_input(
        "Your response:",
        key="user_input",
        on_change=process_input
    )

# Auto-scroll to bottom
import streamlit.components.v1 as components
import time
# Use a changing key to force re-render
js = f"""
<script>
    function scroll() {{
        var body = window.parent.document.querySelector(".main");
        if (body) {{
            body.scrollTop = body.scrollHeight;
        }}
    }}
    // Run multiple times to handle dynamic loading
    scroll();
    setTimeout(scroll, 100);
    setTimeout(scroll, 500);
</script>
"""
components.html(js, height=0, width=0)
