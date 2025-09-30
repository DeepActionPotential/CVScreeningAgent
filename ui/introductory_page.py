# 📄 intro_page.py
import streamlit as st
import pathlib
import tempfile
import os

class IntroductoryPage:
    def __init__(self):
        self.jd_file = None
        self.cv_files = None

    def render(self, screening_manager=None):
        # Set page config
        

        # --- Title ---
        st.markdown('<div class="header-text">🧠 CV Screening Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader-text">Upload your Job Description and candidate CVs to get started.</div>', unsafe_allow_html=True)

        # --- Layout ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Job Description")
            self.jd_file = st.file_uploader("Upload JD (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="jd")

        with col2:
            st.subheader("👥 Candidate CVs")
            self.cv_files = st.file_uploader("Upload CVs (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="cvs")

        st.markdown("---")

        if self.jd_file and self.cv_files:
            st.success("Files uploaded successfully! Ready for analysis.")
            if st.button("🚀 Run Screening"):
                with st.spinner("Analyzing CVs..."):
                    temp_dir = tempfile.mkdtemp()

                    # Save JD
                    jd_path = os.path.join(temp_dir, self.jd_file.name)
                    with open(jd_path, "wb") as f:
                        f.write(self.jd_file.read())

                    # Save CVs
                    cv_paths = []
                    for cv_file in self.cv_files:
                        path = os.path.join(temp_dir, cv_file.name)
                        with open(path, "wb") as f:
                            f.write(cv_file.read())
                        cv_paths.append(path)

                    st.session_state["show_results"] = True
                    st.session_state["jd_path"] = jd_path
                    st.session_state["cv_paths"] = cv_paths

                    st.rerun()
        else:
            st.warning("Please upload both Job Description and at least one CV to continue.")
