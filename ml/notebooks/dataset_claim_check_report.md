# Dataset claim check

Data folder: `E:\Documents\advanced_statistics\fyp\founders-carnet\carnet_data\data`

| dataset | claim | report says | file shows | result |
|---|---|---|---|---|
| Roman-Urdu-Parl | read from local folder | (no number in report) | roman_urdu_parl_split_dataset | INFO |
| Roman-Urdu-Parl | rows per split found | (no number in report) | {'test': 20741, 'validation': 20719, 'train': 6365808} | INFO |
| Roman-Urdu-Parl | train rows | 6333218 | 6365808 | FAIL |
| Roman-Urdu-Parl | validation rows | 20719 | 20719 | PASS |
| Roman-Urdu-Parl | test rows | 20741 | 20741 | PASS |
| Roman-Urdu-Parl | total rows | 6374678 | 6407268 | FAIL |
| Roman-Urdu-Parl | difference from the paper's 6,365,808 | (no number in report) | 41460 | INFO |
| Roman-Urdu-Parl | columns | ['Urdu text', 'Roman-Urdu text'] | ['Urdu text', 'Roman-Urdu text'] | PASS |
| LinkedIn | LICENSE file present in repo (report: none stated) | False | False | PASS |
| LinkedIn | pickle type | (no number in report) | DataFrame | INFO |
| LinkedIn | profiles (rows) | 3600 | 3600 | PASS |
| LinkedIn | columns | 39 | 39 | PASS |
| LinkedIn | columns that look like personal fields (report: excluded, never used) | (no number in report) | ['Full Name'] | INFO |
| LinkedIn | candidate label column 'Photo' | (no number in report) | {'Yes': 3062, 'No': 538} | INFO |
| LinkedIn | candidate label column 'Number of Educations' | (no number in report) | {2: 1266, 1: 925, 3: 924, 0: 485} | INFO |
| LinkedIn | candidate label column 'Number of Licenses' | (no number in report) | {0: 2581, 3: 478, 1: 349, 2: 192} | INFO |
| LinkedIn | candidate label column 'Number of Volunteering' | (no number in report) | {0: 2607, 3: 424, 1: 320, 2: 249} | INFO |
| LinkedIn | candidate label column 'Number of Skills' | (no number in report) | {3: 2762, 0: 762, 1: 57, 2: 19} | INFO |
| LinkedIn | candidate label column 'Number of Recommendations' | (no number in report) | {0: 2152, 6: 471, 1: 347, 3: 175, 2: 169, 4: 163, 5: 123} | INFO |
| LinkedIn | candidate label column 'Number of Projects' | (no number in report) | {0: 3343, 3: 108, 1: 106, 2: 43} | INFO |
| LinkedIn | candidate label column 'Number of Publications' | (no number in report) | {0: 3226, 3: 210, 1: 110, 2: 54} | INFO |
| LinkedIn | candidate label column 'Number of Courses' | (no number in report) | {0: 3296, 3: 199, 1: 66, 2: 39} | INFO |
| LinkedIn | candidate label column 'Number of Honors' | (no number in report) | {0: 2922, 3: 381, 1: 186, 2: 111} | INFO |
| LinkedIn | candidate label column 'Number of Scores' | (no number in report) | {0: 3559, 1: 24, 2: 10, 3: 7} | INFO |
| LinkedIn | candidate label column 'Number of Languages' | (no number in report) | {0: 2676, 2: 360, 3: 288, 1: 276} | INFO |
| LinkedIn | candidate label column 'Number of Organizations' | (no number in report) | {0: 2990, 3: 252, 1: 236, 2: 122} | INFO |
| LinkedIn | candidate label column 'Label' | (no number in report) | {0: 1800, 1: 600, 10: 600, 11: 600} | INFO |
| LinkedIn | group sizes (1,800 + 600 + 600 + 600) | [600, 600, 600, 1800] | [600, 600, 600, 1800] | PASS |
| Crunchbase success/fail | rows | 66368 | 66368 | PASS |
| Crunchbase success/fail | columns | 14 | 14 | PASS |
| Crunchbase success/fail | has a status field | True | True | PASS |
| Crunchbase success/fail | status values | (no number in report) | {'operating': 53034, 'closed': 6238, 'acquired': 5549, 'ipo': 1547} | INFO |
| Crunchbase success/fail | columns that look like personal fields (report: excluded, never used) | (no number in report) | ['name'] | INFO |
| Crunchbase success/fail | duplicate rows | (no number in report) | 0 | INFO |
| Crunchbase investments | rows | 54294 | 54294 | PASS |
| Crunchbase investments | columns | 39 | 39 | PASS |
| Crunchbase investments | duplicate rows | 4855 | 4855 | PASS |
| Crunchbase investments | columns that look like personal fields (report: excluded, never used) | (no number in report) | ['name'] | INFO |
| HSE resume-job | columns | 91 | 91 | PASS |
| HSE resume-job | columns that look like personal fields (report: excluded, never used) | (no number in report) | ['gender', 'age'] | INFO |
| HSE resume-job | pairs (rows) | 150493 | 150493 | PASS |
| HSE resume-job | unique resumes | 65714 | 65714 | PASS |
| HSE resume-job | unique vacancies | 43756 | 43756 | PASS |
| HSE resume-job | cv_status values | (no number in report) | {'Отказ': 129503, 'Приглашение': 20990} | INFO |
| HSE resume-job | rejected % | 86.1 | 86.1 | PASS |
| HSE resume-job | invited % | 13.9 | 13.9 | PASS |
| Resume Dataset PDF | PDF files | 8905 | 8905 | PASS |
| Resume Dataset PDF | files with extractable text in the 30-file sample | 0 | 0 | PASS |
| ATS dataset | file used | (no number in report) | ats_resume_dataset_elite_v3.csv | INFO |
| ATS dataset | rows | 6000 | 6000 | PASS |
| ATS dataset | columns that look like personal fields (report: excluded, never used) | (no number in report) | none | INFO |
| ATS dataset | mean characters per text column | (no number in report) | {'resume_id': np.float64(4.8), 'resume_text': np.float64(376.9), 'resume_skills': np.float64(51.1), 'education_level': np.float64(6.3), 'projects': np.float64(102.6), 'certifications': np.float64(29.5), 'job_role': np.float64(14.8), 'required_skills': np.float64(51.0), 'job_description': np.float64(131.8)} | INFO |
| ATS dataset | mean resume text length ('resume_text') | 376 | 377 | PASS |
| ATS dataset | 'experience_years': 11 distinct values; top share | (no number in report) | 0.1 | INFO |
| ATS dataset | 'education_level': 3 distinct values; top share | (no number in report) | 0.342 | INFO |
| ATS dataset | 'job_experience_required': 6 distinct values; top share | (no number in report) | 0.173 | INFO |
| ATS dataset | 'experience_match': 2 distinct values; top share | (no number in report) | 0.688 | INFO |
| ATS dataset | 'education_match': 2 distinct values; top share | (no number in report) | 0.674 | INFO |
| ATS dataset | duplicate rows | (no number in report) | 0 | INFO |
| Crunchbase success/fail | missing % — name | (no number in report) | 0.0% | INFO |
| Crunchbase success/fail | missing % — status | (no number in report) | 0.0% | INFO |
| Crunchbase success/fail | missing % — category_list | (no number in report) | 4.7% | INFO |
| Crunchbase success/fail | missing % — country_code | (no number in report) | 10.5% | INFO |
| Crunchbase success/fail | missing % — founded_at | (no number in report) | 22.9% | INFO |
| Crunchbase success/fail | missing % — funding_total_usd | (no number in report) | 0.0% | INFO |
| Crunchbase investments | missing % — funding_total_usd | (no number in report) | 8.9% | INFO |
| Crunchbase investments | missing % — funding_rounds | (no number in report) | 8.9% | INFO |
| Crunchbase investments | missing % — country_code | (no number in report) | 18.7% | INFO |
| Crunchbase investments | missing % — founded_at | (no number in report) | 29.0% | INFO |
| Crunchbase investments | missing % — status | (no number in report) | 11.4% | INFO |
| Crunchbase success/fail | founded_at range | (no number in report) | 1015-01-30 to 2914-01-01 (0 NaT) | INFO |
| Crunchbase success/fail | first_funding_at range | (no number in report) | 1014-03-01 to 2015-12-05 (0 NaT) | INFO |
| Crunchbase success/fail | last_funding_at range | (no number in report) | 1971-01-01 to 2115-12-01 (0 NaT) | INFO |
| Crunchbase investments | founded_at range | (no number in report) | 1636-09-08 to 2014-12-13 (0 NaT) | INFO |
| Crunchbase investments | first_funding_at range | (no number in report) | 0001-05-14 to 2014-12-31 (0 NaT) | INFO |
| Crunchbase investments | last_funding_at range | (no number in report) | 0001-05-14 to 2015-01-01 (0 NaT) | INFO |
| Crunchbase investments | funding_total_usd: non-null count | (no number in report) | 40907 | INFO |
| Crunchbase investments | funding_total_usd: negative values | (no number in report) | 0 | INFO |
| Crunchbase investments | funding_total_usd: zero values | (no number in report) | 0 | INFO |
| Crunchbase investments | funding_total_usd: median USD | (no number in report) | $2,000,000 | INFO |
| Crunchbase investments | funding_total_usd: max USD | (no number in report) | $30,079,503,000 | INFO |
| ATS dataset | label column candidates | (no number in report) | none found matching keywords | INFO |
| Roman-Urdu-Parl | file extensions found | (no number in report) | ['', '.csv', '.md', '.py', '.txt'] | INFO |
| Roman-Urdu-Parl | 'Urdu text': Arabic-script chars % | (no number in report) | 78.1% | INFO |
| Roman-Urdu-Parl | 'Roman-Urdu text': Latin chars % | (no number in report) | 81.4% | INFO |
| LinkedIn | columns with >50% missing | (no number in report) | {} | INFO |
| LinkedIn | columns with 0% missing | (no number in report) | ['Intro', 'Connections', 'Photo', 'Followers', 'About', 'Experiences', 'Number of Experiences', 'Educations', 'Number of Educations', 'Licenses', 'Number of Licenses', 'Volunteering', 'Number of Volunteering', 'Skills', 'Number of Skills', 'Recommendations', 'Number of Recommendations', 'Projects', 'Number of Projects', 'Publications', 'Number of Publications', 'Courses', 'Number of Courses', 'Honors', 'Number of Honors', 'Scores', 'Number of Scores', 'Languages', 'Number of Languages', 'Organizations', 'Number of Organizations', 'Interests', 'Number of Interests', 'Activities', 'Number of Activities', 'Label'] | INFO |
| HSE resume-job | 'idVacancy': Cyrillic char % | (no number in report) | 0.0% (expected >50% for Russian) | INFO |
| HSE resume-job | 'localityName': Cyrillic char % | (no number in report) | 83.8% (expected >50% for Russian) | INFO |