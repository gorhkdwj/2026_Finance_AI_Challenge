# 금융 현안 발굴 리서치 — 진행 기록

각 Task 종료 시 맨 아래에 섹션을 덧붙인다. 기존 내용은 고치지 않는다.

관련 문서
- 설계: `docs/superpowers/specs/2026-07-20-financial-problem-research-design.md`
- 계획: `docs/superpowers/plans/2026-07-20-financial-problem-research.md`

---

## Task 1 — 검증 스크립트 구축

- **상태:** 완료
- **산출:** `tools/validate_problems.py`, `tools/samples/valid_sample.md`, `tools/samples/invalid_sample.md`, `tools/samples/malformed_sample.md`, `tools/samples/silent_failure_sample.md`, `tools/samples/heading_edgecase_sample.md`
- **수치:** 정상 픽스처 3항목 PASS / 위반 픽스처 HARD 3건 검출. 코드 리뷰 3회를 거치며 픽스처를 5개로 확장하고, 조용한 실패 경로 4건을 수정: (1) 어긋난 ID 헤딩이 오류 없이 조용히 파싱에서 빠지던 것, (2) 어긋난 헤딩 검출 후 `current`가 리셋되지 않아 직전 정상 블록의 필드가 오염되던 것, (3) 닫히지 않은 코드펜스가 파일 끝까지를 "펜스 안"으로 간주해 이후 문제 블록 전체를 조용히 무시하던 것, (4) 한 블록 안에서 같은 필드를 두 번 쓰면 나중 값이 이전 값을 조용히 덮어쓰고 PASS 처리되던 것.
- **판단:** 발산보다 검증기를 먼저 만들어, 에이전트가 스스로 형식을 교정하게 함. 초기 구현에는 "오류 없이 조용히 넘어가는" 경로가 여러 개 남아 있었고, 이런 경로는 발산 에이전트 6개가 실제로 형식을 어겼을 때 검증기가 이를 놓치고 PASS를 내주는 결과로 이어지므로, 코드 리뷰를 반복해 조용한 실패를 능동적으로 찾아 막는 방식으로 진행함.
- **다음 Task에 넘기는 것:** 근거 URL은 쉼표 구분 다중 값을 허용함. 코드펜스(```) 안의 내용은 파싱에서 완전히 제외되므로 형식 예시는 코드펜스로 감싸면 안전함. 단, 코드펜스는 반드시 닫아야 하며 닫히지 않으면 HARD 오류로 검출됨. ID 헤딩은 `### P{1-6}-{2자리}` 형식을 엄격히 요구하며, 자리수 부족(`### P1-1`)이나 부가 텍스트(`### P1-01: 제목`)는 HARD 오류로 검출됨. 한 블록 안에 같은 필드를 두 번 쓰면 HARD 오류로 검출됨.

## Task 2 — 리서치 헌장 작성

- **상태:** 완료
- **산출:** `docs/research/00-research-brief.md`, `docs/research/prompts/divergent-template.md`
- **수치:** 헌장 101줄 (상한 140줄)
- **판단:** 브리프의 헌장 본문과 프롬프트 템플릿 내용은 그대로 옮겨 적었고, Task 1에서 추가로 확정된 검증기 동작(코드펜스 닫힘 필수, 어긋난 ID 헤딩 검출, 블록 내 필드 중복 검출) 두 줄만 §8에 덧붙였다. 헌장을 실제 검증기(`tools/validate_problems.py`)로 직접 돌려 `검사 대상: 0개 항목` / `PASS`를 확인함으로써, 헌장 안의 형식 예시(§4)와 요약 블록 규약(§8)이 검증기에 의해 실제 문제 항목으로 오인되지 않음을 실증했다. 이는 문서만 읽고 "형식이 맞겠지" 추정하는 대신, 다음 단계에서 6개 발산 에이전트가 동시에 이 헌장을 프롬프트에 삽입해 쓸 때 자기 파일이 아니라 헌장 자체 때문에 검증이 오염될 위험을 사전에 차단하기 위함이다.
- **다음 Task에 넘기는 것:** 헌장(`00-research-brief.md`)과 템플릿(`divergent-template.md`) 모두 검증기로 실측 검증되어 `검사 대상: 0개 항목` / `PASS` / `exit=0`임을 확인함 — 두 문서를 발산 에이전트 프롬프트에 그대로 삽입해도 검증기가 문서 내 예시를 실제 문제 항목으로 오인하지 않는다. 다음 Task(발산 에이전트 실행/오케스트레이션)에서는 `divergent-template.md`의 5개 플레이스홀더(`{{AXIS_ID}}` `{{AXIS_NAME}}` `{{AXIS_SCOPE}}` `{{MIN_COUNT}}` `{{OUTPUT_PATH}}`)와 `{{RESEARCH_BRIEF}}`(헌장 전문)를 채워 6개 축(P1~P6, §6 표 기준 최소 산출 개수 상이)에 대해 서브에이전트를 병렬 실행하면 된다. 각 에이전트는 산출 후 `python tools/validate_problems.py {산출파일} --min {최소개수}`로 자체 검증하도록 템플릿에 이미 지시되어 있다.
