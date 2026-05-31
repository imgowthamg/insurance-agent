import json
from app.rag import search_policy
from app.llm import llm


# 1. Intent Agent
def intent_agent(state):
    # state is always a dict (passed from graph); extract question safely
    question = state.get("question", "") if isinstance(state, dict) else str(state)
    return {
        **state,
        "question": question,
        "intent": "insurance_query"
    }


# 2. Retriever Agent
def retriever_agent(state):
    question = state["question"]

    docs = search_policy(question)
    state["context"] = "\n\n".join(docs)

    return state


# 3. Policy Agent (RAG reasoning)
def policy_agent(state):
    prompt = f"""
You are an insurance policy analyst.

Use ONLY context below.

Context:
{state['context']}

Question:
{state['question']}

Extract ONLY relevant clause.
Do not add external knowledge.
"""

    response = llm.invoke(prompt)
    state["analysis"] = response.content
    return state


# 4. Decision Agent (STRICT JSON OUTPUT)
def decision_agent(state):
    prompt = f"""
You are a strict insurance decision engine.

Return ONLY JSON:

{{
  "decision": "Approved | Not Covered | Partially Covered",
  "reason": "short explanation"
}}

Context:
{state['context']}

Analysis:
{state['analysis']}
"""

    response = llm.invoke(prompt)

    cleaned = response.content.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
    except Exception:
        parsed = {
            "decision": "Parsing Error",
            "reason": cleaned
        }

    state["decision"] = parsed
    return state


# 5. Report Agent (no hallucination)
def report_agent(state):
    prompt = f"""
Create a clean insurance report.

Rules:
- Only use provided data
- Do NOT invent new facts

Question: {state['question']}
Context: {state['context']}
Decision: {state['decision']}
"""

    response = llm.invoke(prompt)
    state["final_answer"] = response.content
    return state
