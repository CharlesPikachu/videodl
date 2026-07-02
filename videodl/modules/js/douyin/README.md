# 抖音 a_bogus 签名

抖音 web 接口（`/aweme/v1/web/aweme/detail/` 等）需要 `a_bogus` 反爬签名。该签名由抖音
前端 JS 算法生成、**匿名即可（不需要登录）**，但算法随抖音版本变化。

## 文件

- `a_bogus.<version>.js` — 签名算法（按版本存放）。入口函数 `get_abogus(query, post, ua)`。
- `sign.js` — node 包装器：内置浏览器环境 polyfill（document/navigator/canvas…），剥掉算法
  自带的坏 polyfill，用 node 内置 `vm` 模块在干净上下文里跑算法。
  - 用法：`node sign.js "<query>" "<post>" "<user_agent>"`，stdout 输出 a_bogus。
  - 选版本：环境变量 `ABOGUS_VERSION=<version>`（默认见 sign.js 的 `DEFAULT_VERSION`）。

Python 侧封装见 `videodl/modules/utils/douyin_sign.py` 的 `get_a_bogus()` / `sign_query()`，
走 videodl 已自带的 node（nodejs_wheel），无需额外依赖。

## 按版本更新

抖音改版导致签名失效时：
1. 取一份新版 `douyin.js`（含 `get_abogus`），放成 `a_bogus.<新版本>.js`。
2. 设 `ABOGUS_VERSION=<新版本>` 或改 `sign.js` 的 `DEFAULT_VERSION`。

旧版本文件保留，方便回退/对比。

## 来源与许可

`a_bogus.1.0.1.5.js` 与浏览器环境 polyfill 改编自
[hhy5562877/douyin_mcp](https://github.com/hhy5562877/douyin_mcp)（MIT License）。
原项目用 py_mini_racer 跑该算法；此处改为用 node（vm 模块）跑，以复用 videodl 自带的
node、避免引入新依赖。
