## Tech-subset checks

Date: 2026-10-17

| dataset | claim | report says | file shows | result |
|---|---|---|---|---|
| Resume Dataset PDF | excluded from final set | (no prior claim) | image-only PDF; 0 of 30 sampled files had extractable text | INFO |
| Resume Dataset PDF | tech-niche applicability | (no prior claim) | not applicable; no text content available for any filter | INFO |
| ATS dataset | excluded from final set | (no prior claim) | short uniform texts; no duplicate rows; consistent with synthetic generation | INFO |
| ATS dataset | tech-niche applicability | (no prior claim) | not applicable; synthetic-looking data excluded from all subsets | INFO |
| Crunchbase success/fail | raw rows | (no prior claim) | 66368 | INFO |
| Crunchbase success/fail | rows with missing category_list (excluded from tech subset) | (no prior claim) | 3148 | INFO |
| Crunchbase success/fail | tech rows (category filter) | (no prior claim) | 28695 | INFO |
| Crunchbase success/fail | tech % of non-missing category rows | (no prior claim) | 45.4% | INFO |
| Crunchbase success/fail | status distribution in tech subset | (no prior claim) | {'operating': 23211, 'acquired': 2834, 'closed': 2221, 'ipo': 429} | INFO |
| Crunchbase success/fail | top 15 matched tech categories | (no prior claim) | {'software': 8768, 'mobile': 5557, 'e-commerce': 4152, 'enterprise software': 2694, 'internet': 2071, 'saas': 1989, 'apps': 1876, 'analytics': 1839, 'hardware + software': 1499, 'big data': 929, 'cloud computing': 919, 'information technology': 910, 'fintech': 731, 'web development': 571, 'internet of things': 469} | INFO |
| Crunchbase success/fail | founded_at 1990-2015: rows in range (count only) | (no prior claim) | 23840 | INFO |
| Crunchbase success/fail | founded_at 1990-2015: rows out of range (count only) | (no prior claim) | 388 | INFO |
| Crunchbase success/fail | founded_at 1990-2015: unparseable or missing (count only) | (no prior claim) | 4467 | INFO |
| Crunchbase investments | raw rows | (no prior claim) | 54294 | INFO |
| Crunchbase investments | rows with missing category_list (excluded from tech subset) | (no prior claim) | 8817 | INFO |
| Crunchbase investments | tech rows before dropping duplicates | (no prior claim) | 20542 | INFO |
| Crunchbase investments | tech rows after dropping duplicates | (no prior claim) | 20542 | INFO |
| Crunchbase investments | tech % of non-missing category rows | (no prior claim) | 45.2% | INFO |
| Crunchbase investments | top 15 matched tech categories | (no prior claim) | {'software': 6882, 'mobile': 4430, 'e-commerce': 3240, 'enterprise software': 2243, 'analytics': 1406, 'hardware + software': 1358, 'saas': 1218, 'internet': 918, 'apps': 900, 'cloud computing': 673, 'big data': 567, 'web development': 434, 'information technology': 284, 'internet marketing': 260, 'mobile commerce': 225} | INFO |
| Crunchbase investments | founded_at 1990-2015: rows in range (count only) | (no prior claim) | 17264 | INFO |
| Crunchbase investments | founded_at 1990-2015: rows out of range (count only) | (no prior claim) | 299 | INFO |
| Crunchbase investments | founded_at 1990-2015: unparseable or missing (count only) | (no prior claim) | 2979 | INFO |
| LinkedIn | columns that could carry industry or headline text | (no prior claim) | ['Intro', 'About', 'Experiences', 'Number of Experiences'] | INFO |
| LinkedIn | Intro column: rows matching tech keywords (informational) | (no prior claim) | 661 | INFO |
| LinkedIn | Intro column: tech match % (informational) | (no prior claim) | 18.4% | INFO |
| LinkedIn | Label distribution inside tech-match rows (informational) | (no prior claim) | {0: 229, 10: 183, 11: 182, 1: 67} | INFO |
| LinkedIn | NOTE | (no prior claim) | LinkedIn is kept whole; Intro keyword count is informational; no rows are filtered | INFO |
| Roman-Urdu-Parl | tech filter | (no prior claim) | no tech filter applied; language data kept whole | INFO |
| Roman-Urdu-Parl | README states: original dataset total | (no prior claim) | 6,365,808 rows | INFO |
| Roman-Urdu-Parl | files show: train rows | (no prior claim) | 6365808 | INFO |
| Roman-Urdu-Parl | files show: validation rows | (no prior claim) | 20719 | INFO |
| Roman-Urdu-Parl | files show: test rows | (no prior claim) | 20741 | INFO |
| Roman-Urdu-Parl | README vs files: validation | (no prior claim) | card: 20,719; files: 20,719 -- match | INFO |
| Roman-Urdu-Parl | README vs files: test | (no prior claim) | card: 20,741; files: 20,741 -- match | INFO |
| Roman-Urdu-Parl | README vs files: original total | (no prior claim) | README states 6,365,808 (original dataset); train split file shows 6,365,808 rows | INFO |

## Filters used

**TECH_CATEGORIES** (Crunchbase; matched against pipe-delimited category_list, lowercased):

- software
- saas
- artificial intelligence
- machine learning
- analytics
- big data
- enterprise software
- internet
- mobile
- apps
- web development
- cloud computing
- cyber security
- fintech
- e-commerce
- computer vision
- data
- developer tools
- information technology

**HSE IT filter:**
- Column: see 'IT filter column used' row in table above
- Keywords (English): it, software, developer, programmer, data, devops, qa, testing
- Keywords (Russian): тестировщик, программист, разработчик, аналитик данных,
  системный администратор, информационные технологии

**LinkedIn tech keyword list** (Intro column only, informational):

- software
- engineer
- developer
- data
- machine learning
- artificial intelligence
- cloud
- devops
- backend
- frontend
- full stack
- programmer
- analytics
- cyber security
- saas
- startup
- tech
- computer science
- information technology