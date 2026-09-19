# DChen general kit
General sandbox kit with OpenTofu and AWS CLI installed.

Example create command:
```
sbx create --name sb0 ..\personal-config\docker-sandboxes\kits\general .
```

Set GitHub secret:
```
sbx secret set github --command "pass-cli.exe item view --vault-name Daniel --item-title GitHubDChenStealthSandboxPAT --field Secret"
```
