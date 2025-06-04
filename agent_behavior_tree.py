import py_trees
from policy import check_policy
from storage_sqlite import log_flag
from cache_memory import cache_flag
from logger import log_event

class TokenCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name="Check Token"):
        super().__init__(name)
        self.blackboard = py_trees.blackboard.Client()
        self.blackboard.register_key("token", access=py_trees.common.Access.READ)

    def update(self):
        return py_trees.common.Status.SUCCESS if self.blackboard.token else py_trees.common.Status.FAILURE

class RiskEvaluation(py_trees.behaviour.Behaviour):
    def __init__(self, name="Evaluate Risk"):
        super().__init__(name)
        self.blackboard = py_trees.blackboard.Client()
        self.blackboard.register_key("token", access=py_trees.common.Access.READ)
        self.blackboard.register_key("risk_score", access=py_trees.common.Access.READ)
        self.blackboard.register_key("allowed", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("reason", access=py_trees.common.Access.WRITE)

    def update(self):
        allowed, reason = check_policy(self.blackboard.token, self.blackboard.risk_score)
        self.blackboard.allowed = allowed
        self.blackboard.reason = reason
        return py_trees.common.Status.SUCCESS

class FlagIfRisky(py_trees.behaviour.Behaviour):
    def __init__(self, name="Flag If Risky"):
        super().__init__(name)
        self.blackboard = py_trees.blackboard.Client()
        self.blackboard.register_key("allowed", access=py_trees.common.Access.READ)
        self.blackboard.register_key("txn_id", access=py_trees.common.Access.READ)
        self.blackboard.register_key("reason", access=py_trees.common.Access.READ)
        self.blackboard.register_key("token", access=py_trees.common.Access.READ)

    def update(self):
        if self.blackboard.allowed:
            log_flag(self.blackboard.txn_id, self.blackboard.token, self.blackboard.reason)
            cache_flag(self.blackboard.txn_id, self.blackboard.reason)
            log_event(f"Flagged txn {self.blackboard.txn_id}: {self.blackboard.reason}")
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

def build_behavior_tree():
    root = py_trees.composites.Sequence(name="Compliance Check Sequence", memory=True)
    root.add_children([TokenCheck(), RiskEvaluation(), FlagIfRisky()])
    return root
