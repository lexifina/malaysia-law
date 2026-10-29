# Malaysia: law history in git

The law of Malaysia as a git history: one file per provision, one commit per amending Act on the day it came into force, and the Act that made each change as the commit's author. `git blame` names the Act behind every paragraph; `git log` lists every change to an Article; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `my/`.

The text is the **English** text of the Attorney General's Chambers' official reprints on the [Laws of Malaysia portal](https://lom.agc.gov.my). Malay is the national language and the Malay (Rumi) text is published alongside; it is not built here.

**What is in it now**

| Folder | Law | Versions | History |
| --- | --- | ---: | --- |
| `federal-constitution/` | Federal Constitution | 5 | The Reprint as at 15 October 2020 (oldest version available), then Act A1603 s. 3 and Act A1656 (Article 119, voting age eighteen, and Article 119A, both 15 December 2021), Act A1642 (Malaysia Agreement 1963 amendments: Articles 1(2), 160, 161A, 11 February 2022), Act A1663 (anti-party-hopping: Articles 10(3A), 48(6), 49A, 160, Eighth Schedule, 5 October 2022), then the Reprint as at 30 November 2025 |
| `personal-data-protection-act/` | Personal Data Protection Act 2010 [Act 709] | 4 | As enacted, in force 15 November 2013 (read from the First Reprint as at 1 July 2023, which lists no amended sections), then the Personal Data Protection (Amendment) Act 2024 [Act A1727] on its three commencement days: 1 January 2025 (ss. 67, 136), 1 April 2025 ("data user" becomes "data controller" throughout; ss. 4, 5, 9, 21, 48, 129) and 1 June 2025 (Division 1A, ss. 12A, 12B, 43A). The result equals the Reprint as at 15 September 2026 word for word |
| `penal-code/` | Penal Code [Act 574] | 4 | The updated Reprint as at 4 July 2023 (oldest version available), then the Penal Code (Amendment) Act 2024 [Act A1721] (new ss. 424A-424D, 30 October 2024), the Penal Code (Amendment) Act 2025 [Act A1750] (new ss. 507B-507G, 11 July 2025) and the Penal Code (Amendment) (No. 2) Act 2023 [Act A1691] (ss. 305 and 306 substituted, s. 309 deleted, 10 September 2025), each applied from its official text. Not yet compared with a later consolidation (none is online in English) |

Each folder's `README.md` lists every provision, how often it changed and when. Files: `federal-constitution/art-049a.md` is Article 49A; `part-04-chapter-06.md` is the heading of Part IV, Chapter 6; `sch-08.md` is the Eighth Schedule (one file per Schedule).

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did Article 119 say on 1 January 2021? | `python tools/on.py 2021-01-01 federal-constitution art-119` |
| Which Act gave Article 119 its wording on a date | `python tools/on.py --law 2022-01-01 federal-constitution art-119` |
| The whole Constitution on a date | `python tools/on.py 2022-06-01 federal-constitution` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2021-01-01T23:59:59Z" main -- federal-constitution/art-119.md):federal-constitution/art-119.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2021-01-01T23:59:59Z" main -- federal-constitution/art-119.md; git show "$($r):federal-constitution/art-119.md"` |
| Which Act wrote each line of Article 160? | `git blame federal-constitution/art-160.md` |
| Every change to Article 160, word by word | `git log -p --word-diff federal-constitution/art-160.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one Act changed | `git show law/act-a1663` (tags `law/<key>` mark each law's commit) |
| Section 129 of the PDPA before and after 1 April 2025 | `python tools/on.py 2025-03-31 personal-data-protection-act sec-129` and the same for `2025-04-01` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Asia/Kuala_Lumpur, on the day the change came into force**. The in-force day is also in the `In-force:` trailer, which the tools read; royal assent (`Enacted:`) and Gazette publication (`Published:`) are trailers too.
- **In-force days** for the Constitution are those the 2025 Reprint's NOTES give for each provision; for the PDPA, those the 2026 Reprint's LIST OF SECTIONS AMENDED gives ("in force from 05-10-2022"). Where an Act names no day, the Interpretation Acts 1948 and 1967 [Act 388], s. 19(1), put it in force on "the date immediately following the date of its publication".
- **Act A1656** came into force on 15 December 2021 but received royal assent on 31 May 2022: its commit is dated before the Act existed, as the Act itself provides.
- **The two reprints** are dated by their own "As at" dates (15 October 2020 and 30 November 2025).
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a change that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`. The repository is rebuilt a second time from the same data and gives identical hashes.
- Health checks: no merge commits on `main`, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse with `git interpret-trailers --parse`.
- **Against the official text, read a second way** (`tools/verify.py`): every paragraph of every version (9,968 paragraph checks: 4,558 Constitution, 2,224 PDPA, 3,186 Penal Code) appears word for word in the reprint PDF read as plain page text by PyMuPDF, ignoring case (small capitals) and the page furniture between pages. 0 misses. The only two paragraphs not in the 2020 Reprint's body are the Article 119 words the reprint's own footnotes give as the text before Act A1603 section 3 came into force (see below).
- The latest version is the Reprint as at 30 November 2025 exactly as printed; the build stops if the amendments applied to the 2020 Reprint do not reproduce it, apart from the two unexplained changes listed below.

## What "author" means

The author of a commit is the Act that made the change, with an e-mail address that cannot exist (`act-a1663@agc.gov.my.invalid`), so `git blame` and `git log --author` name Acts. The committer is always Lexifina.

- **The first commit** is the oldest English text available online, the 2020 Reprint, credited to the publisher, the Attorney General's Chambers.
- **Credits come only from the source.** Each Act is credited with exactly the provisions the 2025 Reprint's NOTES say it changed, on the day they give.
- **Unexplained changes.** Two small differences between the reprints that no Act explains (a comma in the Second Schedule, Part II, section 1(3); "I," in the Sixth Schedule's Oath of Secrecy) are committed by the publisher on 30 November 2025, labelled unexplained.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see which words each change made.

## What it does not show

- **History before October 2020.** The 2006 and 2010 reprints are online in Malay only; the English reprints online are those of 2020 and 2025. The NOTES in each reprint record every earlier amendment back to 1957 with the replaced words, so a full history could be rebuilt from them; that is not done yet.
- **Article 119 in the 2020 Reprint.** The reprint prints the voting age "eighteen years" and "is registered" (absent voters) although its footnotes say those words of Act A1603 section 3 were "not yet in force". From 15 October 2020 to 14 December 2021 this repository reads the words the footnotes say they replaced ("twenty-one years", "applies for registration").
- **Act A1663, section 6.** The portal's list of amendments says section 6 (the Eighth Schedule) came into force on other days in some States (P.U. (B) 596/2022 and 282/2023); the 2025 Reprint's NOTES give 5 October 2022 for both changes, and that day is used.
- **Acts not yet in force.** The Constitution (Amendment) Act 2025 [Act A1752] (citizenship) and the Constitution (Amendment) (No. 2) Act 2025 [Act A1767] are not in force; the 2025 Reprint marks the provisions they will amend and does not incorporate them. They are not applied.
- **Changes that are not amendments.** Orders under the Constitution that change numbers without changing its words (for example the numbers of judges, P.U. (A) 163/2009) are footnotes in the reprint and are left out, as are the NOTES themselves.
- **Layout.** The reprints' running heads, NOTES pages and footnotes are left out. Small capitals are read as capitals ("Article 160A"). The table head of the Eleventh Schedule, repeated on every page, is left out.
- **PDPA:** the long title and enacting words before Part I are not included; the 2026 Reprint's editorial NOTE quoting the saving provision of Act A1727 (s. 14) is left out. A1727 s. 7 changed only the Malay text. The portal's PDF of the Act as originally gazetted answers HTTP 500, so the 2023 Reprint, which lists no amended sections, stands in for it.
- **Penal Code:** the history starts at July 2023. After that it is the three amending Acts applied to the reprint; no English reprint after July 2023 is online to check the result against. Chapter headings are `chapter-NN.md`; the centred cross-headings between sections ("Mischief") are `xh-<next section>.md`. Section 309 (attempted suicide), deleted by Act A1691, is removed.
- **State law**, subsidiary legislation and the other federal Acts are not included yet.

## How it is built


## Sources

| Source | What | Dated versions | Names the amending law | Licence | Notes |
| --- | --- | --- | --- | --- | --- |
| [Laws of Malaysia](https://lom.agc.gov.my) (Attorney General's Chambers) | Federal Constitution reprints (English 2020 and 2025; Malay 2006, 2010, 2020, 2025), amending Acts as PDFs, principal Acts as updated reprints | reprints only ("As at") | yes (NOTES per Article, with in-force days and replaced words) | "Copyright 2023 by Attorney General's Chambers, Malaysia, all rights reserved"; free download | Official. Online reprints "are not the reprinted version made pursuant to Section 14 of the Revision of Laws Act 1968"; a print-out "is NOT A COPY of the Gazette" |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

See `LICENSE` for the attribution.

## Bahasa Melayu

Repositori ini memuatkan sejarah undang-undang Malaysia dalam git: satu fail bagi setiap peruntukan, dan satu commit bagi setiap Akta pindaan pada hari ia mula berkuat kuasa. Teksnya ialah teks bahasa Inggeris cetakan semula rasmi Jabatan Peguam Negara (lom.agc.gov.my). Perlembagaan Persekutuan bermula dengan Cetakan Semula sehingga 15 Oktober 2020, diikuti Akta A1603, A1656, A1642 dan A1663, dan Cetakan Semula sehingga 30 November 2025. Repositori ini bukan nasihat undang-undang.
