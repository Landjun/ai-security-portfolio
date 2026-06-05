# 案例:不安全反序列化 (Insecure Deserialization)

> `01 传统安全` 案例。对应 OWASP Top 10 A08。本地**无害载荷**演示(只打印,不做真实危害)。

## 1. 原理
`pickle.loads` 反序列化时会执行对象的 `__reduce__`。对**不可信数据**反序列化,
攻击者构造恶意 pickle 即可在 loads 时**远程代码执行(RCE)**。`yaml.load`(无安全 Loader)同理。

## 2. 复现
```
insecure-deserialization/
├── demo.py    # 不安全(pickle.loads) vs 安全(json)
└── README.md
```
`python demo.py`:不安全版在 `pickle.loads` 时自动执行了 payload 的代码(本例无害打印),
安全版用 json 只还原数据、不执行代码。

## 3. 防护
1. **不要反序列化不可信数据**(最重要)。
2. **用只还原数据的格式**:JSON、Protobuf 等替代 pickle。
3. 必须用 pickle 时:**只接受可信来源 + 签名校验完整性**。
4. yaml 用 `yaml.safe_load`;Java 等同理避免不安全反序列化组件。

## 4. 修复建议
把跨信任边界的数据交换从 pickle 改为 JSON;移除对用户输入的反序列化;对内部 pickle 加签名。

## 5. 检测清单
- [ ] 是否对用户/外部数据 `pickle.loads` / `yaml.load`?
- [ ] 跨网络/缓存/消息队列的对象是否用安全格式?
- [ ] 必要的反序列化是否做来源校验与签名?

## 6. 面试表达
> "我演示了不安全反序列化:pickle 反序列化会执行对象的 __reduce__,所以对不可信数据 loads
> 就是 RCE——我用一个无害载荷让它在 loads 时自动打印了一句话,真实攻击这里就是 os.system。
> 修复是改用 JSON 这种只还原数据的格式,必须 pickle 时只信可信来源加签名。对应 OWASP A08。"

## 安全边界
载荷为无害打印,演示机制而非危害;仅本地教学。
