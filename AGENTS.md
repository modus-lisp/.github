# Working in the modus-lisp workspace

This file is for anyone, person or agent, writing code in a `kiln sync` workspace:
one directory holding a checkout of every repo in the org. `kiln sync` links it in as
`AGENTS.md` and `CLAUDE.md` at the workspace root. Each repo's own `CLAUDE.md` /
`AGENTS.md` covers that repo; this one covers what is shared between them.

**The rule this file exists for: before you write an algorithm, find out whether the
org already has it.** An inventory in November 2026 found about 30 hex codecs,
22 base64 codecs, 20 UTF-8 codecs, 6 CRC-32s, 5 SHA-256s, 5 SHA-512s, 5 HKDFs,
5 bech32s, 4 SHA-1s, 4 AESs, 7 HTTP clients and 6 JSON readers. Most were written
on the spot, the slowest are up to 100x slower than the fastest, and they keep
being written because each one looked too small to look for.

## 1. Search, then delegate

**`.github/CATALOG.md`** lists every repo: what its systems say they are, what they
depend on, and every symbol each package exports. It opens with an index of names
exported by more than one repo. Grep it first, then grep the source:

```sh
# from the workspace root
grep -n "base64" .github/CATALOG.md
grep -rn "(defun sha256\b" --include=*.lisp */src
```

The catalog is generated, so don't edit it by hand. After adding or renaming exports, run
`sbcl --script .github/catalog/build.lisp` (about 2 s; nothing is loaded) and commit
the result to `.github`.

- **If the canonical home below has it, depend on that system and call it.** Don't
  copy its code into your repo. A copy misses every later fix, and that is how there
  came to be six CRC-32s.
- **If the canonical home lacks what you need, add it there**, with a test, and
  depend on it. A small dependency is fine; the systems below are leaf libraries.
- **If you really must keep a local copy** (a bare-metal image that can't load
  the dependency, say), say so in a comment naming the canonical version. Keep the
  same name and the same results, and add a test that checks the copy against the
  canonical version.

## 2. Canonical homes

| what | system | entry points |
|---|---|---|
| SHA-1, SHA-256, SHA-384, SHA-512, SHA3-256, RIPEMD-160 | `natrium` | `sha256`, `sha256-into`, `with-sha256` / `sha256-update` / `sha256-final-into` (streaming), likewise 384/512; `sha1` |
| HMAC, HKDF, PBKDF2 | `natrium` | `hmac-sha256`, `hmac-into`, `hkdf`, `hkdf-expand-into` |
| AES, ChaCha20-Poly1305, X25519, Ed25519, DRBG | `natrium` | constant-time variants; secrets live in non-moving memory (`natrium/gossamer`) |
| secp256k1, BIP340 Schnorr | `secp256k1-fast` | |
| CRC-32, Adler-32 | `cram` | `crc32`, `crc32-update` (streaming register), `adler32` |
| DEFLATE / zlib / gzip, compress and decompress | `cram` | `zlib-compress`, `zlib-decompress`, `zlib-inflate-stream` (READ/SINK, never holds the stream), `make-zstream` |
| tar | `cram` | `tar-extract`, `tar-do-entries` |
| HTTP(S) client | `seal` (`seal/http`) | `request`, `open-body-reader` (pull), `request-into` (push to a sink) |
| TLS | `seal` | |
| JSON | `json-simple` | |
| git (clone, fetch, packs, objects) | `cairn` | `fetch-pack-into`, `stream-object` |
| FAT32 | `fs-fat` | `fat32-open-output` / `-write-output` / `-close-output`, `fat32-read-into` |
| hex, base64, UTF-8 | **moving to `natrium`** | until that lands, check `natrium/src/util.lisp` and say which copy you used |

When you are about to write something that isn't in this table, check `*/src` across
the workspace for it first. If it turns out to exist in two places, add a row here.

## 3. Measure on both Lisps, with a reference check

Everything here runs on SBCL and on Modus, which has its own compiler and runtime, and
**the fastest shape is not the same on both**. Measured November 2026, MB/s:

