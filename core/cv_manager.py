from schemas.services_schemas import FileReadInput
from schemas.services_schemas import CVAnalysisResult
from schemas.services_schemas import SkillMatchingInput

import time

class CVScreeningManager:
    """
    Manages the end-to-end process of screening CVs against a job description.
    """

    def __init__(
        self,
        file_manager_agent,
        cv_parser_agent,
        job_description_agent,
        skill_matching_agent,
        insight_generator_agent,
        red_flag_detector_agent,
    ):
        """
        Initializes the CVScreeningManager with required agents.
        """
        self.file_manager_agent = file_manager_agent
        self.cv_parser_agent = cv_parser_agent
        self.job_description_agent = job_description_agent
        self.skill_matching_agent = skill_matching_agent
        self.insight_generator_agent = insight_generator_agent
        self.red_flag_detector_agent = red_flag_detector_agent

    def run_cv_against_jd(self, cv_path: str, jd_path: str, verbose: bool = False, sleep_time_between_requests: int = 0) -> CVAnalysisResult:
        """
        Processes a single CV against a job description and returns the analysis result.

        Args:
            cv_path (str): Path to the candidate's CV file.
            jd_path (str): Path to the job description file.
            verbose (bool): If True, prints step-by-step progress.

        Returns:
            CVAnalysisResult: Structured result of the analysis.
        """
        if verbose:
            print(f"Reading CV from: {cv_path}")
            
        cv_input = FileReadInput(file_path=cv_path)
        raw_cv = self.file_manager_agent.run(cv_input)
        time.sleep(sleep_time_between_requests)

        if verbose:
            print("Parsing CV...")
        parsed_cv = self.cv_parser_agent.run(raw_cv)
        time.sleep(sleep_time_between_requests)

        if verbose:
            print(f"Reading Job Description from: {jd_path}")
        jd_input = FileReadInput(file_path=jd_path)
        raw_jd = self.file_manager_agent.run(jd_input)
        time.sleep(sleep_time_between_requests)

        if verbose:
            print("Parsing Job Description...")
        parsed_jd = self.job_description_agent.run(raw_jd)
        time.sleep(sleep_time_between_requests)


        if verbose:
            print("Matching skills between CV and Job Description...")
        matching_input = SkillMatchingInput(candidate=parsed_cv, job=parsed_jd)
        skill_match = self.skill_matching_agent.run(matching_input)
        time.sleep(sleep_time_between_requests)


        if verbose:
            print("Generating candidate insights...")
        insights = self.insight_generator_agent.run(skill_match)
        time.sleep(sleep_time_between_requests)

        if verbose:
            print("Detecting red flags...")
        red_flags = self.red_flag_detector_agent.run(skill_match)
        time.sleep(sleep_time_between_requests)


        if verbose:
            print("Analysis complete.\n")

        return CVAnalysisResult(
            cv=parsed_cv,
            job_description=parsed_jd,
            skill_match=skill_match,
            insights=insights,
            red_flags=red_flags
        )

    def run_cvs_against_jd(self, cv_paths: list[str], jd_path: str, verbose: bool = False, sleep_time_between_requests: int = 0) -> list[CVAnalysisResult]:
        """
        Processes multiple CVs against a job description and returns a list of analysis results.

        Args:
            cv_paths (list[str]): List of paths to candidate CV files.
            jd_path (str): Path to the job description file.
            verbose (bool): If True, prints step-by-step progress for each CV.

        Returns:
            list[CVAnalysisResult]: List of structured analysis results for each CV.
        """
        results: list[CVAnalysisResult] = []
        for idx, cv_path in enumerate(cv_paths, 1):
            time.sleep(sleep_time_between_requests)
            if verbose:
                print(f"\n--- Processing CV {idx}/{len(cv_paths)} ---")
            result = self.run_cv_against_jd(cv_path, jd_path, verbose=verbose)
            results.append(result)
        if verbose:
            print("\nAll CVs processed.")
        return results