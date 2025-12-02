import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import logging
from typing import Dict, List
from config import settings

class KnowledgeBaseCollector:
    """Collects data from various sources for the knowledge base"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = Path("src/knowledge_base/sample_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_study_abroad_programs(self):
        """Collect study abroad program data"""
        programs = [
            {
                "id": "usa-001",
                "country": "USA",
                "university": "Harvard University",
                "program": "Computer Science",
                "duration": "4 years",
                "tuition_fee": "$54,000/year",
                "requirements": ["SAT: 1500+", "GPA: 3.8+", "TOEFL: 100+"],
                "deadline": "January 1",
                "scholarship_available": True
            },
            {
                "id": "uk-001",
                "country": "UK",
                "university": "University of Oxford",
                "program": "Engineering",
                "duration": "3 years",
                "tuition_fee": "£28,000/year",
                "requirements": ["A-levels: A*AA", "IELTS: 7.0+"],
                "deadline": "October 15",
                "scholarship_available": True
            },
            {
                "id": "canada-001",
                "country": "Canada",
                "university": "University of Toronto",
                "program": "Business Administration",
                "duration": "4 years",
                "tuition_fee": "CAD 45,000/year",
                "requirements": ["High School Diploma", "IELTS: 6.5+"],
                "deadline": "January 13",
                "scholarship_available": True
            }
        ]
        
        self._save_data("study_abroad_programs.json", programs)
        return programs
    
    def collect_visa_requirements(self):
        """Collect visa requirements for different countries"""
        visa_data = {
            "USA": {
                "visa_type": "F-1 Student Visa",
                "requirements": [
                    "Valid passport",
                    "Form I-20",
                    "SEVIS fee receipt",
                    "Financial proof",
                    "Academic transcripts",
                    "English proficiency test scores"
                ],
                "processing_time": "3-5 weeks",
                "fee": "$510",
                "interview_required": True
            },
            "UK": {
                "visa_type": "Tier 4 Student Visa",
                "requirements": [
                    "CAS from university",
                    "Financial proof (£1,334/month for London)",
                    "TB test certificate",
                    "Academic qualifications",
                    "English proficiency (IELTS/TOEFL)"
                ],
                "processing_time": "3 weeks",
                "fee": "£363",
                "interview_required": "Sometimes"
            },
            "Canada": {
                "visa_type": "Study Permit",
                "requirements": [
                    "Letter of acceptance",
                    "Proof of financial support",
                    "Passport photos",
                    "Medical exam",
                    "Police certificate"
                ],
                "processing_time": "8 weeks",
                "fee": "CAD 150",
                "interview_required": False
            },
            "Australia": {
                "visa_type": "Student Visa (subclass 500)",
                "requirements": [
                    "CoE from institution",
                    "Genuine Temporary Entrant requirement",
                    "Health insurance (OSHC)",
                    "English proficiency",
                    "Financial capacity proof"
                ],
                "processing_time": "4-6 weeks",
                "fee": "AUD 630",
                "interview_required": "Rarely"
            }
        }
        
        self._save_data("visa_requirements.json", visa_data)
        return visa_data
    
    def collect_tuition_programs(self):
        """Collect tuition program information"""
        tuition_programs = [
            {
                "program": "IGCSE",
                "subjects": ["Mathematics", "Physics", "Chemistry", "Biology", "English"],
                "duration": "2 years",
                "fee_structure": {
                    "per_subject": "KES 15,000/term",
                    "full_program": "KES 120,000/year"
                },
                "features": [
                    "Expert tutors",
                    "Regular assessments",
                    "Mock exams",
                    "University guidance"
                ]
            },
            {
                "program": "A-Levels",
                "subjects": ["Mathematics", "Further Mathematics", "Physics", "Chemistry", "Biology"],
                "duration": "2 years",
                "fee_structure": {
                    "per_subject": "KES 18,000/term",
                    "full_program": "KES 150,000/year"
                },
                "features": [
                    "Cambridge curriculum",
                    "University preparation",
                    "Career counseling",
                    "Research projects"
                ]
            },
            {
                "program": "SAT Preparation",
                "subjects": ["Math", "Evidence-Based Reading and Writing"],
                "duration": "3 months",
                "fee_structure": {
                    "intensive": "KES 50,000",
                    "regular": "KES 35,000"
                },
                "features": [
                    "Full-length practice tests",
                    "Score improvement guarantee",
                    "Personalized study plan",
                    "College application guidance"
                ]
            }
        ]
        
        self._save_data("tuition_programs.json", tuition_programs)
        return tuition_programs
    
    def collect_application_guides(self):
        """Collect step-by-step application guides"""
        guides = {
            "USA_Application_Guide": {
                "steps": [
                    "Research universities and programs",
                    "Take required tests (SAT/ACT, TOEFL/IELTS)",
                    "Prepare application documents",
                    "Write personal statement/essays",
                    "Get recommendation letters",
                    "Complete online application",
                    "Submit financial documents",
                    "Apply for student visa"
                ],
                "timeline": "Start 12-18 months before intake",
                "important_dates": {
                    "Early Decision": "November 1",
                    "Regular Decision": "January 1-15",
                    "Financial Aid": "Varies by university"
                }
            },
            "UK_Application_Guide": {
                "steps": [
                    "Register on UCAS",
                    "Choose up to 5 courses",
                    "Write personal statement",
                    "Get reference letter",
                    "Submit application",
                    "Track application",
                    "Receive offers",
                    "Firm/insurance choices",
                    "Apply for visa"
                ],
                "timeline": "Start by June for September intake",
                "important_dates": {
                    "Oxford/Cambridge": "October 15",
                    "Most courses": "January 25",
                    "Art & Design": "March 24"
                }
            }
        }
        
        self._save_data("application_guides.json", guides)
        return guides
    
    def collect_all_data(self):
        """Collect all data for knowledge base"""
        self.logger.info("Starting data collection...")
        
        data_sources = [
            self.collect_study_abroad_programs,
            self.collect_visa_requirements,
            self.collect_tuition_programs,
            self.collect_application_guides
        ]
        
        for collector in data_sources:
            try:
                collector()
                self.logger.info(f"Successfully collected: {collector.__name__}")
            except Exception as e:
                self.logger.error(f"Error collecting {collector.__name__}: {str(e)}")
        
        self.logger.info("Data collection completed!")
    
    def _save_data(self, filename: str, data: Dict):
        """Save data to JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
