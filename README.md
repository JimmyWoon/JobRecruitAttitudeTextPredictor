# JobRecruitAttitudeTextPredictor

This project aimed to develop a recruitment system that automates the extraction of valuable information from candidate-submitted documents within a recruitment-based platform. The system also allows users to upload self-introduction videos as an alternative to the traditional resume file selection. This innovative approach significantly reduces recruitment efforts, enhances HR staff performance, and provides an improved user experience.

The web application, built using Flask (a Python library) and SQL Alchemy, efficiently allocates resources and streamlines the recruitment process, leading to informed decisions for optimized workforce management. To analyze the attitudes expressed in job resumes, the system utilizes Support Vector Machine (SVM) as the underlying methodology. The benchmarks for evaluating candidate attitude traits are based on previous research and findings from other researchers.

A parser machine was implemented to analyze textual information from uploaded candidate resumes in PDF, DOCX, and DOC formats, as well as video files in MP4 format. For video input, the Moviepy library was utilized to convert spoken language by the candidate into written text.
