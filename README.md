# TalentScout Hiring Assistant 🤖

## Project Overview
TalentScout is an AI-powered recruitment screening assistant designed to automate the initial technical interview process. It engages candidates in a structured conversation, identifies their technical strengths, and generates tailored screening questions using an LLM. The goal is to save recruiter time while providing a fair, consistent, and engaging experience for candidates.

## LLM Selection Justification
We selected **meta-llama/Llama-3.1-8B-Instruct** for this implementation because:
1.  **Instruction Following**: As a state-of-the-art open-source model, it excels at following complex multi-step instructions (e.g., "Screen for these 3 techs, generate 3 questions each").
2.  **Reasoning Capabilities**: Llama 3.1 demonstrates superior reasoning for technical topics compared to smaller models, ensuring high-quality, relevant questions.
3.  **Conversational Fluency**: It handles the nuances of recruitment dialogue naturally, providing a smoother candidate experience.
4.  **Open Standard**: Widely supported and easier to fine-tune or swap if needed.

## Features
*   **Structured Information Collection**: Validates candidate details (Email, Phone, Experience).
*   **Dynamic Tech Stack Analysis**:
    *   **Intelligent Expansion**: Automatically prompts for frameworks or databases if the initial input is too vague (e.g., just "Python").
    *   **Per-Technology Breakdowns**: Generates questions for each specific technology listed.
*   **AI-Generated Screening Questions**: Uses **Llama-3.1-8B** to generate tailored questions, capped at 6 questions to respect candidate time.
*   **Adaptive Conversations**:
    *   **Sentiment Awareness**: Detects confidence levels and provides encouraging feedback.
    *   **Contextual Personalization**: Explicitly adjusts question difficulty based on years of experience.
    *   **Robust Fallback**: Detects one-word or insufficient answers and politely asks the candidate to elaborate.
*   **Premium UI**: A sleek, dark-mode interface built with Streamlit and custom CSS, featuring auto-scrolling chat.

## Prompt Design Strategy
*   **Role-Playing**: The system prompt defines the AI as a "Technical Recruiter" to set the correct tone and domain.
*   **Per-Technology Iteration**: The prompt explicitly asks for "3 questions for EACH technology" to prevent generic questions like "Tell me about code."
*   **Negative Constraints**: We explicitly instruct the model *what NOT to do* (e.g., "Do not include intro text", "Do not ask trivia") to ensure the output is clean and usable by the app.
*   **Structured Output**: The prompt forces a flat numbered list format, which allows the regex parser to reliably separate individual questions.

## Data Privacy & Security
*   **Session-Based Storage**: Candidate data is held only in `st.session_state` (RAM) during the interview.
*   **No Persistence**: Data is **not** saved to a database or file after the session ends.
*   **Stateless AI**: We use the stateless Hugging Face API; no candidate data is used to train the model.
*   **Environment Variables**: API tokens are stored securely in `.env` and excluded from version control via `.gitignore`.

## Setup & Run Instructions

### Prerequisites
*   Python 3.8+
*   Hugging Face API Token

### Installation
1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd talentscout
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    HUGGINGFACE_API_TOKEN=your_hf_token_here
    ```

### Running the App
```bash
streamlit run app.py
```
