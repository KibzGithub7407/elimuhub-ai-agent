import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application
    APP_NAME = "Elimuhub AI Agent"
    VERSION = "1.0.0"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "data")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/knowledge_base.db")
    
    # AI/ML Settings
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD = 0.7
    
    # WhatsApp
    WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "False").lower() == "true"
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    
    # Web
    SECRET_KEY = os.getenv("SECRET_KEY", "elimuhub-secret-key-2024")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Knowledge Base Categories
    CATEGORIES = [
        "study_abroad_programs",
        "visa_requirements",
        "tuition_programs",
        "application_guides",
        "partner_universities",
        "scholarships",
        "faqs"
    ]
    
    # Escalation Settings
    ESCALATION_THRESHOLD = 3  # Number of unsuccessful attempts before escalation
    SUPPORT_EMAIL = "support@elimuhub.com"
    SUPPORT_PHONE = "+254700000000"

config = Config()
