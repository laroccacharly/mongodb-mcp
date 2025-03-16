# mongodb-mcp 

MCP server to interact with MongoDB. 

## Installation 

1. Run MongoDB container
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

2. Install MCP server

```bash
uv tool install -e . 
```

## Usage 
Command line tool to interact with MCP server. 
```bash
mongodb-mcp
```


