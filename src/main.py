import argparse
import logging
from src.knowledge_base.collector import KnowledgeBaseCollector
from src.knowledge_base.processor import KnowledgeBaseProcessor
from src.ai_engine.nlp_processor import NLPProcessor
from src.web.app import create_app
from src.utils.logger import setup_logger

def initialize_knowledge_base():
    """Initialize and populate the knowledge base"""
    print("Initializing Elimuhub Knowledge Base...")
    
    # Collect data
    collector = KnowledgeBaseCollector()
    collector.collect_all_data()
    
    # Process and structure data
    processor = KnowledgeBaseProcessor()
    processor.process_and_store()
    
    print("Knowledge base initialized successfully!")

def train_ai_models():
    """Train AI models for intent classification and recommendations"""
    print("Training AI models...")
    
    nlp = NLPProcessor()
    nlp.train_models()
    
    print("AI models trained successfully!")

def main():
    parser = argparse.ArgumentParser(description="Elimuhub AI Agent")
    parser.add_argument('--init-kb', action='store_true', help='Initialize knowledge base')
    parser.add_argument('--train', action='store_true', help='Train AI models')
    parser.add_argument('--web', action='store_true', help='Start web server')
    parser.add_argument('--whatsapp', action='store_true', help='Start WhatsApp bot')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logger()
    
    if args.init_kb:
        initialize_knowledge_base()
    
    if args.train:
        train_ai_models()
    
    if args.web:
        app = create_app()
        app.run(host='0.0.0.0', port=5000, debug=True)
    
    if args.whatsapp:
        from src.whatsapp.whatsapp_bot import WhatsAppBot
        bot = WhatsAppBot()
        bot.run()

if __name__ == "__main__":
    main()
