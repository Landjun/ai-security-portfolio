"""
policy.py —— 工具调用权限策略(谁能调什么、调用的边界)。

核心理念:最小权限 (Least Privilege)。
- 默认拒绝:不在策略里的工具一律拒绝(白名单思想)。
- 分级授权:只读放行;对外/资金等动作需人工确认;数据销毁直接禁止。
- 参数约束:即使工具允许,参数也要在边界内(如转账金额上限)。
"""

# 决策三态
ALLOW = "ALLOW"        # 直接放行
APPROVAL = "APPROVAL"  # 需人工确认后才能执行
DENY = "DENY"          # 直接拒绝

# 权限策略表。未列出的工具 -> 默认拒绝。
POLICY = {
    "read_order": {
        "action": ALLOW,
    },
    "send_email": {
        "action": APPROVAL,        # 对外动作,需人工确认
    },
    "transfer_money": {
        "action": APPROVAL,        # 资金操作,需人工确认
        "constraints": {
            "max_amount": 1000,    # 且单笔不得超过 1000 元,超了直接拒绝
        },
    },
    "delete_database": {
        "action": DENY,            # 数据销毁,任何情况都禁止
    },
}
