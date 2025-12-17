def get_custom_css():
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* Global Variables */
        :root {
            --primary-color: #2563EB;
            --secondary-color: #1E40AF;
            --background-start: #0F172A;
            --background-end: #1E293B;
            --text-color: #F8FAFC;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        /* Base Styles */
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background-start); /* Fallback */
            color: var(--text-color);
        }

        /* Target the main app container to override default white theme */
        .stApp {
            background: linear-gradient(135deg, var(--background-start), var(--background-end));
            background-attachment: fixed;
        }

        /* Ensure headers are white */
        h1, h2, h3, h4, h5, h6, span, div, p {
            color: var(--text-color) !important;
        }
        
        /* Fix specific text inputs that might be inheriting dark text */
        .stTextInput label, .stMarkdown, .stText {
            color: var(--text-color) !important;
        }

        /* Chat Message Styling */
        .stChatMessage {
            background-color: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .stChatMessage[data-testid="stChatMessageUser"] {
            background-color: rgba(37, 99, 235, 0.2);
            border-color: rgba(37, 99, 235, 0.3);
        }

        /* Inputs */
        .stTextInput > div > div > input {
            background-color: var(--glass-bg);
            color: var(--text-color);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.5);
        }

        /* Buttons */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background-color: var(--secondary-color);
            transform: translateY(-1px);
        }

        /* Headers */
        h1, h2, h3 {
            color: white;
            font-weight: 700;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.95);
            border-right: 1px solid var(--glass-border);
        }
    </style>
    """
