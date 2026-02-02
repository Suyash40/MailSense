from fastapi import APIRouter
from app.agents.agent_graph import build_graph

router = APIRouter()

graph = build_graph()

@router.get("/emails")
def run_agents():

    result = graph.invoke({})

    return {"emails": result["emails"]}
