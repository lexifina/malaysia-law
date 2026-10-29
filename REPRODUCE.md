# How this repository was made (Malaysia)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Laws of Malaysia portal, Attorney General's Chambers of Malaysia (lom.agc.gov.my) | <https://lom.agc.gov.my/> | 2026-10-29 | Copyright Attorney General's Chambers, Malaysia, all rights reserved (portal terms, tnc.php); free download; the repository is private |
| Laws of Malaysia portal, Attorney General's Chambers: Act 709 reprints (2023, 2026) and Act A1727 | <https://lom.agc.gov.my/principal.php?type=updated> | 2026-10-29 | Copyright Attorney General's Chambers, Malaysia, all rights reserved (portal terms); reprints published by the Commissioner of Law Revision under the Revision of Laws Act 1968; Act A1727 printed by Percetakan Nasional Malaysia Berhad (publisher's copyright, all rights reserved) |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `federal-constitution` | Federal Constitution | 5 | 2020-10-15 to 2025-11-30 |
| `personal-data-protection-act` | Personal Data Protection Act 2010 [Act 709] | 4 | 2013-11-15 to 2025-06-01 |

The build made 10 commits:

| Commits | Kind |
| ---: | --- |
| 2 | first version of an act |
| 7 | one law on its in-force day |
| 1 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 6 laws in the record.
- 15 tags.

## Dates

Each commit is dated at noon (Asia/Kuala_Lumpur) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Interpretation Acts 1948 and 1967 [Act 388], s. 19(1): "The commencement of an Act or subsidiary legislation shall be the date provided in or under the Act or subsidiary legislation or, where no date is so provided, the date immediately following the date of its publication in pursuance of section 18." https://lom.agc.gov.my/ilims/upload/portal/akta/outputaktap/16312_BI/Act 388 (Muktamad).pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `93986c9ad4ef9abc5c3ea26515e53c5832235a039dd54e477c69bb8b175ac6fc` (756282 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

9 versions of 2 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- English is built: the Attorney General's Chambers publish English reprints of the Federal Constitution and principal Acts; Malay (Rumi) texts exist alongside and are not built. No Jawi text is used.
- Federal Constitution: only the 2020 and 2025 reprints are online in English (the 2006 and 2010 reprints are Malay only), so the history starts at the Reprint as at 15 October 2020, credited to the publisher as the oldest version available.
- Each change between the two reprints is credited to the amending Act and dated by the in-force day the 2025 Reprint's NOTES give for that provision; the NOTES name every changed provision.
- The 2020 Reprint prints Act A1603 section 3's words in Article 119 (voting age eighteen; "is registered" as an absent voter) although its footnotes say they were not yet in force; for 15 October 2020 to 14 December 2021 the words the footnotes say they replaced ("twenty-one years", "applies for registration") are read instead.
- Article 160 changed twice: Act A1642 (11 February 2022) inserted "Malaysia Day" and replaced "the Federation"; Act A1663 (5 October 2022) inserted "political party". The text between those days is the 2025 text without the "political party" definition, which the NOTES say A1663 inserted.
- Act A1663: the portal's list says section 6 (the Eighth Schedule) commenced on other days in some States (P.U. (B) 596/2022, 8 December 2022; P.U. (B) 282/2023, 24 July 2023), and the 2025 Reprint's list of amendments says "except s.6 (see ss. 1(3))"; its NOTES date both Eighth Schedule changes 5 October 2022 (P.U. (B) 476/2022), and that day is used.
- Act A1656 (royal assent 31 May 2022) put Article 119A in force from 15 December 2021, before it was enacted; the in-force day is kept.
- Acts A1752 and A1767 (2025) are not yet in force; the 2025 Reprint does not incorporate them (its footnotes say "has been amended by ..., not yet in force"), and they are not applied.
- Layout: running heads, NOTES pages and 8 pt footnotes are dropped, with their asterisk markers; small capitals are read as capitals; the Eleventh Schedule's table head "Section Subject Matter", repeated on each page, is dropped. Provisions whose words are the same in both reprints use the 2025 line breaks throughout.
- Two differences between the reprints that no Act explains (Second Schedule Part II s. 1(3) comma; Sixth Schedule "I,") are committed as unexplained on 30 November 2025, the 2025 Reprint's date.
- PDPA: the First Reprint as at 1 July 2023 lists no amended sections ("- NIL -"), so its text is taken as the Act as enacted and dated from commencement, 15 November 2013 (P.U. (B) 464/2013, from the portal's list of principal Acts); the portal's copy of the original Act could not be read. The long title and enacting words before Part I are not included.
- PDPA: Act A1727 is applied on the days the 2026 Reprint's LIST OF SECTIONS AMENDED gives per section (1 January, 1 April, 1 June 2025). Sections not in that list differ only by the general amendment of A1727 s. 2 ("data user(s)" -> "data controller(s)"; parse checks this word for word) and go on its day, 1 April 2025. A1727 s. 7 changes only the national language text (s. 16(3)) and so nothing here.
- PDPA: the 2026 Reprint's editorial NOTE quoting A1727 s. 14 (saving), printed under s. 146, is left out; A1727 s. 14 is not a provision of Act 709.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code with Claude Opus 5.5 (claude-opus-5-5) wrote Lexifina's code, chose the sources and acts and read the reprints' NOTES to list which provisions each amending Act changed and when. It wrote no legal text: every line of law comes from a reprint PDF. The code runs no model.
- Claude Code with Claude Opus 5.5 (claude-opus-5-5) wrote Lexifina's code and read Act A1727 and the reprint's lists to map each change to its day. No model wrote legal text.
