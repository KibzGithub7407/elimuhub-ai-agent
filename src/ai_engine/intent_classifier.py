# Lightweight wrapper for loading/saving intent classifier (optional)
import logging
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

class IntentClassifier:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.model = None

    def save(self, pipeline):
        path = self.model_dir / "intent_classifier.pkl"
        with open(path, "wb") as f:
            pickle.dump(pipeline, f)
        logger.info("Intent classifier saved to %s", path)

    def load(self):
        path = self.model_dir / "intent_classifier.pkl"
        if path.exists():
            with open(path, "rb") as f:
                self.model = pickle.load(f)
            logger.info("Intent classifier loaded from %s", path)
        return self.model
