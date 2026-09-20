git config --global url."https://github.com/".insteadOf "git@github.com:"
git config --global user.name "Daniel Chen (agent)"
git config --global user.email "danieljnchen+agent@gmail.com"

mkdir -p /home/agent/.claude
cp -r /home/agent/claude_setup/. /home/agent/.claude

/home/agent/.local/bin/claude mcp add-json --scope user aws-mcp '{"type":"stdio","command":"uv","args":["tool", "run", "mcp-proxy-for-aws-cli@latest","https://aws-mcp.us-east-1.api.aws/mcp","--metadata","AWS_REGION=us-east-1"],"env":{}}'
