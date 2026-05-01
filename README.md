# belief_set

`belief_set` is a small Python package for finite formal belief sets and
belief-revision kernels.

The package uses a flat layout:

```text
belief_set/
tests/
```

It does not know about propstore claims, sources, contexts, sidecars,
repositories, provenance graphs, worldlines, or CLI policy.

## Paper Assets

Processed paper notes and metadata belong in `papers/` when they specify
package-owned formal algorithms. Source PDFs and rendered page PNGs may be
present in the working tree for local paper reading, but they are intentionally
ignored by Git and are not tracked package artifacts.
