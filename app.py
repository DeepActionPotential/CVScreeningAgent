import streamlit as st

# --- Page Modules ---
from ui.introductory_page import IntroductoryPage
from ui.results_page import ResultsPage
from core.cv_manager import CVScreeningManager

# --- Agent & Service Modules ---
from agents.agents import (
    FileManagerAgent,
    CVParserAgent,
    JobDescriptionAgent,
    SkillMatchingAgent,
    InsightGeneratorAgent,
    RedFlagDetectorAgent,
)
from services.input_service import FileManager
from config import DefaultCFG
# --- LLM Provider ---
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider



# # === SETUP AI MODEL ===
provider = GoogleProvider(api_key=DefaultCFG.api_key)
model = GoogleModel(model_name=DefaultCFG.model_name, provider=provider)




# === INITIALIZE AGENTS ===
file_manager_agent = FileManagerAgent(service=FileManager(), model=model)
cv_parser_agent = CVParserAgent(model=model)
job_description_agent = JobDescriptionAgent(model=model)
skill_matching_agent = SkillMatchingAgent(model=model)
insight_generator_agent = InsightGeneratorAgent(model=model)
red_flag_detector_agent = RedFlagDetectorAgent(model=model)

# === SCREENING MANAGER ===
screening_manager = CVScreeningManager(
    file_manager_agent=file_manager_agent,
    cv_parser_agent=cv_parser_agent,
    job_description_agent=job_description_agent,
    skill_matching_agent=skill_matching_agent,
    insight_generator_agent=insight_generator_agent,
    red_flag_detector_agent=red_flag_detector_agent,
)

# === PAGE ROUTING ===

st.set_page_config(
            page_title="CV Screening Assistant",
            page_icon="🧠",
            layout="centered",
            initial_sidebar_state="auto"
        )


with open('./ui/styles.css', "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

if not st.session_state["show_results"]:
    intro_page = IntroductoryPage()
    intro_page.render(screening_manager)
else:
    results_page = ResultsPage(
        screening_manager=screening_manager,
        jd_path=st.session_state["jd_path"],
        cv_paths=st.session_state["cv_paths"]
    )
    results_page.render()
