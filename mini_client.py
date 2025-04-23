import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def main():
    # mini_server.py をPythonで実行し、stdin/stdoutで接続
    server_params = StdioServerParameters(
        command="/Users/kohei/repos/Log-Analyzer-with-MCP/.venv/bin/python", 
        args=["/Users/kohei/repos/Log-Analyzer-with-MCP/src/cw-mcp-server/server.py"])

    # サーバ接続のためのクライアントストリームを確立
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # 初期化処理（initialize）
            await session.initialize()

            # "hello_world" ツールを呼び出し
            result = await session.call_tool("search_logs", {
                "log_group_name": "/aws/lambda/bluebench",
                "hours": 24,
                "query": "fields @timestamp, @message | sort @timestamp desc"
            })
            print("Tool result:", result.content)

if __name__ == "__main__":
    asyncio.run(main())
