import py_trees
from agent_behavior_tree import build_behavior_tree
from py_trees.blackboard import Client

def calculate_risk(txn):
    score = 0
    if txn['amount'] < 5.0:
        score += 40
    elif txn['amount'] > 1000:
        score += 20

    if abs(txn['v14']) > 2.0: score += 30
    if abs(txn['v10']) > 1.5: score += 30
    if abs(txn['v17']) > 1.5: score += 30
    if abs(txn['v12']) > 2.0: score += 30

    v_flags = sum([
        abs(txn['v14']) > 4,
        abs(txn['v10']) > 4,
        abs(txn['v17']) > 4,
        abs(txn['v12']) > 4
    ])
    if v_flags >= 2:
        score += 50
    return score

def process_transaction(txn, token):
    risk_score = calculate_risk(txn)
    txn["risk_score"] = risk_score  # Save for frontend

    blackboard = Client(name="AgentMemory")
    blackboard.register_key("txn_id", access=py_trees.common.Access.WRITE)
    blackboard.register_key("token", access=py_trees.common.Access.WRITE)
    blackboard.register_key("risk_score", access=py_trees.common.Access.WRITE)
    blackboard.register_key("allowed", access=py_trees.common.Access.READ)
    blackboard.register_key("reason", access=py_trees.common.Access.READ)

    blackboard.txn_id = txn.get("id", "unknown")
    blackboard.token = token
    blackboard.risk_score = risk_score

    root = build_behavior_tree()
    root.tick_once()

    if blackboard.allowed:
        return f"✅ Flagged: {blackboard.reason}", risk_score
    else:
        return f"✅ Safe: {blackboard.reason}", risk_score


