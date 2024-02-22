# Vinyl

## Sources

Sources are data models that can't be modified. Sources act as the bridge between external systems (SaaS tools, databases, other Vinyl projects, etc.) and Vinyl. Sources are the only way to get data into Vinyl. Sources are comprised of 3 parts: (1) a source definition which contains fields, typing and other metadata (2) a connector which is an adapter to the system where the data is stored and (3) a fetcher which tells Vinyl how to fetch data from the connector and at what frequency.

## Most Used Commands

`vinyl sources list` - list all sources available in the project
`vinyl sources cache` - cache data from all sources into a local repository (default is .turntable/sources)

## How to load sources

```python
import vinyl

conn = vinyl.connect('local')
```

The return of connect() is an ibis connection. The first time this may be slow as each table needs to be created. Subsequent loads are cached.
