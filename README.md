# Policy and Terms of Service Repository

This repository serves as the **authoritative public archive** and single source of truth for all legal documents, including:

- Terms of Service  
- Privacy Policy  
- other platform-related legal agreements

By keeping these documents in a version-controlled Git repository, we provide full transparency and an immutable history of every legal commitment to be made by our users on regular conditions.

## Goals of this Repository

- **Public auditability** — anyone can verify the exact wording of any policy at any historical point  
- **Tamper-evident history** — Git commit hashes + timestamps cryptographically guarantee no retroactive changes without trace  
- **High availability & embeddability** — documents are distributed via global CDN for reliable client-side usage

### Repository Structure

```text
├── versions.json                          ← current version of each document
├── PrivacyPolicy/
│   ├── current_privacy_policy.md          ← active version (currently in effect)
│   └── Archive/
│       ├── privacy_policy_v1.md
│       ├── privacy_policy_v2.md
│       └── ...
├── TermsOfService/
│   ├── current_terms_of_service.md        ← active version (currently in effect)
│   └── Archive/
│       ├── terms_of_service_v1.md
│       ├── terms_of_service_v2.md
│       └── ...
├── CookiePolicy/
│   ├── current_cookie_policy.md
│   └── Archive/
├── Disclaimer/
│   ├── current_disclaimer.md
│   └── Archive/
└── README.md
```

### Document Versions (`versions.json`)

`versions.json` is the source of truth for **which version of each document is in effect**. A commit to a document does not, by itself, create a new version: only a change to `version` does.

```json
"terms_of_service": {
  "version": 1,
  "file": "TermsOfService/current_terms_of_service.md",
  "effective_date": "2026-06-22",
  "v1_legacy_hash": "f7bc861"
}
```

- `version` — integer, starts at 1 and never decreases. Raising it asks every user to accept the document again.
- `file` — path of the active text. It must exist; renaming the file means updating this field in the same PR.
- `effective_date` — the date the version takes effect (the document's "Last updated").
- `v1_legacy_hash` — before this manifest, an acceptance was recorded as the short hash of the last commit that touched the file. Acceptances recorded with this hash count as version 1. It never changes.

An acceptance is recorded as `v<version>@<short hash of the commit>`, e.g. `v2@1a2b3c4`: the version decides whether the user is up to date, and the hash points to the exact text they accepted.

### Changing a Document

1. **Typo, formatting or a wording change that does not alter rights or obligations:** edit the `current_*.md` file and leave `version` as is. Users are not asked to accept again.
2. **Material change** (anything that alters what the user agrees to): copy the current file to `Archive/<doc>_v<N>.md`, edit the `current_*.md`, raise `version` and update `effective_date` in `versions.json`, all in the same PR.
3. **Who decides:** a version bump is merged only with the explicit approval of the Horus Technologies LLC owner in the PR. When in doubt whether a change is material, treat it as material.

Every PR runs `.github/workflows/check-manifest.yml`: it fails when a `file` does not exist, a `version` decreases or a `v1_legacy_hash` changes, and it warns when a document changes without a version bump.

### Verifying Document History
You can inspect the complete change history of any file using standard GitHub features:

- Click History on any file to see all commits
- Use Blame to see who changed which line and when
- Every meaningful change is tied to a commit hash, author, date, and commit message

### Important Notes / Disclaimer

- Files located in /Archive/ folders are no longer in effect unless explicitly stated otherwise in a legal notice.
- The current_*.md files in the root of each category represent the active, legally binding versions.
- This repository is provided for transparency, reference, and integration purposes. It does not replace any legally required in-app or on-site presentation of the current terms.

We welcome reasoned feedback about wording clarity, but substantive legal changes follow our normal governance process.