| algorithm | implementation | SBCL | Modus |
|---|---|---|---|
| CRC-32 | slicing-by-8, beacon's copy | 1272 | 33 |
| CRC-32 | one typed table lookup per byte (cram before) | 338 | 244 |
| CRC-32 | **slicing-by-8 (cram now)** | 1311 | 384 |
| CRC-32 | bit at a time (scribe) | 7 | 0.9 |
| Adler-32 | modulo per byte (old cram) | 29 | 29 |
| Adler-32 | **deferred modulo, NMAX 5552 (cram)** | 1498 | 447 |
| inflate | bit-at-a-time Huffman (old cram) | 8.5 | 4.1 |
| inflate | **10-bit lookup table (cram)** | 12.0 | 5.2 |
| SHA-1 | natrium, before | 20 | 6.8 |
| SHA-1 | seal | 100 | 9.7 |
| SHA-1 | beacon | 67 | 26 |
| SHA-1 | **natrium, now** (seal's, unrolled, ROL on SBCL) | 181 | 11 |
| SHA-256 | natrium, before | 35 | 9.4 |
| SHA-256 | beacon (`ldb (byte 32 0)` modular arithmetic) | 75 | 5.1 |
| SHA-256 | folio | 11 | 10.8 |
| SHA-256 | cl-sev-snp | 23 | 11.7 |
| SHA-256 | **natrium, now** (beacon's compression function, ROL on SBCL) | 90 | 18.6 |
| SHA-512 | **natrium** | 133 | 11.6 |
| SHA-512 | folio | 2.8 | 0.04 |
| SHA-512 | cl-sev-snp | 5.4 | 0.04 |

ironclad, outside the org, is faster on SBCL: SHA-1 364, SHA-256 120, SHA-512 121.
That speed comes from x86-64 assembly in SBCL VOPs, which is exactly the opaque layer
this org avoids. Among Lisp implementations the bold rows are the fastest we have.

Every row above was checked against the others for the same output. **The rule when
the two Lisps disagree: take the SBCL winner.** Modus is being made comparably fast,
and its slow spots are bugs to fix in Modus, not reasons to ship a slower algorithm.
natrium now carries the SBCL winner for each hash, so call natrium.

The scripts that produced these are in `.github/bench/`. Run them from the
workspace root, for example `SYSTEMS="natrium seal" sbcl --script .github/bench/hash.lisp`,
or with `modus --script` in place of `sbcl --script`.

So:

- **Benchmark a candidate on SBCL and on Modus**, and record both numbers in the
  commit message. Choose by SBCL. When the Modus number is much worse, note it:
  that is a Modus performance bug, and a measured case to fix it with.
- **Check results against an independent implementation**: SBCL's own, or another
  library (chipz for inflate, GNU tar for tar, a known test vector). Otherwise a fast
  implementation can be wrong without anyone noticing.
- Warm up before timing on Modus. A function goes native after 64 calls or 10 ms
  of interpretation, and a single long call finishes interpreted.

## 4. What makes code slow (or wrong) on Modus

- **Declare octet vectors.** `(make-array n :element-type '(unsigned-byte 8))`. A
  generic vector costs 8 bytes per element and every access is generic.
- **No `(concatenate 'vector ...)` or `subseq` to accumulate a buffer.** Both make a
  generic vector and copy everything each time. Keep one octet buffer, with a fill
  index, and `replace` into it.
- **Type-dispatch on simple octet vectors with `typep`** (as cram's `adler-step` does),
  and keep a generic arm for everything else. `(simple-array (unsigned-byte 8) (*))`
  does not match an adjustable or fill-pointered vector. Before Modus commit 1b31f6ca
  it wrongly did, and a `(safety 0)` fast arm then read the array header as data.
  At `(safety 0)` a wrong declaration is memory corruption, not an error.
- **No per-byte generic-function dispatch.** A `defmethod` called once per byte
  costs far more on Modus than on SBCL. Dispatch once per buffer.
- **Prefer streaming.** A board has ~88 MB of semispace with ~35 MB live, and a
  copying collector needs the live set to fit in one semispace. Read with a pull
  function returning `(values buf end)` or write through a sink. Don't build the
  whole thing in memory. When writing a file in pieces, write `NAME.partial` and
  rename it over `NAME` when complete.

## 5. Before you call something slow

Compare it with a sibling first: the same algorithm in another repo, or the same code
on the other Lisp. A primitive that is slow everywhere is a fact about the primitive.
A primitive that is slow in one place is usually a fact about how it was called there.
