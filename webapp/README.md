# Kanji Deconstruction Viewer

Static frontend (vanilla HTML/CSS/JS) that displays a kanji and lets you scroll
through its decomposition into radicals/components, one level at a time, with
a click-to-zoom detail card and a vertical depth-navigation.

## Running locally

`app.js` is loaded as an ES module, which browsers block from `file://` pages.
Serve the folder over HTTP instead, e.g.:

```bash
cd webapp
python3 -m http.server 8000
```

Then open `http://localhost:8000/index.html`.

## Current data source (temporary)

There is no backend yet. The app reads from `mock-data.js`, a fixture with
3 real kanji pulled from this project's own data files (`人` atomic, `明`
two-part, `海` three-level nested) — enough to exercise every case the UI
handles (no decomposition, flat decomposition, nested decomposition).

Once the FastAPI backend (`src/kanjidb/api/`) exists, only one place needs to
change:

- `fetchKanjiData(literal)` in `app.js` — replace the `MOCK_KANJI[literal]`
  lookup with `fetch(`/api/kanji/${literal}`).then(r => r.json())`.
- `init()` calls `setupSearch(Object.keys(MOCK_KANJI))` — replace with the
  list returned by `GET /kanji`.

No other file needs to change; the rendering and animation code only depends
on the data shape (see `mock-data.js` for the expected schema), not on where
the data comes from.

## Files

| File           | Purpose                                                    |
| -------------- | ----------------------------------------------------------- |
| `index.html`   | Page structure: search bar, info panel, decomposition stage |
| `style.css`    | All styling, dark theme                                    |
| `app.js`       | Rendering, layout, scroll animation, search wiring          |
| `mock-data.js` | Temporary fixture standing in for the real API              |
