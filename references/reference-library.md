# IP 参考图库

## 目录与已授权包

默认图库位于 `${CODEX_HOME}/ip-reference-library/`。本包附带 `assets/authorized-reference-library/`：只包含资产库所有者确认可再分发的素材。每个版本的 `source.md` 必须保留来源页、资产 URL、获取日期、权利方和授权声明。

不要把此记录理解为任何权利方的授权背书；授权状态改变时，删除对应素材并重新打包。

```text
${CODEX_HOME}/ip-reference-library/
  pop-mart/<character>/official-store-product/front.*
  sanrio/<character>/official-web/front.*
  chiikawa/<character>/official-web/front.*
  peanuts/<character>/official-web/front.*
  moomin/<character>/official-web/front.*
  jellycat/<character>/official-web/front.*
  mbti-16personalities/<type>/official-web/front.*
  family-style/<style>/official-web/front.*
```

文件夹使用小写英文短横线。具体系列、服装、产品形态或动画版本必须单独建版本目录。

## 每个版本保存什么

- `front.*`：正面或最能识别轮廓的主参考。
- `three-quarter.*`：推荐的 3/4 角度参考；主参考清楚时可以稍后补齐。
- `side.*`：只有当场景确实需要侧面时保存。
- `source.md`：来源网址、获取日期、权利方、版本说明、是否允许本地使用或再分发。

不要缓存搜索结果页缩略图、带水印预览、同人图或来源不明素材。不要为了凑数量混用不同版本。

## 查询顺序

1. 优先从包内 `assets/authorized-reference-library/` 读取；需要时同步到私有图库。
2. 用官方英文角色名规范化路径。
3. 在对应家族下查找精确角色和版本。
4. 用 `rg --files` 找 `front`、`three-quarter`、`side` 与 `source.md`。
5. 用 `view_image` 检查候选图，选 1-3 张清晰且同版本的参考。
6. 缺图时告诉用户具体缺少“哪个角色、哪个版本、哪个角度”。

## 刷新已授权素材

授权清单在 `references/authorized-reference-sources.json`，采集器在 `scripts/collect_reference_library.py`。先运行它写入私有图库，再把已确认可再分发的目录复制进 `assets/authorized-reference-library/`。不要添加搜索页缩略图或无法说明来源的素材。

POP MART 与 Jellycat 的角色参考来自对应官方商城产品页与其官方 CDN。遇到新角色时，先在官方商城定位并验证产品页，再把该产品页和实际渲染的主图 URL 加进清单；不能以第三方替代图补位。

## 分享技能时

只打包：

- `SKILL.md`
- `references/`
- `assets/reference-manifest.yaml`
- 清单与逐图 `source.md` 支撑的授权素材，或本任务生成的身份锚点与画风板
- `agents/openai.yaml`
- `LICENSE`
- `NOTICE.md`

不得打包 `${CODEX_HOME}/ip-reference-library/` 中没有明确再分发授权的官方原图或动画截图。
