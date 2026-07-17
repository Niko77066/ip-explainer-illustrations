# 单图提示词模板

执行参数：`model=gpt-image-2`；最终图优先 `quality=high`；接口支持尺寸时使用 `2048x1152`。

```text
Use case: illustration-story.
Asset type: standalone 16:9 Chinese article explanation illustration.
Generation model: GPT-image-2 only.

Selected IP and character lock:
Character identity: {官方英文角色名} from {家族}.
Exact series/version: {版本}.
Original identity references: {路径列表}.
Identity master: {identity-master.png}.
Style master: {style-master.png}.
Identity invariants: {逐字复用完整角色卡中的可检查事实}.
Style source title and exact version: {动画作品 / 家族动画 / default sketch}.
Style invariants: {逐字复用完整画风卡中的可检查事实}.

Core idea:
{只写一个认知动作或判断。}

Physical metaphor:
{低科技物件 + IP 正在完成的核心动作。}

Composition:
The IP is the central worker, not decoration. Subject occupies about 40%-60% of the canvas with sufficient quiet space for an article illustration. Preserve the selected animation medium and shape language. If and only if the style route is default sketch, use a pure white background and minimal black hand-drawn fine lines.

Chinese handwritten labels:
{3-5 个短标注；要求只出现这些文字。}

Color use:
Follow the selected animation palette. If and only if the style route is default sketch, use orange for the main path, red for a warning or result, and blue for a secondary note.

Constraints:
One image explains one mechanism. Change only pose, action, props, composition, expression, and the requested labels. Preserve every identity and style invariant. No extra characters. Never include 小黑 or an invented monster character. No upper-left type title. No PPT infographic, formal flowchart, commercial poster, children’s illustration, realistic UI, gradient, shadow, texture, dense text, or watermark. Invent a fresh metaphor for this content.
```

上传图片 Q 版时，在每张提示词中重复：

```text
Preserve the same recognizable identity, face or fur pattern, silhouette, colors, outfit, accessories, and Q-style proportions as the character anchor image. Change only pose and action required by this scene.
```
