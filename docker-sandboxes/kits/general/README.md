# DChen general kit
General sandbox kit (Kit spec v3) with OpenTofu, AWS CLI, and Node.js 24 (via fnm) installed.

- `general.yaml` — kit descriptor (`schemaVersion: "3"`)
- `general.dockerfile` — recipe that builds the kit's image (replaces the old `images/general` image)
- `files/home/` — copied into `/home/agent`; `setup_sbx.sh` runs once at build time

Example create command (source-form kit, built on demand by `sbx`, no push needed):
```
sbx create --name sb0 ..\personal-config\docker-sandboxes\kits\general .
```

Validate/build the kit locally:
```
docker buildx build . -f general.yaml --output type=cacheonly
```

Override the Node.js version at build time with `--build-arg NODE_VERSION=<version>`.

Set GitHub secret:
```
sbx secret set github --command "pass-cli.exe item view --vault-name dchenstealth --item-title GitHubDChenStealthSandboxPAT --field Secret"
```
