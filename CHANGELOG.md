# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning:
https://semver.org/

---

## [0.1.0] – Initial Release

### Added
- Kanji decomposition engine based on Unihan CJKVI IDS data
- Recursive IDS tree resolution with cycle protection
- Kangxi radical dataset integration
- Radical variant normalization and canonical radical indexing
- Bidirectional dictionaries:
  - kanji → components / radicals
  - radical → kanji usage
- Structural kanji complexity metrics:
  - tree depth
  - total node count
  - leaf count
  - distinct radical count
  - average branching factor
- Normalization of metrics across the full corpus
- RPG-oriented difficulty score based on normalized metrics
- Difficulty class mapping (tutorial → legendary)
- ASCII tree visualization for kanji decomposition
- Public Python API for querying kanji data and metrics
- LRU caching for performance-critical API calls
- Logging support for debugging and analysis
- Initial unit test suite covering:
  - parsing invariants
  - metric consistency
  - API behavior
  - RPG score bounds

### Notes
- This is the first public and usable version of the engine.
- The public API is considered stable for exploratory and gameplay use,
  but may evolve in future 0.x releases.

