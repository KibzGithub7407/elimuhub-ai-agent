# Elimuhub AI Agent

An intelligent AI agent for Elimuhub that improves service efficiency, enhances user engagement, and provides instant, accurate information about study abroad programs, visa requirements, tuition, and more.

## Features

- **Intelligent Search**: Context-aware answers based on user intent
- **Auto-organization**: Automatic categorization of knowledge base content
- **Multi-channel Support**: Website and WhatsApp integration
- **Natural Language Understanding**: Advanced NLP for query processing
- **Machine Learning Recommendations**: Personalized program suggestions
- **User Feedback System**: Continuous improvement through user interactions

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KibzGithub7407/elimuhub-ai-agent.git
cd elimuhub-ai-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the knowledge base:

```bash
python src/main.py --init-kb
```

5. Train AI models:

```bash
python src/main.py --train
```

6. Run the web application:

```bash
python src/main.py --web
```

7. Access the application at http://localhost:5000

### Running tests

```bash
pytest tests/
```

## Deployment

Recommended: Docker + docker-compose (see deployment/)

```bash
docker-compose up -d
```

Or run with gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 src.web.app:create_app()
```

## Contributing

Please add features via pull requests. Follow tests and linting rules. See CONTRIBUTING.md (optional) for more guidance.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
