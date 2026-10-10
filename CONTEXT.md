# Current factory context

Primary repository: https://github.com/kcloud1/cloud-app-factory
Primary directory: /home/user/git/cloud-app-factory
Authorized related repository: kcloud1/factory-pilot (routine-update proof).
Templates and unrelated repositories remain read-only.

M0–M2 complete; M2 stays disabled/no-write with empty deployment allowlist.
M3 Issue #3 closed with factory PR #7 merge
d60d213b3fa77510deb29b084b0efa802c7c16a4, pilot PR #1 merge
f9834502860329026c5d321d9f73b5815302249d, Actions run 38067305167 PASS,
provider version/readback, exact live SHA and two browser PASS. Evidence:
https://github.com/kcloud1/cloud-app-factory/issues/3#issuecomment-6099659025

M4 Issue #4 closed: factory PR #8 merged
ae17563bbdc86903fb2bf65c2d6323c639226b76; the existing Codex Cloud environment
produced pilot PR #2, merged fc83a8a815432e55941db8bba8ac5d795e40d68a.
Automatic release run 38068905425 passed on the SAME Worker; live source SHA
matched. Evidence:
https://github.com/kcloud1/cloud-app-factory/issues/4#issuecomment-6099912560

M6 Issue #11 owns the optional pinned AWS software toolkit, credential-free
validation and aws-cloudops Skill. See docs/aws-toolkit.md for the contract and
Issue #11 for the exact review/merge and software-only acceptance receipt.
No AWS authentication, resources, IAM or spending authority is included.
M5 PR #10 is separate and remains untouched. Cloudflare pipelines and pilot stay
unchanged. Next application adoption must use the reviewed full factory SHA,
exact repository/Issue and explicit profile; AWS access needs separate authority.
