from utils.mcp_client import MCPClient


class AIHelper:
    def analyze_failure(self, error):
        prompt = f"Analyze this error: {error}"
        return MCPClient().send_request(prompt)
