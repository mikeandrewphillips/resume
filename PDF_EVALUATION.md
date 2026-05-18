# Resume PDF Evaluation & Changes — May 17, 2026

## What changed in this pass

### Template
- **Dropped the "Last Updated on …" stamp** from the Deedy one-pagers (was rendering as a faint draft-watermark in the top-right corner).

### `resume.yaml`
- **Address → city/state only** (`"Champaign, IL"`). Full street address removed for privacy/recruiter-norms.
- **All dates → en-dash** (`Jan 2021 – Dec 2023`). Previously a mix of hyphen-minus and U+2010 was rendering inconsistently across the document.
- **Split Languages and Coursework into two technology groups.** Previously `"Courses taken while at Auburn:"` appeared as a fake bullet inside the Languages list. The Coursework group is tagged `[extended, academic]` so it shows on the Full CV only and is hidden from one-pagers.
- **MikroTik label → "MikroTik (lapsed)"**, and the `(expired 2024)` suffix on the inline cert list dropped. Cleaner, more honest, less visually noisy.
- **Two safe bullet rewrites:**
  - SSE "Mentored juniors and peers across the org; formally participated in the young professional development program" → **"Mentored junior and peer engineers across the org through the company's young-professional development program"** (removes "formally participated" without losing the program reference).
  - Wolfram PM "Led or coordinated 20-35 hours of meetings weekly with frequent C-level interaction" → **"Ran the weekly operational cadence, including standing C-level program reviews"** (the original framed time-in-meetings as the achievement; the rewrite reframes around the cadence and the C-suite touchpoint).

### Tag changes (affecting which variants show which bullets)
- **Closed the Product variant's 2-year SE II gap.** Added `product` tag to the GitHub-App, ElastiCache, and repo-migration bullets. The SE II role now appears on Product with three legitimate program-delivery bullets, eliminating the visible May 2022 → Sep 2024 gap.
- **Filled out the Networking variant** (which was ~40% whitespace). Added `networking` to four `extended`/`early`-only bullets that genuinely belong on a networking resume: Wolfram Network Sys Admin Wi-Fi rollout, Cisco/Extreme/MikroTik/Ubiquiti equipment management, Pavlov network-architecture documentation, and Wolfram vulnerability assessments.

## What still needs input from you (cannot do without facts)

These are the items from the original evaluation that I held off on rather than fabricate. Each one is a single-line YAML edit once you provide the number/fact.

### 1. Add quantification to the top bullets — biggest single lift
For each, even a rough number transforms it. I need you to fill in:
- **Grainger EM bullet:** team size, # of pipelines under management, # of repos served. ("Lead a team of N engineers within Platform Engineering, optimizing CI/CD pipelines across ~M repositories…")
- **SE II migration bullet:** the actual number (`100s` is informal). 350+? 500+? Also: did the migration reduce build times, infra cost, or duplicate-tooling? Any percentage you remember would land.
- **GitHub App / ElastiCache bullets:** anything quantitative — # of policies enforced, # of teams using it, $ or build-hours saved, violation reduction %.
- **Wolfram Sys Cmd Manager:** uptime SLO, MTTR, # of tickets/year, # of incidents handled, scope ($/year of infra under your watch).
- **TRYAD CubeSats:** scope beyond the $893K budget — # of subsystems, deliverables shipped, design-review outcomes.

### 2. The Grainger EM second bullet is fluff
Current: "Drive innovation, reliability, and cross-team collaboration across developer-platform initiatives." I left it because removing it would shrink the EM section to one bullet. Two replacement options once you give me a concrete fact:
- A specific initiative you led ("Led the rollout of X to Y teams, reducing Z by N%").
- A scope/ownership statement ("Own platform initiatives across N developer teams, including [specific named program]").

### 3. The Networking variant's lead-of-page misalignment
The current Grainger EM bullet ("CI/CD pipelines, GitHub Actions, SonarQube…") opens every variant including Networking, where it doesn't fit the audience. Cannot fix without a new EM-era bullet that has a networking-relevant framing. If your current platform work touches networking/infrastructure scope (it likely does — service mesh, ingress, infra reliability, …), one such bullet tagged `[overview, networking, product]` would solve this.

### 4. Wolfram chronology gap on Standard variant
The Aug 2018 → May 2019 Network Systems Administrator role doesn't appear on the standard one-pager. I tried adding a bridge bullet via the `overview` tag, but every bullet pushed the resume to two pages (the Deedy minipages flip the whole construct to page 2 when they overflow). Options when you have time:
- Decide a bullet to drop from the Standard so the bridge bullet can be added.
- Trim a one-line `overview` bullet that's worth more than the bridge.
- Accept the gap (it's a 9-month gap inside a single employer, which is usually fine).

### 5. Full CV still 4 pages with a sparse page 4
Page 4 holds only `Publications`. To force it onto page 3, either: (a) tighten Technology and shrink `\parskip` in `templates/cv.tex.j2`, or (b) accept it. Not breaking, but a 3-pager reads more confidently. Want me to take a shot at the template tweak?

### 6. Parkland teaching bullet
"Brought industry experience and mentoring into the classroom" is vague. Either drop it or replace with something concrete (course enrollment, % student pass rate on A+, etc.). Only appears on the Full CV.

### 7. Education has zero differentiation
On the Full CV: no GPA, honors, capstone, relevant coursework. If any are competitive, worth adding for the CV (not for one-pagers).

## Verified outputs (rebuilt and re-read this session)

| Variant | Pages | Status |
|---|---|---|
| `resume.pdf` (standard) | 1 | Same density as before, cleaner header, en-dashes, MikroTik (lapsed) |
| `MichaelPhillips_Networking.pdf` | 1 | **No longer ~40% whitespace** — added 4 networking bullets that were previously hidden |
| `MichaelPhillips_Product.pdf` | 1 | **SE II gap closed** with 3 product-tagged bullets; meeting-hours bullet reframed |
| `MichaelPhillips_FullCV.pdf` | 4 | All variants of the YAML fixes are visible; page 4 still sparse |

Also fixed a portability bug in `build.py`: the cleanup of `.aux/.log/.out` files now tolerates `PermissionError`, which the macOS bind-mount in some sandboxes returns even though `missing_ok=True` is set.
