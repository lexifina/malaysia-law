# Structure

| Folder | What it holds |
| --- | --- |
| `constitution/` | The Federal Constitution, one file per Article (`art-160.md`), Part heading and Schedule |
| `acts/<year>/<number>-<slug>/` | A principal Act of Parliament by the year in its title (or, for a Code with no year, the year it was first enacted) and its Act number in the Laws of Malaysia, e.g. `acts/1950/136-contracts/` (Act 136), `acts/1936/574-penal-code/` |
| `acts/<year>/a<number>-<slug>/` | An amending Act as enacted, e.g. `acts/2025/a1750-penal-code-amendment/` (Act A1750) |

Each folder holds one file per section (`s-012.md`; `s-005-a.md` is section 5A), the schedules (`schedule-1.md`),
and a `README.md` with the source and the provisions. No folder holds more than 1,000 entries.

## Dates

Each version is one commit, dated 12:00 Asia/Kuala_Lumpur on the day it took effect, which its `In-force:` trailer
repeats; `In-force-basis:` says where that day comes from:

- `reprint-latest-amendment`: a reprint of the Commissioner of Law Revision, on the day page 2 of the reprint says
  its latest amendment came into operation;
- `reprint-as-at` / `reprint-amendments-up-to`: a reprint that names no latest amendment, on the day it says it
  is "As at" or incorporates all amendments up to;
- `commencement-provision`: an Act as enacted, on the day it names itself;
- `portal-commencement`: an Act on the single commencement day the Laws of Malaysia portal lists for it.

Acts brought into force on several days or by a notice not yet in the list, PDFs without a text layer (no OCR is
run) and Acts whose sections could not be found in order are held back. A reprint consolidates the amendments
before its day and is credited to the reprint, not to an amending law. No date in this repository is the day we
downloaded anything.
