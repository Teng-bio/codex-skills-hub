---
name: ppt-image-first
description: Build presentation plans for PPT / slides / decks through a conversation-first workflow, then propose multiple visual directions with preview images before writing deck specs. Use when the user asks to create a PPT, presentation, deck, 答辩稿, 路演 deck, 产品介绍 PPT, 汇报 PPT, or when the user has only a topic or rough materials and needs help clarifying structure, style, and page planning before generation.
---

# PPT Image First

Use this skill to turn a vague PPT request into a generation-ready deck plan.

## Core workflow

Follow this sequence:
1. Clarify the request lightly
2. Output a short baseline judgment
3. Get **需求确认**
4. Create a pre-style `content_report.md` or equivalent content basis unless the user already provided a complete report-like narrative
5. Output a short synthesized content-basis judgment
6. Do a short style-boundary alignment
7. Propose the requested number of style directions
8. Generate `首页 / 目录页 / 正文页` previews for each direction
9. Show the proposals together with the previews
10. Run style refinement rounds if needed
11. Get **风格确认**
12. Run `风格反演确认` on the chosen `首页 / 目录页 / 正文页`
13. Write `design_spec.md`
14. Write `slide_blueprint.md`
15. Write `spec_lock.md`
16. Output a short pre-generation summary
17. Get **生成前确认**
18. Confirm whether the user wants one final image per slide or multiple candidates per slide
19. Generate the first full set of page visuals
20. If the user chose multi-candidate generation, generate `n` candidates per slide with the same page prompt, assemble and open the candidate-picker HTML, and let the user copy the chosen codes back into chat
21. Map the returned selection codes to the chosen page images
22. Assemble and open a dedicated review HTML
23. Tell the user: if satisfied, they can end the review; if not satisfied, use the review page's copy buttons and paste the copied JSON into the chat input
24. Run review-and-retouch rounds if needed
25. Export and open the final PPT only after the reviewed pages are approved

Do not skip the confirmation points.

## What to load

- Read `references/workflow.md` for the detailed stage-by-stage process and the 3 confirmation points.
- Read `references/conversation_framework.md` when you need the conversation-first intake pattern.
- Read `references/style-system.md` when producing style proposals and interpreting V1-V8.
- Read `references/preview-flow.md` when producing style previews and organizing the preview output.
- Read `templates/content_report_reference.md` before writing `content_report.md` when the user has not already provided a complete report-like narrative.
- Read `templates/design_spec_reference.md` before writing `design_spec.md`.
- Read `templates/slide_blueprint_reference.md` before writing `slide_blueprint.md`.
- Read `templates/spec_lock_reference.md` before writing `spec_lock.md`.

## Working principles

