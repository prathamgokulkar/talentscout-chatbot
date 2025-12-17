import os
import re
from typing import List, Dict, Optional
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class Screener:
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.client = None
        if self.api_token:
            self.client = InferenceClient(token=self.api_token)
        
        # Fallback questions if LLM fails or no token
        self.fallback_questions = {
            "default": [
                "Can you describe a challenging technical problem you solved recently?",
                "How do you handle version control and code collaboration?",
                "What is your preferred development environment and why?"
            ]
        }

    def validate_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        # Basic validation: numeric, 7-15 digits, allowing for + and spaces/dashes
        clean_phone = re.sub(r'[\s\-+]', '', phone)
        return clean_phone.isdigit() and 7 <= len(clean_phone) <= 15

    def validate_experience(self, exp: str) -> bool:
        try:
            val = float(exp)
            return 0 <= val <= 50
        except ValueError:
            return False

    def generate_questions(self, tech_stack: str, experience_years: str) -> List[str]:
        """
        Generates technical screening questions based on the declared tech stack.
        """
        if not self.client:
            return self.fallback_questions["default"]

        # Parse tech stack to identify major technologies
        technologies = [t.strip() for t in tech_stack.replace('and', ',').split(',') if t.strip()]
        technologies = technologies[:5]

        tech_list_str = ", ".join(technologies)
        
        system_prompt = "You are a technical recruiter. Your goal is to screen candidates effectively."
        user_prompt = f"""
        The candidate has {experience_years} years of experience.
        Their tech stack includes: {tech_list_str}.

        Task: Generate exactly 3 technical screening questions for EACH of the following technologies: {tech_list_str}.

        Rules:
        1. Questions should be specific to the technology.
        2. Test practical understanding.
        3. Return ONLY the questions as a single flat numbered list. 
        4. Do not include headers, intro, or outro text.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            
            response = self.client.chat_completion(
                messages=messages,
                model="meta-llama/Llama-3.1-8B-Instruct", 
                max_tokens=1000,
                temperature=0.1, # Nearly deterministic
                top_p=0.95,     # Restrict random tail
                seed=42         # Fixed seed for reproducibility
            )
            
            content = response.choices[0].message.content
            
            # Parse response
            raw_questions = []
            for line in content.split('\n'):
                line = line.strip()
                # Match "1. Question" or "- Question"
                if line and (line[0].isdigit() or line.startswith('-')):
                    cleaned = re.sub(r'^[\d\-\.\s]+', '', line)
                    if cleaned:
                        raw_questions.append(cleaned)
            
            if not raw_questions:
                 # Fallback attempt to parse non-bulleted lines
                 return [l for l in content.split('\n') if len(l) > 15][:5]

            return raw_questions

        except Exception as e:
            print(f"Error generating questions: {e}")
            return self.fallback_questions["default"]

    def _generate_fallback_questions(self, prompt):
        # Deprecated logic, keeping method stub just in case
        return self.fallback_questions["default"]

    def analyze_tech_stack(self, user_input: str) -> Dict[str, List[str]]:
        """
        Simple parsing of tech stack. 
        In a real app, this could also be LLM-powered to categorize them.
        """
        # For now, just splitting by commas
        items = [item.strip() for item in user_input.replace('and', ',').split(',')]
        return {"declared": items}

    def analyze_sentiment(self, text: str) -> str:
        """
        Returns 'positive', 'neutral', or 'negative/uncertain' based on polarity.
        """
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.3:
                return "confident"
            elif polarity < -0.1:
                return "uncertain"
            else:
                return "neutral"
        except ImportError:
            # Fallback if TextBlob is not installed
            return "neutral"

    def validate_answer(self, answer: str) -> bool:
        """
        Basic check if an answer is substantial enough.
        """
        # If it's too short (e.g. "yes", "no")
        if len(answer.strip().split()) < 2:
            return False
        return True

    def get_experience_level_message(self, years_str: str) -> str:
        try:
            years = float(years_str)
            if years <= 2:
                return f"Since you have {years_str} years of experience, I'll focus on core fundamentals."
            elif years <= 5:
                return f"With {years_str} years of experience, we'll dive into some practical scenarios."
            else:
                return f"Given your {years_str} years of experience, these questions will touch on advanced concepts and architecture."
        except:
            return "I've prepared some questions based on your background."

    def get_encouragement(self) -> str:
        import random
        return random.choice([
            "No worries, take your time.",
            "That's a complex topic, just give it your best shot.",
            "You're doing great, just a few more steps."
        ])
    
    def get_confidence_acknowledgement(self) -> str:
        import random
        return random.choice([
            "Great, concise answer.",
            "Excellent point.",
            "Good.",
            "Noted."
        ])
