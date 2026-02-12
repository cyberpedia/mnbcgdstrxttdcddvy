# PDF Export Guide (Export-ready)

The Cerberus docs are written in Markdown and structured for PDF export.

## Documents

- `user-guide.md`
- `admin-guide.md`
- `challenge-author-guide.md`
- `api-reference.md`
- `deployment-maintenance-guide.md`
- `security-best-practices.md`

## Recommended export options

### Option A: Pandoc
```bash
pandoc cerberus/docs/user-guide.md -o cerberus/docs/user-guide.pdf
```

### Option B: Batch script
Use:
```bash
./cerberus/scripts/export-docs-pdf.sh
```

## Notes

- Ensure a PDF engine is installed (`wkhtmltopdf` or LaTeX engine).
- Use consistent heading hierarchy for generated TOC.
- Keep code fences for API examples to preserve formatting in PDF.
