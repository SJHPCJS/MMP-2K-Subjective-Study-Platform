# MMP-2K Subjective Study Platform

Welcome to the hands-on portal behind **MMP-2K: A Benchmark Multi-Labeled Macro Photography Image Quality Assessment Database** (IEEE ICIP 2025). This toolkit powers the human-in-the-loop study that fuels the dataset - annotators sign in, explore carefully curated macro shots, record subjective scores, and watch their progress come alive through friendly dashboards and visualisations.

## What's Inside
- `backend/server`: a Python 3 Flask API with Flask-CORS that streams image metadata, records MOS submissions, and keeps every annotator's progress neatly organised next to the `image_base/` gallery.
- `frontend`: a Vue CLI 5 application (Vue 2.6, Element UI, axios) that guides participants from onboarding through training, main study, references, and final summaries.
- `Data/display_data`: pandas + matplotlib utilities for quick analytics using the bundled demo result file.
- Root `package-lock.json`: shared npm lockfile for reproducible front-end installs.

## Getting Ready
- Python 3.9+ with `pip`.
- Node.js 16.x (recommended for Vue CLI 5) with npm.
- Optional but helpful: a Python virtual environment dedicated to the backend and data scripts.

## Launching the Backend
1. (Optional) Activate your virtual environment.
2. Install the dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. (Optional, for visualisation scripts) add:
   ```bash
   pip install pandas matplotlib
   ```
4. From the repository root, start the API:
   ```bash
   python backend/server/backend.py
   ```
   The service listens on `http://127.0.0.1:5001` with CORS already enabled, ready for the Vue front-end to talk to it.

### Creating Annotation Accounts
Generate annotator workspaces with the helper script (run it from the repo root so paths stay consistent):
```bash
python backend/server/create_user.py
```
When prompted:
- Enter a unique user ID.
- The script appends the ID to `id.txt`, creates `backend/server/<ID>/`, and prepares `<ID>_result.json` with a shuffled mix of study images and 60 cleverly interleaved golden questions.
- Any ID listed in `id.txt` now unlocks the login screen.

## Lighting Up the Front-end
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run the dev server:
   ```bash
   npm run serve
   ```
3. Open the displayed URL (typically `http://localhost:8080/`). Sign in with one of the generated IDs to tour the intro, training flow, main annotation view, reference examples, and progress report. All requests are routed to `http://127.0.0.1:5001`.

## Visualising Study Data
Inside `Data/display_data`, `display.py` demonstrates how to translate result logs into quick insights.

- Check the JSON filename at the top of the script (the repo ships `demo_result.json`; update it if you're analysing another user).
- Execute from the repository root or the `display_data` folder:
  ```bash
  python Data/display_data/display.py
  ```
- The script produces bar charts covering images per batch, average MOS per batch, rating distribution, and factor frequencies. Saved PNGs land in the same directory for easy sharing.

## Bundled Samples
- `backend/server/image_base/`: mock macro photography assets for testing (swap with official data when ready).
- `backend/server/golden/` & `backend/server/golden_result/`: quality-control examples for golden questions.
- `Data/display_data/demo_result.json`: synthetic annotations for trial runs and plotting demos.

## About MMP-2K
- Paper: [MMP-2K: A Benchmark Multi-Labeled Macro Photography Image Quality Assessment Database](https://arxiv.org/abs/2505.19065), accepted at IEEE ICIP 2025.
- Supplementary material: https://github.com/MMP-2k/MMP-2k/blob/main/supplementary.md
- Download the official dataset:
  - https://github.com/Future-IQA/MMP-2k/releases/tag/v1.0.0
  - https://huggingface.co/datasets/MMP-2k/MMP-2k
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0).

### Authors
- [Jiashuo Chang](https://github.com/SJHPCJS)
- [Zhengyi Li](https://github.com/Zhengyi1212)
- [Jianxun Lou](https://scholar.google.com/citations?user=pPmIqeoAAAAJ&hl)
- [Zhen Qiu](https://scholar.google.com/citations?hl=en&user=uDy8DnMAAAAJ)
- [Hanhe Lin](https://scholar.google.com/citations?user=PtY7WbYAAAAJ&hl=en)

### Cite Us
> Jiashuo Chang, Zhengyi Li, Jianxun Lou, Zhen Qiu, Hanhe Lin. MMP-2K: A Benchmark Multi-Labeled Macro Photography Image Quality Assessment Database. Proceedings of the 2025 IEEE International Conference on Image Processing (ICIP), Anchorage, AK, USA. IEEE, 2025. doi:10.1109/ICIP55913.2025.11084596

```bibtex
@mmp2k{11084596,
  author={Chang, Jiashuo and Li, Zhengyi and Lou, Jianxun and Qiu, Zhen and Lin, Hanhe},
  booktitle={2025 IEEE International Conference on Image Processing (ICIP)},
  title={MMP-2k: A Benchmark Multi-Labeled Macro Photography Image Quality Assessment Database},
  year={2025},
  pages={169-174},
  doi={10.1109/ICIP55913.2025.11084596}
}
```
