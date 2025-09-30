from pydantic import BaseModel
from pydantic_ai import Agent
from typing import Optional

from schemas.services_schemas import FileReadInput, FileReadOutput, ParsedCV, ParsedJobDescription, SkillMatchingInput, SkillMatchingOutput, CandidateInsights, RedFlagReport








class FileManagerAgent:
    def __init__(self, service, model):
        """
        service: instance of FileManagerService
        model: pydantic_ai compatible LLM or model object
        """
        self.service = service
        # bind the service method as a tool
        self.agent = Agent(
            name="FileManagerAgent",
            result_type=FileReadOutput,
            description="Reads a file and returns its path and content",
            tools=[self._read_file_tool],
            system_prompt=(
                "You are a File Manager Agent. "
                "When given a FileReadInput, call the read_file tool to load the file content."
            ),
            model=model
        )

    def _read_file_tool(self, file_path: str) -> FileReadOutput:
        """Internal wrapper to call service and package output"""
        content = self.service.read_file(file_path)
        return FileReadOutput(file_path=file_path, file_content=content)

    def run(self, input_data: FileReadInput) -> FileReadOutput:
        # pass JSON string to run_sync
        output = self.agent.run_sync(input_data.json()).output
        return output


class CVParserAgent:
    def __init__(self, model):
        self.agent = Agent(
            name="CVParserAgent",
            description="Parses the raw CV text and extracts structured fields such as name, email, skills, education, and experience.",
            result_type=ParsedCV,
            tools=[],  # No custom tools — all handled by the LLM
            system_prompt=(
                "You are a CV parsing expert. When given a CV as plain text, "
                "extract the candidate's name, email, phone, skills (as a list), "
                "education (as a list), and work experience (as a list). "
                "If available, also extract certifications and a brief professional summary. "
                "Return the result as a structured response."
            ),
            model=model
        )

    def run(self, input_data: FileReadOutput) -> ParsedCV:
        return  self.agent.run_sync(input_data.json()).output
        






class JobDescriptionAgent:
    def __init__(self, model):
        self.agent = Agent(
            name="JobDescriptionAgent",
            description="Parses raw job description text and extracts structured job attributes such as title, skills, and responsibilities.",
            result_type=ParsedJobDescription,
            tools=[],  # LLM handles all logic
            system_prompt=(
                "You are a job description interpretation expert. "
                "Given a plain text job description, extract the following:\n"
                "- Job title\n"
                "- Company name (if present)\n"
                "- Location (if mentioned)\n"
                "- Summary or short description\n"
                "- Required skills (as a list)\n"
                "- Responsibilities (as a list)\n"
                "- Qualifications (degrees, certifications, etc.)\n"
                "- Employment type (Full-Time, Contract, etc.)\n"
                "- Seniority level (Entry, Mid, Senior)\n"
                "- Industry (if deducible)\n"
                "Return the result in a structured format."
            ),
            model=model
        )

    def run(self, input_data: FileReadOutput) -> ParsedJobDescription:
        return self.agent.run_sync(input_data.json()).output
        




class SkillMatchingAgent:
    def __init__(self, model):
        self.agent = Agent(
            name="SkillMatchingAgent",
            description="Matches a candidate CV to a job description using multi-factor scoring (skills, experience, education, etc.)",
            result_type=SkillMatchingOutput,
            tools=[],
            system_prompt=(
                "You are a smart hiring assistant. When given structured CV and job description data, evaluate the candidate based on:\n\n"
                "1. Skill match (do they know the required tools?)\n"
                "2. Experience match (have they held relevant jobs?)\n"
                "3. Education (do they meet degree requirements?)\n"
                "4. Certifications/qualifications\n"
                "5. Job responsibilities alignment\n\n"
                "Calculate sub-scores (0-100) for each dimension, then compute a weighted total_score.\n"
                "Return matched/missing elements, and a short summary justifying the score."
            ),
            model=model
        )


    def run(self, input_data: SkillMatchingInput) -> SkillMatchingOutput:
        return self.agent.run_sync(input_data.json()).output



class InsightGeneratorAgent:
    def __init__(self, model):
        self.agent = Agent(
            name="InsightGeneratorAgent",
            description="Generates interpretive insights for a candidate from their skill matching output",
            result_type=CandidateInsights,
            tools=[],
            system_prompt=(
                "You are a hiring strategist. Given a skill matching result for a candidate:\n"
                "- Identify strengths (strong skills, excellent education, or relevant experience)\n"
                "- Identify weaknesses or gaps (missing skills, mismatched responsibilities, or education gaps)\n"
                "- Describe the candidate's potential (growth, leadership, adaptability, etc.)\n"
                "- Summarize the overall impression of the candidate in 1-2 lines.\n\n"
                "Be analytical but concise. Avoid vague statements."
            ),
            model=model
        )

    def run(self, input_data: SkillMatchingOutput) -> CandidateInsights:
        return self.agent.run_sync(input_data.json()).output



# ----------------------------
# 3. RedFlagDetectorAgent
# ----------------------------
class RedFlagDetectorAgent:
    def __init__(self, model):
        self.agent = Agent(
            name="RedFlagDetectorAgent",
            description="Detects red flags in a candidate's profile based on skill matching results.",
            result_type=RedFlagReport,
            tools=[],
            system_prompt=(
                "You are a red flag detection expert in HR screening.\n"
                "Given a skill matching report, identify any major issues that may disqualify or concern a recruiter.\n"
                "Common red flags include:\n"
                "- Missing critical skills\n"
                "- Major responsibility mismatches\n"
                "- No relevant experience\n"
                "- Poor education alignment\n"
                "- Missing key certifications\n"
                "- Low total score (e.g. < 60)\n\n"
                "Return a list of red_flags, classify severity (Low, Medium, High), and summarize the concern."
            ),
            model=model
        )

    def run(self, input_data: SkillMatchingOutput) -> RedFlagReport:
        return self.agent.run_sync(input_data.json()).output
        
