# 代码生成时间: 2025-09-29 01:58:33
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional


# Pydantic 模型用于请求和响应验证
class LightningNode(BaseModel):
    alias: str
    color: str
    last_update: str


# 创建 FastAPI 实例
app = FastAPI()


# 用于存储节点数据的模拟数据库
mock_lightning_nodes = {
    "node1": {
        "alias": "Node 1",
        "color": "blue",
        "last_update": "2024-04-01 10:00:00"
    },
    "node2": {
        "alias": "Node 2",
        "color": "green",
        "last_update": "2024-04-01 11:00:00"
    }
}


# 获取所有节点信息的端点
@app.get("/nodes", response_model=List[LightningNode])
async def read_nodes():
    return list(mock_lightning_nodes.values())


# 获取单个节点信息的端点
@app.get("/nodes/{node_id}")
async def read_node(node_id: str, error: Optional[str] = None):
    node = mock_lightning_nodes.get(node_id)
    if node is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")
    return node


# 添加新节点的端点
@app.post("/nodes/")
async def create_node(node: LightningNode):
    if node.alias in mock_lightning_nodes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Node already exists")
    mock_lightning_nodes[node.alias] = node.dict()
    return node


# 更新节点信息的端点
@app.put("/nodes/{node_id}")
async def update_node(node_id: str, node: LightningNode):
    if node_id not in mock_lightning_nodes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")
    mock_lightning_nodes[node_id] = node.dict()
    return node


# 删除节点的端点
@app.delete("/nodes/{node_id}")
async def delete_node(node_id: str):
    if node_id not in mock_lightning_nodes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Node {node_id} not found")
    del mock_lightning_nodes[node_id]
    return {"message": f"Node {node_id} deleted"}
