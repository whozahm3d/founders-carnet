# Corpus manifest

Columns mirror the `corpus_document` table (data dictionary, module 5). Files are committed in `rag/data/`. See `docs/context/corpus.md` for the rules.

`retrieved_at` is blank where the date was not recorded. Only the two web pages have a known access date (2026-10-04). `is_active` is true for every row.

| file | title | issuing_body | document_type | source_url | effective_date | consolidation_date | retrieved_at | content_sha256 | scope_note | is_active |
|---|---|---|---|---|---|---|---|---|---|---|
| `Income Tax Ordinance 2001, amended to 30 Jun 2026 (FBR).pdf` | Income Tax Ordinance, 2001 | FBR | statute | <https://download1.fbr.gov.pk/Docs/2026724177725705IncomeTaxOrdinanace2001.pdf> | 2026-06-30 |  |  | `1b611d31c667107a65d3d47a97e163df2ee8ba403952930f527db11d40b32c8b` | 839 pages. Amended up to 30 Jun 2026. Covers s.2(62A), s.154A and Division IVA of Part III of the First Schedule. | true |
| `Finance Act 2026, gazette of 26 Jun 2026.pdf` | Finance Act, 2026 | FBR (Gazette of Pakistan) | statute | <https://download1.fbr.gov.pk/Docs/20266291261044366FinanceAct2026.pdf> | 2026-07-01 |  |  | `49ad283594c4d1cb015fe224d3a5a126b0742bb1e416cf11089aef01df5cb124` | 256 pages. Gazette of 26 Jun 2026. Amendments in force from 1 Jul 2026. | true |
| `Companies Act 2017, updated 18 Aug 2022 (SECP).pdf` | Companies Act, 2017 | SECP | statute | <https://www.secp.gov.pk/document/the-companies-act-2017-updated-18-aug-2022/?wpdmdl=45422> |  | 2022-08-18 |  | `55243877bb5121239167d86cea335c2509b9e1aec91f3b9d0176cb0a7b1e715b` | 418 pages. Index Parts I and IV and sections 462 to 473 only. | true |
| `Seventh Schedule, fees from 20 Apr 2026 (SECP).pdf` | Seventh Schedule (fees) | SECP | fee schedule | <https://www.secp.gov.pk/document/seventh-schedule-updated-till-20-04-2023-2/?wpdmdl=47657> | 2026-04-20 |  |  | `7393e74c7266c0fcf3c8f1a5968e446cb1b29588dad916d928bd79f3a706b7e1` | 13 pages. Fees effective 20 Apr 2026 (page 1: W.E.F 20th April, 2026). The URL slug says 2023; the file is the 2026 version. | true |
| `Regulatory Sandbox Guidelines 2019 (SECP).pdf` | Regulatory Sandbox Guidelines, 2019 | SECP | guidelines | <https://www.secp.gov.pk/document/secp-regulatory-sandbox-guidelines-2019/?wpdmdl=37476> | 2019 |  |  | `d20a8f8bf6cb9dee1b5a7b46539ce1fb9342884310960b9a5f118493dac45208` | 8 pages. | true |
| `Start-up ecosystem position paper, 30 Oct 2024 (SECP).pdf` | Start-up ecosystem position paper | SECP | position paper | <https://www.secp.gov.pk/document/rsb-position-paper/> | 2024-10-30 |  |  | `e1e6b77cd4d071d60c04184a78f3b3267ffd037abc7747c3823cbb3c9ae63b1c` | 28 pages. Dated 30 Oct 2024 (the press release says 31 Oct). | true |
| `Virtual One Stop Shop circular, 27 Mar 2018 (FBR).pdf` | Virtual One Stop Shop (VOSS) for company registration | FBR | circular | <https://download1.fbr.gov.pk/Docs/20194121643945673VirtualOneStopShop(VOSS)forCompanyRegistration.pdf> | 2018-03-27 |  |  | `87a382f52bc2150468adbaa938318e196ea62d28b141ad5022a02d5cb7884ef9` | 1 page, scanned. Needs OCR or hand transcription before indexing. | true |
| `Registration of Individual on Iris, 25 May 2019 (FBR).pdf` | Registration of Individual on Iris | FBR | guide | <https://download1.fbr.gov.pk/Docs/2019527755039915Registrationofindividualoniris.pdf> | 2019-05-25 |  |  | `0d638627f083874da145da4c6897fe053dcf6942cf5284214534aa924f035269` | 6 pages. Individual registration steps only. | true |
| `Iris FAQs (FBR).pdf` | Iris FAQs | FBR | FAQ | <https://e.fbr.gov.pk/SOP/IRIS/Iris_FAQs.pdf> | 2023-01-20 |  |  | `77569f40981d3ea98f1ac09ce9fee155be9894aaa2bfd288b18cb11ad6d4eb5d` | 14 pages. File dated 20 Jan 2023. Registration and e-enrollment questions only. | true |
| `PSEB Industry Facilitation page.pdf` | Industry Facilitation (PSEB) | PSEB | web page | <https://techdestination.com/industry-facilitation/> | 2026-08-19 |  | 2026-10-04 | `d62021ad55bce427ea13d436d581337c8c3b31ccd51cc4edfc292861ec9cbe4e` | 7 pages, 876 words. Accessed 4 Oct 2026, last modified 19 Aug 2026. Registration documents, fees and renewal only. Strip the tax sections before indexing. | true |
| `fbr_register_income_tax_2026-10-04.html` | Register for income tax (FBR web page) | FBR | web page | <https://www.fbr.gov.pk/categ/register-income-tax/51147/30846/%2071150> |  |  | 2026-10-04 | `d44a7b18d877d4241d54f6f98585eabea1d48d8497346476f78188cb50f239cc` | 615 words, undated. Accessed 4 Oct 2026. Snapshot saved as html and txt. | true |
| `fbr_register_income_tax_2026-10-04.txt` | Register for income tax (FBR web page, text copy) | FBR | web page | <https://www.fbr.gov.pk/categ/register-income-tax/51147/30846/%2071150> |  |  | 2026-10-04 | `fd70b4eb059e0c4e4e0b9356ffbffbf53f9054047e316549c2b0de02a2623982` | Text copy of the html snapshot above. Index one of the two, not both. | true |

## Check

Run `python rag/corpus_profile/profile_corpus.py` and compare its SHA-256 values with the `content_sha256` column. They matched on 2026-10-16 (the `.txt` copy is not in the profile report; its hash was computed directly). A different hash means a different file version: stop and tell the team.

## Not in the corpus

- Iris login manual (excluded).
- 2015 Urdu guide (excluded).
- Companies Regulations 2024 (still being considered).
