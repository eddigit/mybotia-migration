#!/usr/bin/env python3
"""Push password protection middleware to mvp-igh repo via GitHub API."""
import json, urllib.request, sys

TOKEN = "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"
REPO = "eddigit/mvp-igh"
API = f"https://api.github.com/repos/{REPO}"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"}

MIDDLEWARE = '''import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const authHeader = request.headers.get("authorization");
  if (authHeader) {
    const [scheme, encoded] = authHeader.split(" ");
    if (scheme === "Basic") {
      const decoded = atob(encoded);
      const [user, pass] = decoded.split(":");
      if (user === "igh" && pass === "IGH-Demo2026!") {
        return NextResponse.next();
      }
    }
  }
  return new NextResponse("Accès protégé", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="Accès restreint"' },
  });
}

export const config = { matcher: ["/((?!_next|favicon.ico).*)"] };
'''

def api(path, data=None):
    url = f"{API}/{path}" if not path.startswith("http") else path
    req = urllib.request.Request(url, headers=HEADERS)
    if data:
        req.data = json.dumps(data).encode()
    return json.loads(urllib.request.urlopen(req).read())

# 1. Get current main ref
ref = api("git/ref/heads/main")
base_sha = ref["object"]["sha"]
print(f"1. Base commit: {base_sha}")

# 2. Get base tree
commit = api(f"git/commits/{base_sha}")
base_tree = commit["tree"]["sha"]
print(f"2. Base tree: {base_tree}")

# 3. Create blob
blob = api("git/blobs", {"content": MIDDLEWARE, "encoding": "utf-8"})
print(f"3. Blob: {blob['sha']}")

# 4. Create tree
tree = api("git/trees", {
    "base_tree": base_tree,
    "tree": [{"path": "middleware.ts", "mode": "100644", "type": "blob", "sha": blob["sha"]}]
})
print(f"4. Tree: {tree['sha']}")

# 5. Create commit
new_commit = api("git/commits", {
    "message": "URGENT: Add password protection (Basic Auth)",
    "tree": tree["sha"],
    "parents": [base_sha],
    "author": {"name": "Gilles KORZEC", "email": "gilleskorzec@gmail.com", "date": "2026-03-30T18:00:00Z"},
    "committer": {"name": "Gilles KORZEC", "email": "gilleskorzec@gmail.com", "date": "2026-03-30T18:00:00Z"}
})
print(f"5. New commit: {new_commit['sha']}")

# 6. Update ref
req = urllib.request.Request(f"{API}/git/refs/heads/main", headers=HEADERS, method="PATCH")
req.data = json.dumps({"sha": new_commit["sha"]}).encode()
result = json.loads(urllib.request.urlopen(req).read())
print(f"6. Ref updated: {result['ref']} -> {result['object']['sha']}")
print("\n✅ DONE — Password protection pushed. Vercel will auto-deploy.")
print("Login: igh / IGH-Demo2026!")
