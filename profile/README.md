# modus-lisp

### Sovereign computing for the infinite zero-day future.

Advanced AI is collapsing the cost of attack. It reads, explains, and exploits
opaque systems faster than any human — turning every codebase into a field of
discoverable zero-days. Obscurity was always a weak defense. Against an attacker
who can make the opaque legible on demand, it is no defense at all.

So we invert it. If legibility is what AI hands the attacker, then **build what is
already legible** — small, readable, auditable down to the metal — and the
advantage flips back to the defender. There is no hidden ground left to uncover,
and whoever built the system understands it most cheaply of all. **A system you
can fully read is a system you can fully defend.**

modus-lisp is that bet: a stack with no opaque layers, written in a language that
explains itself.

## The stack

**[modus](https://github.com/modus-lisp/modus)** — bare-metal Common Lisp for
sovereign computing. The substrate: a Lisp that runs the projects below it, with
nothing opaque underneath.

**[cl-consensus](https://github.com/modus-lisp/cl-consensus)** — a clean-room
Bitcoin full node + HD wallet, from scratch. The consensus rules, the Script
interpreter, ECDSA and Schnorr — re-implemented in Lisp and differential-tested to
**100% agreement with Bitcoin Core**. Wraps nothing.

**[secp256k1-fast](https://github.com/modus-lisp/secp256k1-fast)** —
dependency-free secp256k1 / ECDSA / BIP340 Schnorr. The cryptography, in the open.

**[pagetree](https://github.com/modus-lisp/pagetree)** — a pure-Lisp
copy-on-write B+tree store. Storage you can read end to end.

**[scribe](https://github.com/modus-lisp/scribe)** — first-class text rendering
from scratch: sfnt/WOFF2 parsing, CFF & variable fonts, OpenType shaping, and an
analytic gamma-correct rasterizer — verified against FreeType, HarfBuzz, and the
fontTools instancer. The letterforms, in the open.

**[brotli-pure](https://github.com/modus-lisp/brotli-pure)** — a from-scratch
Brotli codec (RFC 7932). Compression you can read end to end.

---

Common Lisp by design — image-based, interactive, inspectable, homoiconic:
legible by construction.

*Research / educational. Not audited — see each repository.*
