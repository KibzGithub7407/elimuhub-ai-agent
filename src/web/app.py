from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import logging
from datetime import datetime
from src.ai_engine.response_generator import ResponseGenerator
from src.utils.escalation_manager import EscalationManager
from src.utils.feedback_handler import FeedbackHandler
from config import settings

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    CORS(app)
    
    # Initialize components
    response_generator = ResponseGenerator()
    escalation_manager = EscalationManager()
    feedback_handler = FeedbackHandler()
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/chat')
    def chat():
        """Chat interface"""
        session['conversation_id'] = datetime.now().strftime('%Y%m%d_%H%M%S')
        session['message_count'] = 0
        return render_template('chat.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat_api():
        """Chat API endpoint"""
        try:
            data = request.json
            user_message = data.get('message', '')
            conversation_id = session.get('conversation_id')
            
            # Generate response
            response, intent, confidence = response_generator.generate_response(
                user_message, conversation_id
            )
            
            # Check if escalation is needed
            session['message_count'] = session.get('message_count', 0) + 1
            if confidence < 0.5 and session['message_count'] >= settings.ESCALATION_THRESHOLD:
                escalation_info = escalation_manager.escalate(
                    user_message, conversation_id
                )
                response = f"{response}\n\n{escalation_info}"
            
            # Log interaction
            feedback_handler.log_interaction(
                conversation_id=conversation_id,
                user_message=user_message,
                ai_response=response,
                intent=intent,
                confidence=confidence
            )
            
            return jsonify({
                'success': True,
                'response': response,
                'intent': intent,
                'confidence': float(confidence)
            })
            
        except Exception as e:
            logging.error(f"Error in chat API: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
    
    @app.route('/api/feedback', methods=['POST'])
    def feedback_api():
        """Handle user feedback"""
        try:
            data = request.json
            conversation_id = data.get('conversation_id')
            rating = data.get('rating')
            comments = data.get('comments', '')
            
            feedback_handler.save_feedback(
                conversation_id=conversation_id,
                rating=rating,
                comments=comments
            )
            
            return jsonify({'success': True})
            
        except Exception as e:
            logging.error(f"Error in feedback API: {str(e)}")
            return jsonify({'success': False}), 500
    
    @app.route('/api/knowledge-base/search', methods=['GET'])
    def search_knowledge_base():
        """Search knowledge base"""
        query = request.args.get('q', '')
        category = request.args.get('category', '')
        
        results = response_generator.search_knowledge_base(query, category)
        return jsonify({'results': results})
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'elimuhub-ai-agent'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=settings.DEBUG)
