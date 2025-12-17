# TalentScout Hiring Assistant 🤖

## Project Overview
TalentScout is an AI-powered recruitment screening assistant designed to automate the initial technical interview process. It engages candidates in a structured conversation, identifies their technical strengths, and generates tailored screening questions using an LLM. The goal is to save recruiter time while providing a fair, consistent, and engaging experience for candidates.

## Features
*   **Structured Information Collection**: Validates candidate details (Email, Phone, Experience).
*   **Dynamic Tech Stack Analysis**: Identifies programming languages and tools, asking follow-up questions if the input is vague.
*   **AI-Generated Screening Questions**: Uses **meta-llama/Llama-3.1-8B-Instruct** to generate specific technical questions based on the candidate's exact stack and experience level.
*   **Adaptive Conversations**:
    *   **Sentiment Awareness**: Detects candidate confidence/uncertainty and responds with encouragement.
    *   **Contextual Personalization**: Tailors language based on years of experience (e.g., focusing on "fundamentals" vs "architecture").
    *   **Fallback Handling**: Detects incomplete answers and asks for elaboration.
*   **Premium UI**: A sleek, dark-mode interface built with Streamlit and custom CSS.

## Tech Stack
*   **Frontend**: Streamlit (Python)
*   **AI/LLM**: Hugging Face Inference API
*   **Model**: `meta-llama/Llama-3.1-8B-Instruct`
*   **Logic**: Python (RegEx validation, TextBlob for sentiment)
*   **Styling**: Custom CSS (Glassmorphism, Inter font)

## Architecture
1.  **User Interface**: Streamlit manages the chat session and state.
2.  **Screener Logic**: A helper class handles:
    *   Input validation (RegEx)
    *   State transitions (Greeting -> Info -> Stack -> Questions)
    *   Sentiment analysis (TextBlob)
3.  **LLM Service**: Connects to Hugging Face via API.
    *   **Input**: Tech stack + Experience + Prompt
    *   **Output**: Structured list of 3-5 technical questions.

## LLM Selection Justification
We selected **Mistral-7B-Instruct-v0.3** for this implementation because:
1.  **Instruction Following**: It excels at following strict formatting rules (e.g., "Return ONLY a numbered list"), which is critical for parsing questions.
2.  **Determinism**: By setting `temperature=0.1` and `seed=42`, this model produces consistent, reproducible questions, ensuring fairness across candidates.
3.  **Efficiency**: It provides a perfect balance of reasoning capability and latency for a real-time chat application.
4.  **Open Source**: Allows for transparency and potential future self-hosting.

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
