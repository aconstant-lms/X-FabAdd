# Chapter 02 slides: which file is what

| File | What it is |
|---|---|
| `02_technology_polymer.pdf` / `.pptx` | **Current** polymer session (55 slides): processes, prices, box, clocks, interface, six physical laws, maturity index, exercise "Polymer AM 2022 → 2026", references. The debrief with the exercise answers (part 9) is left out on purpose: it is in the claude.ai deck only. |
| `02_technology_metal.pdf` / `.pptx` | **Current** metal session (39 slides): LPBF, DED powder, WAAM, cold spray (animations), binder jetting, box, clocks, interface, five physical laws for metals, machines, powders and makers, references. |
| `02_technology_unused.pdf` / `.pptx` | Slides set aside (28): traditional technologies, other AM processes, parked slides. |
| `02_technologies_old_2026-11-09.pptx` | First PowerPoint version (52 slides, 9 Nov 2026), kept for reference only. |

## Direct downloads (click: the file itself downloads)

| Deck | PDF | PowerPoint |
|---|---|---|
| Polymers | [02_technology_polymer.pdf](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_polymer.pdf) | [02_technology_polymer.pptx](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_polymer.pptx) |
| Metals | [02_technology_metal.pdf](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_metal.pdf) | [02_technology_metal.pptx](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_metal.pptx) |
| Set aside | [02_technology_unused.pdf](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_unused.pdf) | [02_technology_unused.pptx](https://github.com/aconstant-lms/X-FabAdd/raw/main/02_technologies/slides/02_technology_unused.pptx) |

Do not right-click a file name in GitHub's file list and "Save link as": that saves GitHub's web page
(about 200 KB) under the file's name, and it will not open. Use the links above, or open the file
on GitHub and press the download button (↓, "Download raw file") at the top right.

The PDFs also open directly on GitHub. The PowerPoints show each slide as a picture with the speaker
notes; to change a slide, edit the claude.ai deck and export again:

```bash
cd 02_technologies/slides/claude_deck
python gen_technology_decks.py build    # slides from the generators
python export_decks.py                  # -> ../02_technology_*.pdf and .pptx
```

Editable decks (claude.ai): polymers https://claude.ai/artifact/QUfFAekdYybxee5PVWWPAF ·
metals https://claude.ai/artifact/Jre7zVeP4jn9DWpsZQVyVf ·
set aside https://claude.ai/artifact/92KDPMDHVf63xrDNPEGhwJ
