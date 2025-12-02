import json
from pathlib import Path
import logging
import sqlite3
from typing import Dict, Any
from config import settings

class KnowledgeBaseProcessor:
    """Processes raw knowledge base JSON files and stores them in a simple sqlite DB and aggregated JSON."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_dir = Path("src/knowledge_base/sample_data")
        self.output_dir = Path("data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.output_dir / "knowledge_base.db"

    def process_and_store(self):
        """Aggregate sample JSON files and create a simple sqlite storage."""
        self.logger.info("Processing knowledge base files...")
        aggregated = {}

        for file in self.sample_dir.glob("*.json"):
            try:
                with open(file, "r") as f:
                    aggregated[file.stem] = json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load {file}: {e}")

        # Save aggregated JSON for quick loading
        agg_file = self.output_dir / "knowledge_base_aggregated.json"
        with open(agg_file, "w") as f:
            json.dump(aggregated, f, indent=2)

        # Create a very small sqlite DB with simple tables for demonstration
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            # Create tables
            c.execute("""
                CREATE TABLE IF NOT EXISTS programs (
                    id TEXT PRIMARY KEY,
                    country TEXT,
                    university TEXT,
                    program TEXT,
                    duration TEXT,
                    tuition_fee TEXT,
                    requirements TEXT,
                    deadline TEXT,
                    scholarship_available INTEGER
                )
            """)
            # Insert programs if any
            programs = aggregated.get("study_abroad_programs", [])
            for p in programs:
                try:
                    c.execute("""
                        INSERT OR REPLACE INTO programs (
                            id, country, university, program, duration, tuition_fee, requirements, deadline, scholarship_available
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        p.get("id"),
                        p.get("country"),
                        p.get("university"),
                        p.get("program"),
                        p.get("duration"),
                        p.get("tuition_fee"),
                        json.dumps(p.get("requirements", [])),
                        p.get("deadline"),
                        int(bool(p.get("scholarship_available")))
                    ))
                except Exception:
                    self.logger.exception("Failed to insert program %s", p.get("id"))
            conn.commit()
            conn.close()
        except Exception:
            self.logger.exception("Failed to create or populate sqlite DB")

        self.logger.info("Knowledge base processing completed.")