- Treat the user like a client and yourself like the proposing design agent.
- Do not force the user to configure design parameters manually.
- In the first intake round, you may and should ask for real-world identity anchors such as `学校 / 公司 / 实验室 / 课题组 / 课程 / 品牌主体` when they are relevant, because they help later previews and final visuals feel grounded rather than generic.
- Treat those anchors as context-grounding inputs, not as style questions.
- Use style vectors internally, but present front-stage proposals through lightweight proposal cards.
- After `需求确认` and before formal style proposals, first create a pre-style content basis unless the user has already provided a complete report-like narrative.
- The default output of that stage should be `content_report.md`, written as a small research-style report / report-like article rather than a short outline.
- If the user already provided a complete report, paper, project document, experiment record, or complete narrative, compress that stage into extraction and structuring rather than expansion.
- Even if the user says not to expand content, still run the stage as `整理但不扩写`, not as a full skip.
- In the content-basis stage, do not turn the workflow into a long questionnaire.
- At most give one lightweight supplement opening such as: `如果你有现成材料可以补充，现在发我；没有的话我会先整理一版可继续推进的内容研究稿，并把不确定处标出来。`
- Show the user a synthesized content-basis judgment rather than dumping the raw report by default.
- Later previews and planning files should use this content basis rather than generic placeholder structure.
- Mark or scope inferred claims carefully; do not present unsupported precise data, experiment results, citations, or institutional conclusions as user-provided facts.
- After that content-basis stage, run one short style-boundary alignment step.
- In that step, ask only 3 short user-friendly questions: `(1) 亮色系 / 暗色系 / 中间态`, `(2) 常规专业路线 / 明显风格化设计路线`, and `(3) 这次想先看几套风格方向预览？`.
- Show this helper note together with the second question: `如果你没有特别偏好，默认选“常规专业路线”就行；只有当你明确想要更强设计感时，再选“明显风格化路线”。`
- Show this helper note together with the third question: `默认推荐先看 3 套，通常足够比较；如果你只想快速收敛，也可以少一点，如果你想多看一些方向，也可以多一点。`
- Recommend `3` directions by default, but let the user choose the number.
- If the user gives no clear preference on preview count, default to `3` directions.
- Do not expand this step into a parameter form.
- If the user allows the stylized route, do not branch into extra subtype questions there; let the agent design the concrete style directions later in the proposal stage.
- If the user does not clearly answer the route question, default to `常规专业路线`.
- If the brightness answer is missing or ambiguous, default to a middle brightness tendency unless the deck context strongly suggests bright or dark.
- The proposal card is the user-facing interface; it must stay readable and comparable.
- For the style-preview stage, use the bundled HTML shell at `assets/preview_shell/index.html` as the required base UI. Fill or copy that shell; do not invent a replacement preview page, a lookalike shell, or a fresh preview interface from scratch.
- For the optional final multi-candidate selection stage, use the bundled HTML shell at `assets/candidate_picker_shell/index.html` as the required base UI. Fill or copy that shell; do not invent a replacement candidate-picker page, a lookalike shell, or a fresh selection interface from scratch.
- For the final review-and-retouch stage, use the bundled HTML shell at `assets/review_shell/index.html` as the required base UI. Fill or copy that shell; do not invent a replacement review page, a lookalike shell, or a fresh review interface from scratch.
- The rule against rigid design templates applies to PPT visual style generation, not to these workflow UI shells. The bundled preview / candidate-picker / review shells are mandatory workflow assets.
- Only depart from those bundled shells if the relevant asset file is genuinely unavailable or the user explicitly asks for a different interface. In that case, say so clearly instead of silently substituting a self-created shell.
- The preview set for each style must include exactly 3 pages: `首页`, `目录页`, `正文页`.
- All preview images and final page visuals must use a `16:9` slide ratio by default unless the user explicitly requests another presentation ratio.
- In this skill, a preview means an **actual generated image preview by default**, not a text sketch, not ASCII wireframe, and not a verbal mockup.
- Treat previews as directional comparison outputs, not polished finals.
- Within one style direction, the `首页 / 目录页 / 正文页` previews must share one clearly continuous visual system rather than looking like 3 separate template families.
- After a style direction is confirmed, do not jump straight from the raw prompt or proposal text into planning files. First run a short `风格反演确认` stage on the chosen `首页 / 目录页 / 正文页`.
- In that stage, read the selected preview images together with the original generation prompt, extract the stable visual facts and theme-specific liked elements that the user may actually be responding to, and turn them into tighter downstream constraints.
- Separate the reverse-engineered findings into 3 groups: `(1) 明确应延续的`, `(2) 效果好但需要用户确认是否整套延续的`, `(3) 只在当前图里偶然成立、不建议直接锁死的`.
- Use the user-confirmed result of that stage, not just the original prompt wording, as the source for the later deck-level continuity anchor.
- After that confirmation, convert the chosen direction into a deck-level continuity anchor that every later slide must inherit.
- That continuity anchor must explicitly hold steady the deck's base brightness tendency, palette roles, lighting logic, material language, container grammar, decoration grammar, emphasis tone, restraint level, and any user-confirmed thematic anchors or recurring motifs extracted from the preview evidence.
- Do not let later slides drift into a different brightness world or background mood while still claiming to be the same style direction.
- Preview pages must be content-bearing enough to judge. Do not use placeholder text, blank title fields, empty dashboard shells, or mostly decorative structures with little real information inside.
- Once the image-generation path is confirmed, generate the full preview set with minimal intermediate checking and avoid repeated spot-check/regenerate loops unless something is clearly broken.
- Style confirmation should default to **preview-first**, not text-only selection.
- Before final `风格确认`, allow iterative style refinement rounds.
- In a refinement round, let the user pick one current direction as the base, then first do a short refinement-time `风格反演确认` on that base direction before deriving more options from it.
- Use that refinement-time inversion to clarify what the generated images actually expressed and what should be inherited into the next variations.
- Then derive another user-requested number of candidate variations from that base.
- If the user gives no clear count for a refinement round, default to `3` derived variations.
- In each refinement round, proactively offer a few user-friendly tweak prompts such as `对比度高一点`, `色彩再鲜艳一点`, `更克制一点`, `更有高级感一点`, `信息感更强一点`, `画面更轻一点`, or `文字多一点还是图片多一点` so the user can react to concrete adjustment directions.
- Treat those prompts as guidance aids, not as a fixed option menu.
- When you present a refinement round result, explicitly tell the user there are 2 valid next paths: `继续沿某个方向再推` or `就以当前某个方向结束风格阶段`.
- Do not frame the refinement result as if the only next step is to choose a style and immediately enter final PPT generation.
- If previews cannot be generated yet, explicitly tell the user that preview generation is available and state what is currently blocking it.
- Do not ask the user to choose a final style direction without either showing real preview images or clearly explaining why real previews are temporarily unavailable.
- Do not substitute text mockups for preview images unless the user explicitly asks for rough text-only examples.
- After filling the preview HTML shell with the proposal cards and preview images, immediately attempt to open that local HTML page for the user with an environment-appropriate local command instead of only giving them a file path.
- Treat opening the preview page as part of the preview workflow, not as an optional follow-up.
- If automatic opening fails, say that explicitly, tell the user what blocked it, and then provide the file path as fallback.
- Do not write `slide_blueprint.md` before the style direction is confirmed.
- In the final generation stage, keep the workflow image-first.
- Right before the first full generation pass, explicitly ask whether the user wants one final image per slide or multiple final candidates per slide.
- If the user chooses the multi-candidate path, generate `n` candidates for each slide with the same approved page prompt rather than mixing different prompts for that page.
- After multi-candidate generation, assemble the bundled `assets/candidate_picker_shell/index.html`, open it for the user, and tell them to use the page's `复制全部编号` button and paste the copied codes back into the chat input.
- In that multi-candidate stage, do not skip directly to the final review HTML before the user has returned the chosen candidate codes.
- Once the user returns the chosen codes, map them to the selected page images first, then use that chosen set as the input to the final review-and-retouch stage.
- If the user chooses the single-candidate path, skip the candidate-picker stage and go directly to the final review HTML.
- When the confirmed direction depends on generated page visuals, you must use an available image-generation path from the environment such as a tool, MCP server, or skill to produce those visuals.
- Do not hand-draw the final page visuals yourself with code, PPT primitives, SVG-like reconstruction, programmatic shape composition, or ordinary layout boxes as a substitute for image generation.
- Do not silently fall back to a traditional shape-by-shape PPT build or to textless/background-only generated art when the confirmed direction depends on generated page visuals.
- Treat each generated page visual as complete by default rather than as a background plate awaiting further design.
- Post-generation overlays should default to zero.
- Do not use generated images as simple background plates and then freely add your own editable titles, metrics, bullets, labels, callouts, captions, badges, page ornaments, or decorative layers on top unless those additions are already grounded in the confirmed slide content and explicitly traceable to approved blueprint fields.
- Do not add explanatory boxes, correction boxes, patch text, or rescue text just because part of the generated page feels awkward, sparse, or imperfect.
- If generation constraints force a tradeoff between editable text and visual fidelity, surface that tradeoff explicitly instead of changing strategy on your own.
- After the first full set of page visuals is generated, assemble a dedicated review HTML using the same visual language as the preview shell and treat that HTML as the main review surface instead of the live PPT.
- Immediately attempt to open that review HTML for the user.
- When the review HTML is shown, explicitly tell the user: if they are satisfied, they can say so and the workflow can end the review; if they are not satisfied, they should click the review page's `复制当前页结果` or `复制全部页面结果` button and paste the copied JSON directly into the chat input box.
- When telling the user how to paste, use concrete wording such as `复制后，回到对话输入框，把内容粘贴进去再发送` rather than vague wording.
- In review-and-retouch rounds, classify requests into `full-page regeneration`, `local image edit`, or `content/blueprint change` before acting.
- Use an available image-editing path from the environment for local fixes to specific regions, text rendering, background elements, spacing, or emphasis.
- Use full-page regeneration when the user wants broader changes to composition, hierarchy, page concept, tone, or overall visual direction.
- Do not solve review feedback by sneaking in unapproved PPT overlays; update the page visual itself unless the approved blueprint explicitly requires editable overlay content.
- After each retouch round, update the review HTML, open it again, and remind the user of the same review rule:满意则结束评审，不满意则复制结果并粘贴到对话输入框里发送.
- Do not export the final PPT immediately after first-pass generation.
- Only after the user confirms that the reviewed pages are satisfactory may you export the final PPT and immediately attempt to open that final PPT for them.
- When exporting the final PPTX, prefer a standards-compliant PPTX writer such as `python-pptx`. Do not use a hand-written minimal OOXML package as the default final delivery path because WPS may reject it.
- For image-first decks, create blank `16:9` slides and place each approved full-slide page image as the slide content unless the approved blueprint explicitly requires editable overlays.
- If the active Python lacks `python-pptx`, search known local Python / conda environments before installing anything; ask the user before installing new dependencies.
- When regenerating specifically for Office/WPS compatibility, name the output clearly, e.g. with `_WPS_compatible.pptx`.
- Before handoff, validate the final PPTX where possible: run `unzip -t`; if LibreOffice / `soffice` is available, run a headless conversion or open probe. If validation fails, regenerate through a standards-compliant PPTX writer before delivering.
- `spec_lock.md` is always the last of the 3 core planning files.

## Output hierarchy

Use these layers consistently:
- `content_report.md` = pre-style content basis / small research-style report that feeds later planning when the user did not provide a complete report-like narrative
- `design_spec.md` = global deck rationale
- `slide_blueprint.md` = page-by-page intent
- `spec_lock.md` = execution constraints

`content_report.md` is an upstream grounding artifact, not a replacement for the 3 core planning files.
The user should usually see summaries, proposal cards, and previews — not raw internal planning files unless explicitly requested.
