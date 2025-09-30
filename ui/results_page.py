import streamlit as st
from typing import List
from core.cv_manager import CVScreeningManager
from schemas.services_schemas import CVAnalysisResult, ParsedCV, ParsedJobDescription, SkillMatchingOutput, CandidateInsights, RedFlagReport
from config import DefaultCFG


from schemas.services_schemas import CVAnalysisResult, ParsedCV, ParsedJobDescription, SkillMatchingOutput, CandidateInsights, RedFlagReport




class ResultsPage:
    def __init__(self, screening_manager: CVScreeningManager, jd_path: str, cv_paths: List[str]):
        self.screening_manager = screening_manager
        self.jd_path = jd_path
        self.cv_paths = cv_paths

    def render(self):
        st.markdown('<div class="header-text">📊 Screening Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader-text">Click on a candidate card to view personalized insights and match details.</div>', unsafe_allow_html=True)

        results: List[CVAnalysisResult] = self.screening_manager.run_cvs_against_jd(
            self.cv_paths, self.jd_path, verbose=False, sleep_time_between_requests=DefaultCFG.sleep_time_between_requests
        )
        for idx, result in enumerate(results, 1):
            cv: ParsedCV = result.cv
            jd: ParsedJobDescription = result.job_description
            skill: SkillMatchingOutput = result.skill_match
            insights: CandidateInsights = result.insights
            red_flags: RedFlagReport = result.red_flags

            candidate_name = cv.name or f"Candidate {idx}"

            with st.expander(f"👤 {candidate_name} ({round(skill.total_score)}% match)"):
                # --- Job Description Summary Sticky Box ---
                st.markdown(
                    f"""
                    <div style='background-color: #26272B; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;'>
                        <strong>📋 {jd.job_title}</strong> at <strong>{jd.company}</strong><br>
                        <span style="color: #aaa;">{jd.location or 'Location N/A'} | {jd.employment_type}, {jd.seniority_level}</span><br><br>
                        <em>{jd.job_summary or 'No summary available.'}</em>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # --- Metrics Row ---
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Match", f"{skill.total_score:.1f}%", delta=None)
                col2.metric("Skill Score", f"{skill.skill_score:.0f}%")
                col3.metric("Experience Score", f"{skill.experience_score:.0f}%")

                st.divider()

                # 🎯 Skills Section
                st.subheader("🎯 Skills & Responsibilities Overview")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Matched Skills**")
                    for skill_tag in skill.matched_skills or []:
                        st.markdown(f"<span style='background:#0e6251;padding:6px 10px;border-radius:5px;margin-right:4px;color:white;'>{skill_tag}</span>", unsafe_allow_html=True)
                with col2:
                    st.markdown("**❌ Missing Skills**")
                    for missing in skill.missing_skills or []:
                        st.markdown(f"<span style='background:#922b21;padding:6px 10px;border-radius:5px;margin-right:4px;color:white;'>{missing}</span>", unsafe_allow_html=True)

                # Responsibilities
                with st.container():
                    st.markdown("#### 📋 Responsibilities Match")
                    st.markdown("**✅ Matched Responsibilities:**")
                    for r in skill.matched_responsibilities or []:
                        st.success(f"✓ {r}")
                    st.markdown("**❌ Missing Responsibilities:**")
                    for r in skill.missing_responsibilities or []:
                        st.error(f"✗ {r}")

                st.divider()

                # 💡 Insights
                st.subheader("💡 Candidate Insights")
                st.markdown(f"> {insights.insight_summary or 'No insight summary.'}")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✔️ Strengths**")
                    for s in insights.strengths or []:
                        st.success(f"{s}")
                with col2:
                    st.markdown("**⚠️ Weaknesses**")
                    for w in insights.weaknesses or []:
                        st.warning(f"{w}")

                if insights.potential:
                    st.info(f"🌟 Potential: _{insights.potential}_")

                st.divider()

                # 🚩 Red Flags
                if red_flags.red_flags:
                    st.subheader("🚩 Red Flags")
                    for f in red_flags.red_flags:
                        st.error(f"⚠️ {f}")
                    st.caption(f"Severity: **{red_flags.severity_level}** — {red_flags.flagged_summary}")
                else:
                    st.success("✅ No red flags detected.")

                st.divider()

                # 📄 CV Details Tabs
                tab1, tab2 = st.tabs(["📄 Candidate Info", "📋 JD Requirements"])

                with tab1:
                    st.markdown(f"**Name:** {cv.name}")
                    st.markdown(f"**Email:** `{cv.email}` | **Phone:** `{cv.phone}`")
                    st.markdown("**Summary:**")
                    st.markdown(f"> {cv.summary or 'N/A'}")
                    st.markdown("**🎓 Education:**")
                    for edu in cv.education or []:
                        st.markdown(f"- {edu}")
                    st.markdown("**💼 Experience:**")
                    for exp in cv.experience or []:
                        st.markdown(f"- {exp}")
                    if cv.certifications:
                        st.markdown("**📜 Certifications:**")
                        for cert in cv.certifications:
                            st.markdown(f"- {cert}")
                    if cv.skills:
                        st.markdown("**🏷️ Skills:**")
                        st.code(", ".join(cv.skills))

                with tab2:
                    st.markdown("**Required Skills:**")
                    st.code(", ".join(jd.required_skills or []))
                    if jd.qualifications:
                        st.markdown("**Qualifications:**")
                        for q in jd.qualifications:
                            st.markdown(f"- {q}")
                    if jd.responsibilities:
                        st.markdown("**Responsibilities:**")
                        for r in jd.responsibilities:
                            st.markdown(f"- {r}")
                    st.markdown(f"**Industry:** {jd.industry}")
