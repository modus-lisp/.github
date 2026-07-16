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
explains itself. Each piece is clean-room and **no-FFI** — no C, no OpenSSL, no
libgit2, no V8 underneath. And each composes on the ones below it, so the whole
tower stays legible from the metal up.

## The substrate

**[modus](https://github.com/modus-lisp/modus)** — bare-metal Common Lisp for
sovereign computing. A Lisp that runs the projects below it, with nothing opaque
underneath.

## Cryptography

**[natrium](https://github.com/modus-lisp/natrium)** — the NaCl/libsodium
primitive set, from scratch: SHA-2/HMAC/HKDF, ChaCha20-Poly1305, X25519, Ed25519.
Constant-time, RFC/NIST/Wycheproof-gated. The crypto floor everything above stands on.

**[seal](https://github.com/modus-lisp/seal)** — a clean-room TLS 1.3 + 1.2
client: AES-GCM, ChaCha20-Poly1305, X25519, and RSA/ECDSA/Ed25519 certificate
validation over a pluggable transport. No OpenSSL.

**[secp256k1-fast](https://github.com/modus-lisp/secp256k1-fast)** —
dependency-free secp256k1 / ECDSA / BIP340 Schnorr with x86-64 field arithmetic.
The Bitcoin curve, in the open.

## Networking

**[cl-transport](https://github.com/modus-lisp/cl-transport)** — uniform outbound
transport: dial direct, through SOCKS5, or a pluggable backend. One interface, any
path out.

**[cl-tor](https://github.com/modus-lisp/cl-tor)** — a from-scratch Tor client:
ntor circuits, directory validation, SOCKS5, and a v3 onion-service client.
Clean-room — no C-tor, no Arti.

**[conch](https://github.com/modus-lisp/conch)** — a from-scratch SSH-2 client
*and* server: curve25519 KEX, ed25519/RSA/ECDSA host keys, publickey auth, exec +
scp + SFTP. Crypto from natrium + seal, validated against OpenSSH. No libssh.

**[cairn](https://github.com/modus-lisp/cairn)** — a from-scratch git: object
model, packfiles, index, clone/checkout/commit/status/diff, and push/fetch/pull
over HTTPS (seal) and SSH (conch). Validated against real git. No libgit2, no
libcurl.

## Compression

**[brotli-pure](https://github.com/modus-lisp/brotli-pure)** — a from-scratch
Brotli codec (RFC 7932): full decompressor + entropy-coding compressor.

**[zstd-pure](https://github.com/modus-lisp/zstd-pure)** — a from-scratch
Zstandard codec: Huffman + FSE, LZ77, XXH64. Differential-tested byte-for-byte
against libzstd.

## Storage & consensus

**[pagetree](https://github.com/modus-lisp/pagetree)** — a pure-Lisp
copy-on-write B+tree store. Crash-safe, no FFI/mmap. Storage you can read end to end.

**[cl-consensus](https://github.com/modus-lisp/cl-consensus)** — a clean-room
Bitcoin full node + HD wallet, from scratch. The consensus rules, the Script
interpreter, ECDSA and Schnorr — differential-tested to **100% agreement with
Bitcoin Core**. Wraps nothing.

## Rendering

**[scribe](https://github.com/modus-lisp/scribe)** — first-class text rendering
from scratch: sfnt/WOFF2, CFF & variable fonts, OpenType shaping, and an analytic
gamma-correct rasterizer — verified against FreeType, HarfBuzz, and the fontTools
instancer.

**[weft](https://github.com/modus-lisp/weft)** — a from-scratch web rendering
engine: HTML/CSS parsing, the cascade, layout, and a truecolor rasterizer.
**Acid2 pixel-perfect, Acid3 100/100.**

## Runtimes & agents

**[shuttle](https://github.com/modus-lisp/shuttle)** — a Lisp-native JavaScript
engine, clean-room: source → bytecode → stack VM. **88% of test262** — including
BigInt, Proxy, generators/async, full Temporal, and Intl. No V8.

**[operandi](https://github.com/modus-lisp/operandi)** — a Lisp-native ReAct agent
loop, "Claude Code in Common Lisp." A local or frontier model drives a tool-calling
loop over files, shell, web, and **live Lisp eval in the running image** —
architected for self-improvement.

---

Common Lisp by design — image-based, interactive, inspectable, homoiconic:
legible by construction.

*Research / educational. Not audited — see each repository.*
