from pydantic import BaseModel
from typing import Optional, List
from pydantic_ai import Agent


class FileReadInput(BaseModel):
    file_path: str

class FileReadOutput(BaseModel):
    file_path: str
    file_content: str




class FileReadOutput(BaseModel):
    file_path: str
    file_content: str


class ParsedCV(BaseModel):
    name: Optional[str]
    role: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]
    certifications: Optional[List[str]] = []
    summary: Optional[str] = None



class ParsedJobDescription(BaseModel):
    job_title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    job_summary: Optional[str]
    required_skills: List[str]
    responsibilities: List[str]
    qualifications: Optional[List[str]]
    employment_type: Optional[str]  # e.g. Full-Time, Part-Time, Contract
    seniority_level: Optional[str]  # e.g. Entry, Mid, Senior
    industry: Optional[str] = None



from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_ai import Agent

# ----------------------------
# 1. Models from previous agents
# ----------------------------

class ParsedCV(BaseModel):
    name: Optional[str]
    email: Optional[str]
    role:  Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]
    certifications: Optional[List[str]] = []
    summary: Optional[str] = None

class ParsedJobDescription(BaseModel):
    job_title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    job_summary: Optional[str]
    required_skills: List[str]
    responsibilities: List[str]
    qualifications: Optional[List[str]]
    employment_type: Optional[str]
    seniority_level: Optional[str]
    industry: Optional[str] = None



class SkillMatchingInput(BaseModel):
    candidate: ParsedCV
    job: ParsedJobDescription



class SkillMatchingOutput(BaseModel):
    skill_score: float = Field(..., ge=0, le=100)
    experience_score: float = Field(..., ge=0, le=100)
    education_score: float = Field(..., ge=0, le=100)
    qualification_score: float = Field(..., ge=0, le=100)
    responsibility_score: float = Field(..., ge=0, le=100)

    total_score: float = Field(..., ge=0, le=100, description="Weighted overall score")

    matched_skills: List[str]
    missing_skills: List[str]
    matched_responsibilities: List[str]
    missing_responsibilities: List[str]
    education_gaps: Optional[List[str]] = []
    missing_qualifications: Optional[List[str]] = []

    summary: Optional[str] = Field(None, description="Natural language explanation of the score and candidate fit")



class CandidateInsights(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    potential: Optional[str] = Field(..., description="Assessment of candidate's future growth or adaptability")
    insight_summary: Optional[str] = Field(None, description="A short narrative insight about the candidate")





class RedFlagReport(BaseModel):
    red_flags: List[str] = Field(..., description="List of potential concerns or dealbreakers")
    severity_level: str = Field(..., description="Overall severity: Low, Medium, High")
    flagged_summary: Optional[str] = Field(None, description="Natural language summary of the red flags")



class CVAnalysisResult(BaseModel):
    cv: ParsedCV
    job_description: ParsedJobDescription
    skill_match: SkillMatchingOutput
    insights: CandidateInsights
    red_flags: RedFlagReport