# Data asset schema

`.project_os/indexes/assets.tsv` mirrors concise asset rows and should stay compatible with root `DATA_ASSETS.md`.

Header:

```text
asset_id	kind	path	version	source_url	source_note	immutable	status	registered_at	notes
```

Rules:

- Do not infer provenance from filenames alone.
- Mark unclear sources as `provenance_unknown` rather than guessing.
- Raw/reference assets are immutable by default.
- Derived outputs belong in run directories.
- If an asset has a large or external path, record the source and access rule; do not copy by default.
