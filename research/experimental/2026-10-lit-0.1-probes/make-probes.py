"""Build PROBE fixtures (not upstream, not part of lit-core) for gaps without a derived fixture.

Source: unmodified `examples/novel` from this repository (LIT 0.1.0). Source files are only read.
"""
import json
import pathlib
import shutil

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "examples" / "novel"
OUT = pathlib.Path(__file__).resolve().parent / "probe-fixtures"


def load():
    return {
        n: json.loads((SRC / f"{n}.json").read_text(encoding="utf-8"))
        for n in ["project", "components", "canon", "provenance", "rights"]
    }


def write(name, docs, extra=None, layout=None):
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for n, doc in docs.items():
        p = d / (layout or {}).get(n, f"{n}.json")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for rel, data in (extra or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


# P1 uncovered component (rights grant omits chapter:signal)
docs = load()
docs["rights"]["grants"][0]["assets"] = ["chapter:arrival"]
write("uncovered-component", docs)
# P2 canon subject/object/evidence/scope that resolve to nothing in the bundle
docs = load()
a = docs["canon"]["assertions"]
a[0]["subject"] = "character:nobody"
a[0]["evidence"] = ["chapter:does-not-exist"]
a[1]["object"] = "place:nowhere"
a[1]["scope"] = ["branch:unknown"]
write("canon-unresolved-entities", docs)
# P3 language tag / media type that match the schema patterns but are not BCP 47 / IANA registered
docs = load()
c = docs["components"]["components"]
c[0]["language"] = "qqqqq-zz"
c[0]["content"]["mediaType"] = "text/x-not-registered"
docs["project"]["language"] = "english"
write("unregistered-language-media-type", docs)
# P4 manifests relocated under manifests/ via project.json (allowed by §2)
docs = load()
for n in ["components", "canon", "provenance", "rights"]:
    docs["project"][n] = f"manifests/{n}.json"
write(
    "relocated-manifests",
    docs,
    layout={n: f"manifests/{n}.json" for n in ["components", "canon", "provenance", "rights"]},
)
# P5 remote content href
docs = load()
c = docs["components"]["components"][0]["content"]
del c["inline"]
c["href"] = "https://example.org/remote/arrival.md"
write("remote-content-href", docs)
# P6 CRLF + BOM manifests (same JSON values as novel)
docs = load()
d = OUT / "crlf-bom"
if d.exists():
    shutil.rmtree(d)
d.mkdir(parents=True)
for n, doc in docs.items():
    (d / f"{n}.json").write_bytes(
        b"\xef\xbb\xbf"
        + (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").replace("\n", "\r\n").encode("utf-8")
    )
# P7 large integer inside an extension (no duplicate key) - JS precision only
docs = load()
docs["canon"]["extensions"] = {"https://example.org/ext/probe/v0": {"bigId": 12345678901234567890}}

write("big-integer-extension", docs)

print("ok", sorted(p.name for p in OUT.iterdir()))
# P8 rights.json without litVersion
docs = load()
del docs["rights"]["litVersion"]
write("missing-litversion", docs)
