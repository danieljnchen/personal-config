# DChen general kit
General sandbox kit with OpenTofu and AWS CLI installed.

Example create command:
```
sbx create --kit ..\personal-config\docker-sandboxes\kits\general dchen-general-kit --name sb0 .
```

Set GitHub secret:
```
sbx secret set github --command "pass-cli.exe item view --vault-name Daniel --item-title GitHubDChenStealthSandboxPAT --field Secret"
```
