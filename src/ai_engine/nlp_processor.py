import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sentence_transformers import SentenceTransformer
import json
from typing import Dict, List, Tuple
import logging
import pickle
from pathlib import Path

class NLPProcessor:
    """Handles Natural Language Processing for the AI agent"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model_path = Path("models")
        self.model_path.mkdir(exist_ok=True)
        
        # Download NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        # Initialize models
        self.intent_classifier = None
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
        # Intent categories
        self.intent_categories = [
            "study_abroad_inquiry",
            "visa_information",
            "tuition_program",
            "application_guide",
            "scholarship_inquiry",
            "university_search",
            "general_question",
            "escalation_request"
        ]
    
    def train_models(self, training_data=None):
        """Train intent classification model"""
        self.logger.info("Training NLP models...")
        
        # Sample training data if not provided
        if training_data is None:
            training_data = self._create_sample_training_data()
        
        texts = [item['text'] for item in training_data]
        intents = [item['intent'] for item in training_data]
        
        # Create and train pipeline
        self.intent_classifier = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000)),
            ('clf', MultinomialNB())
        ])
        
        self.intent_classifier.fit(texts, intents)
        
        # Save model
        with open(self.model_path / 'intent_classifier.pkl', 'wb') as f:
            pickle.dump(self.intent_classifier, f)
        
        self.logger.info("NLP models trained and saved successfully!")
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent from text"""
        if self.intent_classifier is None:
            self._load_models()
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Predict intent
        intent = self.intent_classifier.predict([processed_text])[0]
        confidence = np.max(self.intent_classifier.predict_proba([processed_text]))
        
        return intent, confidence
    
    def extract_entities(self, text: str) -> Dict:
        """Extract key entities from text"""
        entities = {
            "country": None,
            "university": None,
            "program": None,
            "subject": None,
            "deadline": None
        }
        
        # Simple entity extraction (can be enhanced with NER)
        country_keywords = {
            "usa": ["usa", "united states", "america"],
            "uk": ["uk", "united kingdom", "britain"],
            "canada": ["canada"],
            "australia": ["australia"]
        }
        
        for country, keywords in country_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                entities["country"] = country.upper()
                break
        
        # Extract program mentions
        program_keywords = ["computer science", "engineering", "business", "medicine", "law"]
        for program in program_keywords:
            if program in text.lower():
                entities["program"] = program
                break
        
        return entities
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate semantic embedding for text"""
        return self.embedding_model.encode(text)
    
    def find_similar_questions(self, query: str, knowledge_base: List[Dict], top_k: int = 3) -> List[Dict]:
        """Find similar questions in knowledge base"""
        query_embedding = self.generate_embedding(query)
        similarities = []
        
        for item in knowledge_base:
            if 'question' in item:
                item_embedding = self.generate_embedding(item['question'])
                similarity = np.dot(query_embedding, item_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(item_embedding)
                )
                similarities.append((similarity, item))
        
        # Sort by similarity and return top k
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in similarities[:top_k]]
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for NLP tasks"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation (basic)
        import string
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text
    
    def _create_sample_training_data(self) -> List[Dict]:
        """Create sample training data for intent classification"""
        training_data = []
        
        # Study abroad inquiries
        training_data.extend([
            {"text": "I want to study in USA", "intent": "study_abroad_inquiry"},
            {"text": "Best universities in UK for engineering", "intent": "university_search"},
            {"text": "How to apply for masters in Canada", "intent": "application_guide"},
        ])
        
        # Visa information
        training_data.extend([
            {"text": "What are the visa requirements for USA?", "intent": "visa_information"},
            {"text": "Student visa processing time UK", "intent": "visa_information"},
            {"text": "Documents needed for Canada student visa", "intent": "visa_information"},
        ])
        
        # Tuition programs
        training_data.extend([
            {"text": "IGCSE tuition fees", "intent": "tuition_program"},
            {"text": "A-Levels coaching", "intent": "tuition_program"},
            {"text": "SAT preparation courses", "intent": "tuition_program"},
        ])
        
        return training_data
    
    def _load_models(self):
        """Load trained models from disk"""
        model_file = self.model_path / 'intent_classifier.pkl'
        if model_file.exists():
            with open(model_file, 'rb') as f:
                self.intent_classifier = pickle.load(f)
        else:
            self.train_models()
