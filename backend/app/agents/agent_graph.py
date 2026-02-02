from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from app.agents.email_reader import EmailReaderAgent
from app.agents.email_classifier import EmailClassifierAgent
from app.agents.email_extractor import EmailExtractorAgent
from app.agents.action_agent import ActionAgent


# -----------------------------
# Define shared state
# -----------------------------

class EmailState(TypedDict):
    emails: list


# -----------------------------
# Agent Nodes
# -----------------------------

EMAIL = "pwizard401@gmail.com"
PASSWORD = "esoe zzrx kddi orsp"


def reader_node(state: EmailState):

    reader = EmailReaderAgent(EMAIL, PASSWORD)
    emails = reader.fetch_emails()

    return {"emails": emails}


def classifier_node(state: EmailState):

    classifier = EmailClassifierAgent()

    for mail in state["emails"]:
        mail["category"] = classifier.classify(
            mail["subject"],
            mail["body"]
        )

    return state


def extractor_node(state: EmailState):

    extractor = EmailExtractorAgent()

    import json

    for mail in state["emails"]:
        raw = extractor.extract_info(
            mail["subject"],
            mail["body"]
        )

        clean = raw.replace("```json", "").replace("```", "").strip()
        mail["extracted_info"] = json.loads(clean)

    return state


def action_node(state: EmailState):

    action_agent = ActionAgent()

    for mail in state["emails"]:
        mail["actions"] = action_agent.process(
            mail["category"],
            mail["extracted_info"]
        )

    return state


# -----------------------------
# Build LangGraph
# -----------------------------

def build_graph():

    graph = StateGraph(EmailState)

    graph.add_node("reader", reader_node)
    graph.add_node("classifier", classifier_node)
    graph.add_node("extractor", extractor_node)
    graph.add_node("action", action_node)

    graph.set_entry_point("reader")

    graph.add_edge("reader", "classifier")
    graph.add_edge("classifier", "extractor")
    graph.add_edge("extractor", "action")

    graph.add_edge("action", END)

    return graph.compile()
