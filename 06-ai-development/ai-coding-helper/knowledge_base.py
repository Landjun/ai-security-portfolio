"""
knowledge_base.py —— 「码小安」的编程学习/面试知识库。

RAG 的价值:让助手基于**可控、可更新的资料**回答,而不是只靠模型记忆——
答案更准、可溯源、好维护。这里放一组编程入门与求职面试要点作演示。
真实场景可换成你自己的笔记、面试题库、团队规范文档。
"""

DOCUMENTS = [
    {"id": "kb-1", "title": "Python 列表与元组的区别",
     "content": "list 可变(增删改),用 []；tuple 不可变,用 ()。tuple 更省内存、可作字典 key、可哈希。"
                 "需要频繁修改用 list,需要固定不变或作 key 用 tuple。"},
    {"id": "kb-2", "title": "二分查找原理与边界",
     "content": "前提是有序数组。每次取中点比较,目标在左半就 right=mid-1,在右半就 left=mid+1。"
                 "时间复杂度 O(log n)。常见坑:mid 用 left+(right-left)//2 防溢出;循环条件 left<=right。"},
    {"id": "kb-3", "title": "HTTP 与 HTTPS 的区别",
     "content": "HTTP 明文传输,HTTPS 在 TCP 与 HTTP 之间加了 TLS,做加密+身份认证+完整性校验,默认端口 443。"
                 "面试常追问:TLS 握手过程、对称加密与非对称加密如何配合(非对称协商出对称密钥)。"},
    {"id": "kb-4", "title": "进程与线程的区别",
     "content": "进程是资源分配的基本单位,有独立内存空间;线程是 CPU 调度的基本单位,同进程内线程共享内存。"
                 "Python 因 GIL,CPU 密集用多进程,IO 密集用多线程或 asyncio。"},
    {"id": "kb-5", "title": "SQL 注入原理与防御",
     "content": "把用户输入拼进 SQL 导致语义被篡改。防御首选参数化查询(预编译占位符),"
                 "辅以最小权限、输入校验、ORM。绝不用字符串拼接 SQL。这是 AI 安全里输出处理的同源问题。"},
    {"id": "kb-6", "title": "什么是 RAG(检索增强生成)",
     "content": "RAG = 先检索相关资料,再把资料拼进提示让大模型基于资料作答。好处:减少幻觉、可更新知识、可溯源。"
                 "关键组件:embedding 向量化、向量库、相似度检索、提示拼接。"},
    {"id": "kb-7", "title": "AI 应用开发常见技术栈",
     "content": "模型调用(OpenAI 兼容 SDK)、框架(LangChain/LangChain4j)、检索(RAG+向量库)、"
                 "Agent 与工具调用(function calling/ReAct)、流式输出(SSE)、护栏(输入输出校验)。"},
    {"id": "kb-8", "title": "面试:如何控制 Agent 调用高危工具",
     "content": "不能依赖模型自觉。做法:工具执行前加权限审计关卡——只读工具放行,"
                 "敏感动作(退款/删除)需人工确认,超阈值直接拦截,并记录审计日志。"},
]
