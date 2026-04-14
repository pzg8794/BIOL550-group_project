# Methods Draft Requirements Alignment

This checklist maps the current `materials_methods_piter_draft.tex` against the course paper requirements and the subsection validation hub.

## Source documents
- Requirements: `Semester5/BIOL550/group_project/BIOL550_group_paper_requirements.md`
- Draft: `Semester5/BIOL550/group_project/mouse_new/paper/materials_methods_piter_draft.tex`
- Validation hub: `Semester5/BIOL550/group_project/mouse_new/notebooks/mouse_new_methods_validation_hub.ipynb`
- Weekly report anchors:
  - `Semester5/BIOL550/group_project/mouse_new/reports/BIOL550_Weekly_Report_Mouse_Differential_Expression_2026-03-25.html`
  - `Semester5/BIOL550/group_project/mouse_new/reports/BIOL550_Weekly_Report_Mouse_Differential_Expression_2026-04-02.html`
  - `Semester5/BIOL550/group_project/mouse_new/reports/BIOL550_Weekly_Report_Mouse_Differential_Expression_2026-04-09_GO_Methods.html`

## Requirement alignment
- Standard scientific section support: the draft is written as `Materials and Methods` prose suitable for insertion into the full paper.
- Table of samples in M&M: covered in the Data Collection stage and validated in the hub.
- Sample commands for tools used: covered in `Table~\ref{tab:command_examples}` in the draft.
- Clear workflow organization: enforced through the four-stage CRISP-style structure.
- Tool / pipeline reproducibility: each stage includes tools, checkpoint artifacts, and handoffs.
- Figure and table validation: each draft figure/table has a corresponding category block in the validation hub notebook.

## Validation hub coverage
- `fig:overall_pipeline` ↔ Overview / workflow ribbon category
- `fig:data_collection` + `tab:data_collection` ↔ Data Collection category
- `fig:data_cleaning` + `tab:data_cleaning` ↔ Data Cleaning category
- `fig:data_preparation` + `tab:data_preparation` ↔ Data Preparation category
- `fig:data_analysis`, `fig:data_analysis_selection`, `tab:data_analysis`, `tab:data_analysis_primary` ↔ Data Analysis and Interpretation category

## Notes
- Full tool citations still belong in the shared paper bibliography.
- Final Word/LibreOffice submission formatting and revision-color comment must be applied in the group draft document, not in this LaTeX source.
