# Assignment A02-D: Architecting & Governing Autonomous AI Agents

## Project Overview

This project implements a rational intelligent agent that autonomously evaluates financial transactions and enforces access control using identity-based policies. The system follows structured decision-making using a behavior tree and logs every governance action for traceability.

---

## System Architecture

- `main.py`: FastAPI application that connects user input to the agent logic
- `storage_sqlite.py`: Stores transaction data persistently using SQLite
- `cache_memory.py`: Stores recent decisions in memory (Python dictionary)
- `agent_logic.py` and `agent_behavior_tree.py`: Evaluate transactions using a behavior tree
- `access_control.py`: Decodes token and identifies the user’s role
- `policy.py`: Applies role-based policy using token and risk score
- `logger.py`: Logs every decision and action into `agent_log.log`

---

## Identity Governance Using Tokens

The system uses token-based access control. Each API request must include a token that represents the user’s role.

### Token-to-Role Mapping:

| Token Value       | Role     |
|-------------------|----------|
| token_auditor     | Auditor  |
| token_analyst     | Analyst  |
| None / Invalid    | Blocked  |

### Governance Rules:

- **Auditor**: Can approve any transaction regardless of risk
- **Analyst**: Can only approve if `risk_score < 0.75`
- **No token or invalid token**: Access denied immediately

---

## Agent Behavior and Logic

The goal of the agent is to automatically evaluate transactions and decide if they are allowed or not based on user role and risk score.

### Agent Flow (Behavior Tree):
1. **Token Check**: Is the token valid? If not, stop.
2. **Risk Evaluation**: Use `check_policy(token, risk_score)` to check if the user is allowed.
3. **Flag If Risky**: If allowed, log the result, save it to the database, and cache it.

If the policy denies the action, the agent stops and does nothing further.

---

## Interface Walkthrough

1. I select a token — for example, “Agent Token” or “Auditor Token”.
2. I upload a CSV file with transaction data, including `txn_id`, `amount`, and `risk_score`.
3. I click “Start Stream Simulation” to begin the decision-making process.

The agent goes through each transaction one by one and shows whether it is ✔️ Safe or ❌ Fraud, based on my role and the transaction’s risk level.

---

## Dataset Used

For testing and running this agent, I used a real-world credit card transaction dataset from **Kaggle**.  
The dataset contains thousands of transactions, each with fields like transaction ID, amount, and a fraud label.  
For this project, I simplified it and created a risk score column (`risk_score`) to help simulate more dynamic decision-making.

This realistic data helps the agent make smart, policy-based decisions like it would in a real fraud detection system.

---

## What’s Happening in the Background

- **JWT-style token system**: Used to identify the user and apply access policies
- **Memory caching**: Recent results are stored in a dictionary for fast access
- **SQLite database**: All approved transactions are saved for traceability
- **Logging system**: Each decision is logged with token, risk score, and reason

---

## Example

- A transaction has a **risk score of 100**
- If I use the **Agent token**, the agent blocks it → ❌ Fraud (agents can’t approve high risk)
- If I use the **Auditor token**, the agent allows it → ✔️ Safe (auditors can approve all)

---

## Code Walkthrough

### 1. `main.py`
> This is the entry point of the FastAPI app. It accepts token and transaction data, connects to the agent logic, and returns the result.

### 2. `agent_behavior_tree.py`
> This file builds the behavior tree using `py_trees`.  
> It runs three steps:  
> - `TokenCheck`: Stop if no token  
> - `RiskEvaluation`: Check policy using role and risk  
> - `FlagIfRisky`: If allowed, save, log, and cache the result

### 3. `policy.py` → `check_policy()`
> This function applies access rules.  
Examples:
- Agent + low risk → ✅ allowed  
- Auditor → ✅ always allowed  
- Agent + high risk → ❌ not allowed

### 4. `access_control.py`
> Decodes the token and returns the user's role. If token is missing, the action is blocked.

### 5. `storage_sqlite.py`
> Stores the result in a SQLite database — if allowed.

### 6. `cache_memory.py`
> Stores recent decisions in memory using a Python dictionary.

### 7. `logger.py`
> Logs every agent decision into `agent_log.log` with details.

### 8. `frontend_app.py`
> This is the Streamlit-based UI.  
> It allows token selection, file upload, and shows ✔️ Safe / ❌ Fraud decisions for each transaction.

---

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
```
## Final Summary

This project shows how an autonomous agent can make smart decisions based on user role and transaction risk while still following strict access rules.  
Each part of the system — token check, risk evaluation, caching, database, logging, and interface — works together in a clear and controlled way.  
The result is a secure, intelligent, and observable agent system.

