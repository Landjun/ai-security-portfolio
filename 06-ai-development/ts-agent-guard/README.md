# 项目:TS Agent Guard(TypeScript 工具调用 Agent + 输入护栏 + 权限审计)

> 回应岗位 JD 点名的 **TypeScript** 技术栈:用 TS 复刻作品集里"**Agent 工具调用 × 安全**"的核心思路——
> 输入侧拦提示注入、工具执行前过最小权限审计。与 Python 版(06 码小安 / langchain-agent)同源,证明换语言也能落地同一套安全工程。

## 为什么做这个
- JD 常同时要求 Python 与 **TypeScript**(前端/Node 生态的 AI 应用)。作品集主体是 Python,这里用 TS 补齐技术栈广度。
- 不是玩具:把"**安全做成工具调用的统一关卡**"这一核心理念用 TS 再实现一遍。

## 能力
- `src/guard.ts`:`detectInjection`(提示注入检测,正则特征)+ `audit`(工具权限审计:只读放行 / 敏感需确认 / 超额或未登记拒绝)。
- `src/agent.ts`:确定性 mock "LLM" 规划工具 → 输入护栏 → 权限审计 → 执行的完整循环(离线可跑,不依赖真实模型)。
- `src/index.ts`:演示 5 类输入(只读 / 敏感合规 / 超额 / 高危 / 注入)。
- `src/guard.test.ts`:用 **Node 内置 `node:test`** 做 9 个单测,零额外测试框架。

## 运行 & 测试

```bash
cd 06-ai-development/ts-agent-guard
npm install          # 安装 tsx / typescript / @types/node
npm run demo         # 跑演示(tsx 直接执行 TS)
npm test             # 跑单测(node:test)
npm run build        # 仅类型检查(tsc --noEmit)
```

预期 demo 输出(摘要):
- "查文档" → 只读工具放行;
- "退款 50 元" → 敏感动作,无人确认时被拦(`确认通过`场景会执行);
- "退款 99999 元" → 超额,审计拒绝;
- "删库" → 高危工具,策略禁止;
- "忽略之前的指令…" → 输入护栏拦截。

## 面试表达
> "JD 要求 TypeScript,我就用 TS 把作品集里 Agent 工具调用的安全闭环又实现了一遍:输入侧正则拦提示注入,工具执行前过最小权限审计——只读放行、退款这类敏感动作需人工确认、超额或未登记工具直接拒绝。测试用 Node 自带的 node:test,不引额外框架。这证明我的安全工程思路不绑定某个语言。"

## 安全边界 & 说明
工具均为模拟(退款不涉真实资金);仅本地/学习用途。
> 注:作者机器未装 Node,但本项目已接入 **GitHub Actions CI**(`typescript` job:`npm install` → `tsc --noEmit` 类型检查 → `npm test` node:test),由 CI 在 Node 20 上构建与测试,保证可运行。本机同样可 `npm install && npm test` 复现。
