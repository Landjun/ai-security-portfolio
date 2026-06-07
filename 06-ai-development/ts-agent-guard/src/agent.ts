// agent.ts —— 极简工具调用 Agent(TypeScript):输入护栏 -> 规划工具 -> 权限审计 -> 执行。
// 用确定性的 mock "LLM" 决策,便于离线演示/测试,不依赖真实大模型。

import { detectInjection, audit } from "./guard";

export interface ToolCall {
  tool: string;
  args: Record<string, unknown>;
}

// 模拟 LLM 规划:根据用户输入决定调用哪个工具(确定性)
function mockPlan(userInput: string): ToolCall | null {
  if (/退款|refund/i.test(userInput)) {
    const m = userInput.match(/(\d+)/);
    return { tool: "issue_refund", args: { amount: m ? Number(m[1]) : 0 } };
  }
  if (/查|搜|search|文档|docs/i.test(userInput)) {
    return { tool: "search_docs", args: { q: userInput } };
  }
  if (/删库|drop|delete/i.test(userInput)) {
    return { tool: "delete_database", args: {} };
  }
  return null;
}

const TOOL_IMPL: Record<string, (args: Record<string, unknown>) => string> = {
  search_docs: (a) => `查到与「${String(a.q)}」相关的资料(模拟)`,
  issue_refund: (a) => `已退款 ${Number(a.amount)} 元(模拟)`,
};

/**
 * 跑一轮 Agent。confirm 为 APPROVAL 时的人工确认回调(默认拒绝,演示无人值守安全)。
 */
export function runAgent(
  userInput: string,
  confirm: (call: ToolCall, reason: string) => boolean = () => false,
): string {
  // 1) 输入护栏
  const g = detectInjection(userInput);
  if (g.injection) return `【输入护栏拦截】疑似提示注入,命中 ${g.matched.length} 项特征`;

  // 2) 规划工具
  const plan = mockPlan(userInput);
  if (!plan) return "我可以帮你查资料或处理退款,请说明需求。";

  // 3) 工具执行前过权限审计
  const { decision, reason } = audit(plan.tool, plan.args);
  if (decision === "DENY") return `【审计拒绝】${reason}`;
  if (decision === "APPROVAL" && !confirm(plan, reason)) return `【已取消】${reason}`;

  // 4) 执行
  const impl = TOOL_IMPL[plan.tool];
  return impl ? impl(plan.args) : `【错误】工具 ${plan.tool} 未实现`;
}
