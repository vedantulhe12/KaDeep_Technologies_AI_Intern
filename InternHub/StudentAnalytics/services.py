import json
from google import genai
from .models import StudentProfile, Internship, MatchResult
from django.conf import settings
import re
import PyPDF2
import docx
import os
from django.core.files.storage import default_storage

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class GeminiClient:
    @staticmethod
    def generate(prompt: str) -> str:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text

class InternHubAIService:
    SYSTEM_PROMPT = """

        You are an AI assistant for an internship platform called InternHub.

        You will receive:
        - A student profile (skills, interests, projects, resume)
        - An internship job description

        Your task is to:
        1. Analyze how well the student matches the internship
        2. Explain missing or weak skills
        3. Recommend if the student should apply
        4. Rewrite the student's resume so it fits the internship
        5. Give a confidence / ATS score between 0 and 1

        IMPORTANT:
        Return ONLY valid JSON in this format:

        {
        "match_summary": "Short paragraph explaining fit",
        "skill_gaps": ["skill1", "skill2"],
        "recommendation_text": "Short recommendation for the student",
        "generated_resume": "New resume text customized for this job",
        "ats_score": 0.0
        }
        """


    def run_llm(self, student_data, jd_data):
        user_prompt = f"""
            STUDENT PROFILE:
            {json.dumps(student_data, indent=2)}

            INTERNSHIP:
            {json.dumps(jd_data, indent=2)}
            """
        prompt = self.SYSTEM_PROMPT + user_prompt
        print("LLM Prompt:", prompt)
        response = GeminiClient.generate(prompt)
        print("LLM Response:", response)
        raw = re.sub(r"^```json\s*", "", response)
        raw = re.sub(r"\s*```$", "", raw)

        print("LLM Cleaned Response:", raw)

        return json.loads(raw)
    def extract_resume_text(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return self.read_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self.read_docx(file_path)
        else:
            return ""
    
    def read_pdf(self, path):
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
        
    def read_docx(self, path):
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    def build_student(self, student: StudentProfile):
        resume_content = ""

        # Case 1: User pasted resume
        if student.resume_text:
            resume_content = student.resume_text

        # Case 2: User uploaded a file
        elif student.resume_file:
            resume_content = self.extract_resume_text(student.resume_file.path)

        return {
            "name": student.name,
            "skills": student.skills,
            "interests": student.interests,
            "projects": student.projects,
            "experience": student.experience_summary,
            "resume": resume_content,
        }

    def build_jd(self, internship: Internship):
        return {
            "company": internship.company,
            "role": internship.role,
            "description": internship.description,
            "required_skills": internship.required_skills,
        }

    def get_next_version(self, student, internship):
        last = MatchResult.objects.filter(
            student=student,
            internship=internship
        ).order_by("-version").first()

        return 1 if not last else last.version + 1

    def analyze(self, student, internship):
        student_data = self.build_student(student)
        jd_data = self.build_jd(internship)

        ai_output = self.run_llm(student_data, jd_data)

        version = self.get_next_version(student, internship)

        return MatchResult.objects.create(
            student=student,
            internship=internship,
            version=version,
            match_summary=ai_output["match_summary"],
            skill_gaps=ai_output["skill_gaps"],
            recommendation_text=ai_output["recommendation_text"],
            generated_resume=ai_output["generated_resume"],
            ats_score=ai_output["ats_score"],
        )