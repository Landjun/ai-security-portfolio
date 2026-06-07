// guard.ts —— 输入护栏(提示注入检测)+ 工具调用权限审计(TypeScript 版)
// 与 Python 作品集同一套安全思路:输入拦注入、工具执行前过最小权限审计。

export type Decision = "ALLOW" | "APPROVAL" | "DENY";

// 常见提示注入特征(中英文),与 02 prompt-injection 检测器思路一致
const INJECTION_PATTERNS: RegExp[] = [
  /忽略.*(之前|以上|前面).*(指令|提示|规则)/i,
  /无视.*(指令|规则|设定)/i,
  /ignore\s+(all\s+)?(previous|above|prior)\s+instructions?/i,
  /(你的|system)\s*(系统)?\s*(prompt|提示词)/i,
  /(泄露|告诉我|输出).*(密钥|秘密|key|system\s*prompt|提示词)/i,
  /你现在是|从现在起你是|pretend\s+you\s+are|act\s+as/i,
];

export function detectInjection(input: string): { injection: boolean; matched: string[] } {
  const matched = INJECTION_PATTERNS.filter((p) => p.test(input)).map((p) => p.source);
  return { injection: matched.length > 0, matched };
}

export interface ToolRule {
  action: Decision;
  maxAmount?: number; // 金额上限约束(可选)
}

// 权限策略表:最小权限,未登记的工具默认拒绝
export const POLICY: Record<string, ToolRule> = {
  search_docs: { action: "ALLOW" },
  issue_refund: { action: "APPROVAL", maxAmount: 1000 },
  delete_database: { action: "DENY" },
};

export function audit(
  tool: string,
  args: Record<string, unknown> = {},
): { decision: Decision; reason: string } {
  const rule = POLICY[tool];
  if (!rule) return { decision: "DENY", reason: `工具 '${tool}' 不在白名单(最小权限默认拒绝)` };
  if (rule.action === "DENY") return { decision: "DENY", reason: `工具 '${tool}' 被策略禁止(高危/不可逆)` };
  if (rule.maxAmount !== undefined) {
    const amount = Number(args.amount ?? 0);
    if (amount > rule.maxAmount) {
      return { decision: "DENY", reason: `金额 ${amount} 超过上限 ${rule.maxAmount},拒绝(疑似越权)` };
    }
  }
  if (rule.action === "APPROVAL") return { decision: "APPROVAL", reason: `工具 '${tool}' 为敏感动作,需人工确认` };
  return { decision: "ALLOW", reason: `工具 '${tool}' 为低风险操作,放行` };
}
