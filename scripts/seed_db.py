#!/usr/bin/env python3
"""
Seed the sqlite knowledge_base.db from sample JSON files.

Usage:
    python scripts/seed_db.py
This will create/overwrite data/knowledge_base.db using the JSON files in src/knowledge_base/sample_data
"""

import json
import sqlite3
from pathlib import Path
import logging
from src.utils.logger import setup_logger

def load_json(file_path: Path):
    try:
        return json.loads(file_path.read_text())
    except Exception as e:
        logging.error("Failed to load %s: %s", file_path, e)
        return None

def seed_db():
    setup_logger()
    logger = logging.getLogger("seed_db")

    sample_dir = Path("src/knowledge_base/sample_data")
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = out_dir / "knowledge_base.db"

    # Remove existing DB if present (overwrite)
    if db_path.exists():
        logger.info("Overwriting existing DB at %s", db_path)
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
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

    # Load programs
    prog_file = sample_dir / "study_abroad_programs.json"
    programs = load_json(prog_file) or []
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
        except Exception as e:
            logger.exception("Failed to insert program %s: %s", p.get("id"), e)

    # Create a simple visas table
    c.execute("""
    CREATE TABLE IF NOT EXISTS visas (
        country TEXT PRIMARY KEY,
        visa_type TEXT,
        requirements TEXT,
        processing_time TEXT,
        fee TEXT,
        interview_required TEXT
    )
    """)
    visa_file = sample_dir / "visa_requirements.json"
    visas = load_json(visa_file) or {}
    for country, info in visas.items():
        try:
            c.execute("""
            INSERT OR REPLACE INTO visas (
                country, visa_type, requirements, processing_time, fee, interview_required
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                country,
                info.get("visa_type"),
                json.dumps(info.get("requirements", [])),
                info.get("processing_time"),
                info.get("fee"),
                str(info.get("interview_required"))
            ))
        except Exception as e:
            logger.exception("Failed to insert visa info for %s: %s", country, e)

    # Tuition programs table
    c.execute("""
    CREATE TABLE IF NOT EXISTS tuition_programs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program TEXT,
        details TEXT
    )
    """)
    tuition_file = sample_dir / "tuition_programs.json"
    tuitions = load_json(tuition_file) or []
    for t in tuitions:
        try:
            c.execute("""
            INSERT INTO tuition_programs (program, details) VALUES (?, ?)
            """, (
                t.get("program"),
                json.dumps(t)
            ))
        except Exception as e:
            logger.exception("Failed to insert tuition program %s: %s", t.get("program"), e)

    conn.commit()
    conn.close()
    logger.info("Seeded sqlite DB at %s", db_path)

if __name__ == "__main__":
    seed_db()
