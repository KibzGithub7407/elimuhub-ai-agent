import json
import logging
from pathlib import Path
from typing import Tuple, List, Dict
from src.ai_engine.nlp_processor import NLPProcessor
from config import prompts, settings

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generates responses using simple rule-based + NLP + knowledge base lookup."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nlp = NLPProcessor()
        # Ensure models are available (may trigger training if not present)
        try:
            self.nlp._load_models()
        except Exception:
            logger.debug("Intent model not available on init.")
        # Load knowledge base aggregated file
        agg_file = Path("data/knowledge_base_aggregated.json")
        self.kb = {}
        if agg_file.exists():
            try:
                with open(agg_file, "r") as f:
                    self.kb = json.load(f)
            except Exception:
                logger.exception("Failed to load aggregated knowledge base")
        else:
            logger.info("Aggregated knowledge base not found; please run --init-kb")

    def generate_response(self, user_message: str, conversation_id: str = None) -> Tuple[str, str, float]:
        """Produce a response, returning (text, intent, confidence)."""
        try:
            intent, confidence = self.nlp.classify_intent(user_message)
        except Exception:
            intent, confidence = "general_question", 0.0

        entities = self.nlp.extract_entities(user_message)

        # Simple routing based on intent
        if intent in ("study_abroad_inquiry", "university_search"):
            response = self._handle_program_search(user_message, entities)
        elif intent == "visa_information":
            response = self._handle_visa_info(entities)
        elif intent == "tuition_program":
            response = self._handle_tuition_info(user_message)
        elif intent == "application_guide":
            response = self._handle_application_guide(entities)
        else:
            response = self._fallback_response(user_message)

        return response, intent, float(confidence)

    def search_knowledge_base(self, query: str, category: str = "") -> List[Dict]:
        """Simple search in aggregated JSON: exact-match + keyword filtering."""
        results = []
        query_lower = query.lower()
        if not self.kb:
            return results

        if category and category in self.kb:
            items = self.kb.get(category, [])
        else:
            # search across categories
            items = []
            for cat, data in self.kb.items():
                if isinstance(data, dict):
                    # dict entries (visa, guides)
                    for k, v in data.items():
                        items.append({"category": cat, "key": k, "value": v})
                elif isinstance(data, list):
                    for it in data:
                        items.append({"category": cat, "value": it})

        for item in items:
            text = ""
            if isinstance(item.get("value"), dict):
                text = json.dumps(item["value"]).lower()
            else:
                text = str(item.get("value")).lower()
            if query_lower in text:
                results.append(item)

        return results[:10]

    def _handle_program_search(self, message: str, entities: Dict) -> str:
        programs = self.kb.get("study_abroad_programs", [])
        if not programs:
            return "I don't have program data loaded. Please run the knowledge base initialization."

        # Filter by country/program/university if available
        candidates = []
        country = entities.get("country")
        program = entities.get("program")

        for p in programs:
            if country and country.lower() not in p.get("country","").lower() and country.lower() not in p.get("country","").lower():
                # no country match -> skip
                continue
            if program and program.lower() not in p.get("program","").lower():
                continue
            candidates.append(p)

        if not candidates:
            # fallback: show top 3
            candidates = programs[:3]

        # Build response
        lines = []
        for c in candidates[:3]:
            lines.append(f"{c.get('university')} — {c.get('program')} ({c.get('country')}) — Tuition: {c.get('tuition_fee')} — Deadline: {c.get('deadline')}")
        return "Here are some programs I found:\n" + "\n".join(lines)

    def _handle_visa_info(self, entities: Dict) -> str:
        visa = self.kb.get("visa_requirements", {})
        country = entities.get("country")
        if not visa:
            return "Visa information is not yet available. Please initialize the knowledge base."

        # Attempt to map common country keywords
        if country:
            ckey = country.capitalize()
            info = visa.get(ckey) or visa.get(country.upper()) or visa.get(country.lower())
            if info:
                reqs = "\n".join([f"- {r}" for r in info.get("requirements", [])])
                return f"Visa: {info.get('visa_type')}\nProcessing time: {info.get('processing_time')}\nFee: {info.get('fee')}\nRequirements:\n{reqs}"
        # fallback listing
        keys = list(visa.keys())[:5]
        return f"I have visa information for: {', '.join(keys)}. Please specify a country for detailed info."

    def _handle_tuition_info(self, message: str) -> str:
        tuition = self.kb.get("tuition_programs", [])
        if not tuition:
            return "Tuition program information is not yet available."

        hits = []
        for t in tuition:
            if any(tok in message.lower() for tok in (t.get("program","").lower(),)):
                hits.append(t)
        if not hits:
            hits = tuition[:2]
        lines = []
        for h in hits:
            lines.append(f"{h.get('program')} — duration: {h.get('duration')} — fees: {h.get('fee_structure')}")
        return "Tuition programs:\n" + "\n".join(lines)

    def _handle_application_guide(self, entities: Dict) -> str:
        guides = self.kb.get("application_guides", {})
        # choose by country
        country = entities.get("country")
        key = None
        if country == "USA":
            key = "USA_Application_Guide"
        elif country == "UK":
            key = "UK_Application_Guide"
        else:
            # pick generic if exists
            keys = list(guides.keys())
            key = keys[0] if keys else None

        if key and key in guides:
            g = guides[key]
            steps = "\n".join([f"{i+1}. {s}" for i, s in enumerate(g.get("steps", []))])
            return f"Application Guide ({key}):\n{steps}\nTimeline: {g.get('timeline')}"
        return "Application guides are available for USA and UK. Please specify which one you need."
    
    def _fallback_response(self, message: str) -> str:
        # Minimal fallback — later integrate LLM
        return "Sorry, I didn't fully understand that. Could you rephrase or provide more details?"
