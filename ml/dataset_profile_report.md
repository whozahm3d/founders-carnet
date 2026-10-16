# Dataset profiling report (Track B)

Run date: 2026-10-03

## Roman-Urdu-Parl (HF split)

- Source: Mavkif/Roman-Urdu-Parl-split
- Role: Multilingual benchmark source
- Access date: 2026-10-03
- Licence: not stated in dataset card metadata
- Splits: {'train': 6333218, 'validation': 20719, 'test': 20741}
- Total rows: 6374678
- Features: {'Urdu text': "Value('string')", 'Roman-Urdu text': "Value('string')"}
- First 5 sampled pairs:
  - {"Urdu text": "وکیل", "Roman-Urdu text": "wakeel"}
  - {"Urdu text": "وکیل", "Roman-Urdu text": "wakeel"}
  - {"Urdu text": "وکیل ایک ایسی شخصیت کو کہا جاتا ہے کہ جو دوسرے اپنے صارف کی جانب سے یا اسکی بابت گفتگو کرے اس مضمون میں یہ گفتگو قانون سے متعلق تصور کی گئی ہے اور اس وجہ سے یہ مضمون صرف قانونی وکلا کے بارے میں ذکر کرتا ہے", "Roman-Urdu text": "wakeel 
  - {"Urdu text": "وکیل قانون", "Roman-Urdu text": "wakeel qanoon"}
  - {"Urdu text": "وکیل قانون ایک شخص جسے دوسرے شخص کی جگہ کام کرنے یا کی نمائندگی کرنے کا اختیار حاصل ہوتا ہے وکیل سفر ایک شخص جو تعطیلات اور سفر کا بندوبست کرتا ہے خفیہ وکیل ایک جاسوس", "Roman-Urdu text": "wakeel qanoon 1 shakhs jisay dosray shakhs ki 

## LinkedIn-Dataset (Ayoobi et al.)

- Source: https://github.com/navid-aub/LinkedIn-Dataset
- Role: Profile-verification reference
- Access date: 2026-10-03
- Licence: no LICENSE file in repo
- Size: 25.19 MB
- Other files: {'.pcl': 1, '.md': 1}

## Kaggle: Startup Success/Fail (Crunchbase)

- Source: https://www.kaggle.com/datasets/yanmaksi/big-startup-secsees-fail-dataset-from-crunchbase
- Role: Schema proxy only
- Access date: 2026-10-03
- Licence: not stated
- Size: 10.44 MB
- Other files: {'.json': 1}
- `big_startup_secsees_dataset.csv`: 66,368 rows x 14 columns, duplicates: 0
  - Missing (%): founded_at 22.93, state_code 12.88, region 12.1, city 12.1, country_code 10.48, homepage_url 7.62, category_list 4.74, first_funding_at 0.04
  - `status` values: {'operating': 53034, 'closed': 6238, 'acquired': 5549, 'ipo': 1547}
  - Columns: permalink, name, homepage_url, category_list, funding_total_usd, status, country_code, state_code, region, city, funding_rounds, founded_at, first_funding_at, last_funding_at

## Kaggle: StartUp Investments (Crunchbase)

- Source: https://www.kaggle.com/datasets/arindam235/startup-investments-crunchbase
- Role: Schema proxy only
- Access date: 2026-10-03
- Licence: not stated
- Size: 11.95 MB
- Other files: {'.json': 1}
- `investments_VC.csv`: 54,294 rows x 39 columns, duplicates: 4855
  - Missing (%): state_code 44.45, founded_month 29.12, founded_quarter 29.12, founded_year 29.12, founded_at 28.99, city 20.21, country_code 18.66, region 18.66
  - `status` values: {'operating': 41829, 'nan': 6170, 'acquired': 3692, 'closed': 2603}
  - `round_H` values: {'0.0': 49434, 'nan': 4856, '50000000.0': 1, '600000000.0': 1, '49000000.0': 1, '4600000.0': 1}
  - Columns: permalink, name, homepage_url, category_list,  market ,  funding_total_usd , status, country_code, state_code, region, city, funding_rounds, founded_at, founded_month, founded_quarter, founded_year, first_funding_at, last_funding_at, seed, venture, equity_crowdfunding, undisclosed, convertible_note, debt_financing, angel

## HSE Resume-Job Matching

- Source: https://www.kaggle.com/datasets/darysha/hse-hackathon
- Role: Matching-pipeline practice proxy
- Access date: 2026-10-03
- Licence: not stated
- Size: 973.06 MB
- Other files: {'.json': 1}
- `train.csv`: ERROR ParserError: Error tokenizing data. C error: Expected 75 fields in line 3, saw 194


## Resume Dataset PDF

- Source: https://www.kaggle.com/datasets/hadikp/resume-data-pdf
- Role: Test inputs for resume optimizer
- Access date: 2026-10-03
- Licence: not stated
- Total PDFs: 8905
- Per folder: {'Accountant': 284, 'Accountant resumes': 67, 'Advocate': 247, 'Advocate resumes': 94, 'Agricultural': 199, 'Agricultural resumes': 68, 'Agriculture': 79, 'Apparel': 69, 'Apparel resumes': 51, 'Architect': 84, 'Architects resumes': 60, 'Arts': 255, 'Arts resumes': 68, 'Automobile': 73, 'Automobile resumes': 40, 'Aviation': 200, 'Aviation resumes': 51, 'BPO resumes': 29, 'Banking': 221, 'Banking resumes': 41, 'Blockchain': 24, 'Blockchain resumes': 8, 'Building _Construction resumes': 55, 'Business Analyst resumes': 56, 'BusinessAnalyst': 77, 'Civil Engineer resumes': 73, 'CivilEngineer': 76, 'Consult': 99, 'Consultant': 148, 'Consultant resumes': 71, 'DOT': 66, 'Data Science': 200, 'DataScience': 42, 'Database': 186, 'Database resumes': 63, 'Design': 67, 'Designer': 200, 'Designing resumes': 36, 'DevOps Engineer': 144, 'DevOps Engineer resumes': 72, 'DevOpsEngineer': 60, 'Digital': 85, 'Digital Media': 129, 'Digital Media resumes': 68, 'DotNet Developer resumes': 59, 'ETL': 30, 'ETL Developer': 154, 'ETL Developer resumes': 60, 'Education': 210, 'Education resumes': 53, 'Electrical Engineering resumes': 71, 'ElectricalEngineer': 105, 'Finance': 86, 'Finance resumes': 56, 'Food': 80, 'Food_Beverages resumes': 62, 'HR': 74, 'HR resumes': 85, 'HealthFitness': 56, 'Health_Fitness resumes': 76, 'Human Resources': 199, 'IT': 85, 'Information Technology': 139, 'Information Technology resumes': 46, 'Java Developer resumes': 67, 'JavaDeveloper': 72, 'Management': 248, 'Managment resumes': 52, 'Mechanical Engineer resumes': 103, 'MechanicalEngineer': 82, 'NSE': 69, 'Network Security Engineer resumes': 56, 'OperationManager': 69, 'Operations Manager resumes': 70, 'PBO': 73, 'PMO': 47, 'PMO resumes': 49, 'Public': 71, 'Public Relations resumes': 68, 'Python Developer': 142, 'Python Developer resumes': 48, 'PythonDeveloper': 50, 'React': 20, 'React Developer': 200, 'React Developer resumes': 18, 'SAP Developer': 150, 'SAP Developer resumes': 57, 'SAPDeveloper': 41, 'SQL': 57, 'SQL Developer resumes': 82, 'Sales': 74, 'Sales resumes': 90, 'Testing': 269, 'Testing resumes': 68, 'WebDesigning': 53, 'data science resumes': 60, 'web designing resumes': 59}
- Text extraction (sample): {'sample_size': 30, 'files_with_text': 0, 'pct_with_text': 0.0, 'median_chars': 0}
- PII patterns (sample): {'email_patterns': 0, 'phone_patterns': 0}
- Non-PDF files: {'.json': 1}

## ATS Dataset NLP+ML

- Source: https://www.kaggle.com/datasets/amaymishra11/resume-screening-dataset-ats-and-nlp-ready
- Role: Resume/JD text pairs as test inputs (scores ignored)
- Access date: 2026-10-03
- Licence: not stated
- Size: 4.73 MB
- Other files: {'.json': 1}
- `ats_resume_dataset_elite_v3.csv`: 6,000 rows x 17 columns, duplicates: 0
  - Missing (%): certifications 34.3
  - `experience_years` values: {'9': 597, '3': 585, '2': 556, '5': 543, '8': 543, '10': 539, '6': 537, '7': 536, '4': 528, '1': 526, '0': 510}
  - `education_level` values: {'Masters': 2050, 'PhD': 1993, 'Bachelors': 1957}
  - `job_role` values: {'Data Scientist': 1064, 'Software Engineer': 1017, 'Data Analyst': 991, 'Frontend Developer': 989, 'ML Engineer': 976, 'Backend Developer': 963}
  - `job_experience_required` values: {'3': 1037, '5': 1032, '4': 1030, '6': 997, '2': 967, '1': 937}
  - `experience_match` values: {'1': 4129, '0': 1871}
  - Long-text columns: {'resume_text': {'mean_chars': 376, 'median_chars': 377}}
  - PII pattern counts: {'email_patterns_in_first_5000_rows': 0, 'phone_patterns_in_first_5000_rows': 0}
  - Columns: resume_id, resume_text, resume_skills, experience_years, education_level, projects, certifications, job_role, required_skills, job_experience_required, job_description, skill_match_score, experience_match, education_match, final_score, shortlisted, similarity_score
