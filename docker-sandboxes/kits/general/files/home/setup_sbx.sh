git config --global credential.helper store
git config --global url."git@github.com:".insteadOf "https://github.com/"
git config --global user.name "Daniel Chen (agent)"
git config --global user.email "danieljnchen+agent@gmail.com"

claude mcp add-json --user aws-mcp '{"type":"stdio","command":"uv","args":["tool", "run", "mcp-proxy-for-aws-cli@latest","https://aws-mcp.us-east-1.api.aws/mcp","--metadata","AWS_REGION=us-east-1"],"env":{}}'
