# Assignment A02-D: Architecting & Governing Autonomous AI Agents

## Project Overview

This project implements a rational intelligent agent that autonomously evaluates financial transactions and enforces access control using identity-based policies. The system applies structured decision-making using a behavior tree and logs every governance action for traceability.

---

## System Architecture

- FastAPI (`main.py`) – Handles agent API endpoints.
- SQLite (`storage_sqlite.py`) – Stores transaction data persistently.
- In-memory cache (`cache_memory.py`) – Caches recent evaluation decisions.
- Agent Logic (`agent_logic.py`, `agent_behavior_tree.py`) – Performs evaluation using rules and behavior trees.
- Access Control (`access_control.py`) – Applies PBAC logic using token attributes.
- Policy Logic (`policy.py`) – Evaluates risk threshold and enforces constraints.
- Logger (`logger.py`) – Records all agent decisions into `agent_log.log`.

---

## Identity Governance Using Tokens

The system uses mock token-based access control. Each API request is expected to include a token with user role attributes, simulated as strings like `"token_analyst"` or `"token_auditor"`.

### Token-to-Role Mapping:
| Token Value       | Role     |
|-------------------|----------|
| token_auditor     | Auditor  |
| token_analyst     | Analyst  |
| None / Invalid    | Unknown  |

### Governance Rules (PBAC):
- Auditor: Full access, including high-risk transactions
- Analyst: Can approve transactions only if `risk_score < 0.75`
- Missing or Invalid Token: Request is denied and logged

Access logic is implemented in `access_control.py` and enforced using decorators.

---

## Agent Behavior and Logic

Goal: Evaluate transactions and decide whether to approve or deny them.

### Behavior Logic:
```python
if not token:
    deny("Missing token")
elif user.role == "auditor":
    allow("Auditor access granted")
elif user.role == "analyst" and risk_score < 0.75:
    allow("Analyst approved - low risk")
else:
    deny("Access denied due to high risk or unauthorized role")

