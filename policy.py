from access_control import verify_token

def check_policy(token, risk_score):
    role = verify_token(token)

    if not role:
        return False, "Access Denied: Invalid or expired token"

    if role == "auditor":
        return False, "Auditor can't take action"

    if risk_score > 50 and role in ["agent", "admin"]:
        return True, "High risk: flagged by policy"

    return False, "Safe"





