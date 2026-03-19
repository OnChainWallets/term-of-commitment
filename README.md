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
└── README.md
```

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
