#!/usr/bin/env python3
"""GitHub refuses files over 100 MB and Nerthus's WebAssembly is bigger, so split it into parts and make the
start page fetch the parts and join them. Usage: split.py <version folder>"""
import sys
from pathlib import Path

PART = 80 * 1024 * 1024
d = Path(sys.argv[1])
wasm = d / "nerthus_bg.wasm"
page = d / "index.html"
old = 'const response = await fetch("nerthus_bg.wasm");'
html = page.read_text(encoding="utf-8")
if old not in html:
    sys.exit("index.html does not fetch nerthus_bg.wasm the expected way")
data = wasm.read_bytes()
n = max(1, -(-len(data) // PART))
for i in range(n):
    (d / f"nerthus_bg.wasm.part{i}").write_bytes(data[i * PART:(i + 1) * PART])
wasm.unlink()
new = (f'const response = await fetchParts("nerthus_bg.wasm.part", {n}, {len(data)});')
helper = '''// Mirror change: the WebAssembly is stored in parts (GitHub's 100 MB file limit); join them as one response.
    function fetchParts(name, count, total) {
      const parts = Array.from({ length: count }, (_, i) => fetch(name + i));
      const stream = new ReadableStream({
        async start(controller) {
          for (const p of parts) {
            const r = await p;
            if (!r.ok) {
              controller.error(new Error(`The editor could not be loaded (${r.status}).`));
              return;
            }
            const reader = r.body.getReader();
            for (;;) {
              const { done, value } = await reader.read();
              if (done) break;
              controller.enqueue(value);
            }
          }
          controller.close();
        },
      });
      return new Response(stream, { headers: { "Content-Length": String(total) } });
    }

    '''
marker = "async function fetchEditor()"
assert marker in html
html = html.replace(old, new).replace(marker, helper + marker, 1)
page.write_text(html, encoding="utf-8", newline="")
