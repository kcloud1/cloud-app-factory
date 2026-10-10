# Optional static Worker starter

This folder is inert in the universal template. After accepting a new project's
intent via `INIT.md`, copy these **six files** to that app's repository root:
`worker.js`, `wrangler.jsonc`, `.assetsignore`, `index.html`, `style.css`, `script.js`.
Do not overwrite existing app files. Keep this README as a reference, not an asset.

Replace `replace-with-app-name` with the approved Worker name and replace the page's
app name/content. Update `compatibility_date` to the adoption date. No install or
build is needed to open `index.html` locally. The example has a local demo action
and theme toggle; it makes no network calls.

`worker.js` delegates to `ASSETS`; the allowlist uploads only the three public
frontend files. Add each intended public file explicitly if the app grows.
No API, package manifest, Actions workflow, cloud credentials, domain route, or
provisioning script is included. Production `workers.dev` and Version URLs are
disabled by default (`workers_dev: false`, `preview_urls: false`), so the app
has no public hostname until an explicitly approved Custom Domain is attached.
If the owner intends to publish on `workers.dev`, approve that hostname and
explicitly change `workers_dev` to `true` in the adopted app's configuration.

Follow the [owner onboarding](../../docs/CLOUDFLARE_WORKERS_ONBOARDING.md) before
connecting Builds or deploying. Running `wrangler deploy` can create a Worker;
copying this example grants no provisioning or deployment authority.
