# 금융 현안 발굴 리서치 실행 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 2026 금융 AI Challenge에 제출할 주제를 정하기 위한 전 단계로, 근거가 검증된 금융 현안 3~5개 영역을 도출한다.

**Architecture:** 6개 축으로 병렬 발산하여 문제를 대량 수집하고, 근거 등급 판정·반증 탐색·URL 실증으로 걸러낸 뒤, 6축 가중 스코어링으로 우선순위를 매겨 유망 문제 영역을 선정한다. 산출물은 전부 마크다운 문서이며, 스키마 준수 여부는 Python 검증 스크립트로 기계 검사한다.

**Tech Stack:** Markdown (산출물), Python 3 표준 라이브러리 (검증 스크립트), Claude Agent 병렬 서브에이전트 (발산·검증 실행), Git (이력 관리)

**설계 문서:** `docs/superpowers/specs/2026-07-20-financial-problem-research-design.md`

## Global Constraints

- **해결책 서술 금지** — 발산·검증·평가 전 단계에서 "AI로 ~하면 된다", 기술 스택, 서비스/기능 아이디어를 산출물에 쓰지 않는다. 오직 "무엇이 잘못되어 있는가"만 기술한다.
- **근거 URL 필수** — 모든 문제 항목에 최소 1개의 출처 URL. 없으면 항목 폐기.
- **문제 한줄 템플릿 고정** — `[누가] [어떤 상황에서] [무엇 때문에] [어떤 손해·불편을 겪는다]`
- **필드 값은 한 줄** — 파싱 가능성을 위해 모든 스키마 필드 값은 개행 없이 한 줄로 작성한다.
- **ID 형식 고정** — `P{축번호 1~6}-{2자리 일련번호}` (예: `P1-01`)
- **일자 고정 없음** — 각 Task는 완료 게이트 충족 시 종료, 중단 조건 도달 시 미완이어도 강제 종료.
- **Phase 3(검증)은 생략 불가** — 시간이 부족하면 발산 산출량을 줄이되 검증 절차는 유지한다.
- **커밋 단위** — 각 Task 종료 시 반드시 커밋. 원격은 `origin/main`.

## File Structure

| 파일 | 책임 |
|---|---|
| `docs/research/00-research-brief.md` | 리서치 헌장. 스키마·금지사항·축 정의의 단일 출처(Single Source of Truth). 모든 에이전트 프롬프트에 전문 삽입됨 |
| `docs/research/prompts/divergent-template.md` | 발산 에이전트 공통 프롬프트 템플릿. 축별 지시만 갈아끼움 |
| `docs/research/01-divergent/p{1..6}-*.md` | 축별 문제 발굴 원본. 각 파일은 해당 축의 산출물만 담음 |
| `docs/research/02-problem-pool.md` | 6축 통합 + 중복 제거된 문제 풀 |
| `docs/research/03-problem-validation.md` | 근거 등급·반증 탐색·URL 실증 결과 |
| `docs/research/04-priority-matrix.md` | 6축 가중 스코어링 표 |
| `docs/research/05-shortlist.md` | 최종 유망 문제 영역 3~5개 + 문제 정의서 |
| `docs/research/PROGRESS.md` | 단계별 진행 누적 기록. 팀원이 이 파일 하나만 보면 전체 흐름을 파악할 수 있게 함 |
| `tools/validate_problems.py` | 스키마 준수·URL 도달성 기계 검증. 80개 항목 수작업 검사를 대체 |
| `tools/samples/valid_sample.md` | 검증기 정상 케이스 픽스처 |
| `tools/samples/invalid_sample.md` | 검증기 위반 케이스 픽스처 |

---

## 문서 규약: 요약 블록과 진행 보고서

`01-divergent/*.md`, `02-problem-pool.md`, `03-problem-validation.md`는 기계가 소비하는 데이터 파일이다. 사람이 통독할 수 없으므로 **각 파일 최상단에 요약 블록을 둔다.**

### 요약 블록 형식

```markdown
# {문서 제목}

## 한눈에 보기

- **항목 수:** N개
- **주요 패턴:** [반복 관찰된 경향 2~3개, 각 한 줄]
- **특이 사항:** [예상 밖 발견, 근거가 유독 강하거나 약한 지점]
- **다음 단계 유의점:** [다음 Task 담당자가 알아야 할 것]

---

### P1-01
- 문제 한줄: ...
```

**위치 규칙 (필수):** 요약 블록은 **첫 번째 `### P` 헤딩보다 반드시 앞**에 온다.

검증기는 `### P{1-6}-{2자리}` 헤딩을 만난 뒤부터 `- 키: 값` 줄을 필드로 수집한다. 요약 블록이 첫 문제 블록 뒤에 오면 `- 항목 수: 18개` 같은 줄이 **그 문제의 필드로 잘못 흡수된다.** 앞에 두면 `current is None` 상태라 전부 무시되므로 안전하다.

또한 요약 블록 안에서 `### P1-01` 형태의 문자열을 예시로 쓰지 않는다. 헤딩으로 오인되어 빈 문제 블록이 생긴다.

### PROGRESS.md 형식

각 Task가 끝날 때 **맨 아래에 한 섹션을 덧붙인다.** 기존 내용을 고치지 않는다 — 진행 기록은 누적이지 갱신이 아니다.

```markdown
## Task N — {Task 이름}

- **상태:** 완료 / 중단(사유)
- **산출:** [생성·수정된 파일 경로]
- **수치:** [개수, 통과/탈락 건수 등 정량 결과]
- **판단:** [이 단계에서 내린 결정과 그 이유. 특히 무언가를 잘라냈다면 왜]
- **다음 Task에 넘기는 것:** [주의사항, 미해결 이슈]
```

`판단` 항목이 핵심이다. 나중에 "왜 이 문제를 뺐지?"라는 질문이 반드시 나오는데, 그때 근거가 남아 있어야 한다.

---

## Task 1: 검증 스크립트 구축

**목적:** 발산 단계가 끝난 뒤에 형식 오류를 발견하면 6축 전체를 다시 돌려야 한다. 검증기를 **먼저** 만들어 두고, 발산 에이전트에게 "이 검증기를 통과하는 형식으로 써라"고 지시한다.

**Files:**
- Create: `tools/validate_problems.py`
- Create: `tools/samples/valid_sample.md`
- Create: `tools/samples/invalid_sample.md`

**Interfaces:**
- Consumes: 없음 (첫 Task)
- Produces:
  - CLI: `python tools/validate_problems.py <경로...> [--check-urls] [--min N]`
  - 종료 코드: `0` = HARD 오류 없음, `1` = HARD 오류 있음
  - 문제 블록 형식(이후 모든 Task가 이 형식을 따름):
    ```
    ### P1-01
    - 문제 한줄: ...
    - 당사자: ...
    - 발생 맥락: ...
    - 피해 규모: ...
    - 현재 대응: ...
    - 근거 URL: https://...
    - 관련 업권: 은행
    ```

- [ ] **Step 1: Python 실행 가능 여부 확인**

```bash
python --version
```

기대: `Python 3.x.x` 출력. `python`이 없으면 `python3 --version`을 쓰고, 이후 모든 명령에서 `python`을 `python3`로 바꿔 실행한다.

- [ ] **Step 2: 정상 픽스처 작성**

`tools/samples/valid_sample.md`:

```markdown
# 정상 샘플

### P1-01
- 문제 한줄: 개업 1년 미만 요식업 자영업자가 정책자금을 신청할 때 자격 요건이 기관마다 흩어져 있어 신청 가능한 상품을 놓친다
- 당사자: 개업 1년 미만 요식업 자영업자
- 발생 맥락: 정책자금 공고 확인 및 신청 준비 시점
- 피해 규모: 수치없음
- 현재 대응: 소상공인시장진흥공단 상담센터 전화 문의에 의존
- 근거 URL: https://www.semas.or.kr/
- 관련 업권: 은행

### P1-02
- 문제 한줄: 국내 체류 6개월 미만 외국인이 은행 계좌를 개설할 때 서류 요건을 사전에 알 수 없어 영업점을 반복 방문한다
- 당사자: 국내 체류 6개월 미만 외국인 근로자
- 발생 맥락: 은행 영업점 계좌 개설 창구
- 피해 규모: 수치없음
- 현재 대응: 영업점 직원의 구두 안내
- 근거 URL: https://www.fss.or.kr/
- 관련 업권: 은행

### P1-03
- 문제 한줄: 65세 이상 모바일뱅킹 이용자가 이체 한도를 변경할 때 본인확인 단계를 완료하지 못해 영업점을 방문해야 한다
- 당사자: 65세 이상 모바일뱅킹 이용자
- 발생 맥락: 모바일뱅킹 이체 한도 변경 화면
- 피해 규모: 수치없음
- 현재 대응: 콜센터 안내 후 영업점 방문 처리
- 근거 URL: https://www.fss.or.kr/, https://www.fsec.or.kr/
- 관련 업권: 은행
```

`P1-03`은 **쉼표 구분 다중 URL**이 통과하는지 확인하기 위한 항목이다. Task 5의 병합 규칙이 URL을 쉼표로 이어 붙이므로, 검증기가 이를 허용해야 한다.

- [ ] **Step 3: 위반 픽스처 작성**

`tools/samples/invalid_sample.md`:

```markdown
# 위반 샘플

### P2-01
- 문제 한줄: 소상공인이 대출을 못 받는다
- 당사자: 소상공인
- 발생 맥락: 대출 신청 시
- 피해 규모: 수치없음
- 현재 대응: 없음
- 관련 업권: 은행

### P2-02
- 문제 한줄: 고령층이 모바일뱅킹을 어려워하므로 AI로 음성 안내를 제공하면 된다
- 당사자: 65세 이상 모바일뱅킹 이용자
- 발생 맥락: 모바일뱅킹 이체 화면
- 피해 규모: 수치없음
- 현재 대응: 콜센터 안내
- 근거 URL: not-a-url
- 관련 업권: 은행

### P2-02
- 문제 한줄: 중복 ID 테스트 항목이며 앞 항목과 동일한 ID를 사용한다
- 당사자: 테스트 대상자
- 발생 맥락: 테스트
- 피해 규모: 수치없음
- 현재 대응: 없음
- 근거 URL: https://example.com/
- 관련 업권: 무관
```

이 파일은 의도적으로 3가지 HARD 오류(P2-01 근거 URL 누락, P2-02 URL 형식 불량, P2-02 ID 중복)와 2가지 WARN(뭉뚱그린 당사자 "소상공인", 해결책 키워드 "AI로")을 담고 있다.

- [ ] **Step 4: 검증 스크립트 작성**

`tools/validate_problems.py`:

```python
#!/usr/bin/env python3
"""금융 현안 문제 스키마 검증기.

사용법:
    python tools/validate_problems.py docs/research/01-divergent/
    python tools/validate_problems.py docs/research/02-problem-pool.md --min 40
    python tools/validate_problems.py docs/research/02-problem-pool.md --check-urls

종료 코드: 0 = HARD 오류 없음 / 1 = HARD 오류 있음
"""
import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REQUIRED_FIELDS = [
    "문제 한줄", "당사자", "발생 맥락",
    "피해 규모", "현재 대응", "근거 URL", "관련 업권",
]

SOLUTION_KEYWORDS = [
    "AI로", "AI를 활용", "LLM", "RAG", "챗봇", "에이전트",
    "플랫폼을", "솔루션", "추천 시스템", "자동화하여",
    "모델을 활용", "서비스를 구축", "앱을 개발", "시스템을 개발",
]

VAGUE_ACTORS = [
    "소상공인", "고객", "사용자", "이용자", "국민",
    "청년", "고령층", "노인", "외국인", "투자자", "기업",
]

VALID_SECTORS = ["은행", "인터넷은행", "증권", "생보", "보안", "무관"]

ID_RE = re.compile(r"^###\s+(P[1-6]-\d{2})\s*$")
FIELD_RE = re.compile(r"^-\s*([^:]+?)\s*:\s*(.+?)\s*$")
URL_RE = re.compile(r"^https?://\S+$")


def parse_file(path):
    """마크다운 파일에서 문제 블록을 파싱한다."""
    problems = []
    current = None
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines, 1):
        match = ID_RE.match(line)
        if match:
            current = {
                "id": match.group(1),
                "file": str(path),
                "line": lineno,
                "fields": {},
            }
            problems.append(current)
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            current["fields"][field.group(1).strip()] = field.group(2).strip()
    return problems


def check_url(url, timeout=10):
    """URL 도달성을 확인한다. (True, 상태) 또는 (False, 사유) 반환."""
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "Mozilla/5.0 (compatible; research-validator/1.0)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - 네트워크 예외 전반을 사유로 기록
        return False, type(exc).__name__


def validate(problems, check_urls=False):
    """문제 목록을 검증하여 (hard_errors, warnings)를 반환한다."""
    hard, warn = [], []
    seen_ids = {}

    for problem in problems:
        pid = problem["id"]
        where = f"{problem['file']}:{problem['line']} [{pid}]"

        if pid in seen_ids:
            hard.append(f"{where} ID 중복 (최초 등장: {seen_ids[pid]})")
        else:
            seen_ids[pid] = where

        for field in REQUIRED_FIELDS:
            if field not in problem["fields"]:
                hard.append(f"{where} 필수 필드 누락: {field}")

        # 근거 URL은 병합 항목을 위해 쉼표 구분 다중 값을 허용한다.
        raw_url = problem["fields"].get("근거 URL", "")
        urls = [u.strip() for u in raw_url.split(",") if u.strip()]
        if raw_url and not urls:
            hard.append(f"{where} 근거 URL 비어 있음")
        for url in urls:
            if not URL_RE.match(url):
                hard.append(f"{where} 근거 URL 형식 불량: {url!r}")
            elif check_urls:
                ok, detail = check_url(url)
                if not ok:
                    hard.append(f"{where} 근거 URL 도달 실패 ({detail}): {url}")

        sector = problem["fields"].get("관련 업권", "")
        if sector and sector not in VALID_SECTORS:
            warn.append(f"{where} 업권 값이 목록 밖: {sector!r}")

        actor = problem["fields"].get("당사자", "")
        if actor in VAGUE_ACTORS:
            warn.append(f"{where} 당사자가 뭉뚱그려짐: {actor!r} — 더 좁힐 것")

        blob = " ".join(problem["fields"].values())
        for keyword in SOLUTION_KEYWORDS:
            if keyword in blob:
                warn.append(f"{where} 해결책 서술 의심 키워드: {keyword!r}")

    return hard, warn


def collect_files(targets):
    """경로 목록에서 검사 대상 마크다운 파일을 모은다."""
    files = []
    for target in targets:
        path = Path(target)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"경로를 찾을 수 없음: {target}", file=sys.stderr)
            sys.exit(1)
    return files


def main():
    parser = argparse.ArgumentParser(description="문제 스키마 검증기")
    parser.add_argument("targets", nargs="+", help="검사할 파일 또는 디렉토리")
    parser.add_argument("--check-urls", action="store_true", help="근거 URL 도달성 확인")
    parser.add_argument("--min", type=int, default=0, help="최소 문제 개수 요구")
    args = parser.parse_args()

    problems = []
    for path in collect_files(args.targets):
        problems.extend(parse_file(path))

    hard, warn = validate(problems, check_urls=args.check_urls)

    if args.min and len(problems) < args.min:
        hard.append(f"문제 개수 미달: {len(problems)}개 (최소 {args.min}개 필요)")

    print(f"== 검사 대상: {len(problems)}개 항목 ==")
    if warn:
        print(f"\n-- WARN {len(warn)}건 --")
        for item in warn:
            print(f"  ! {item}")
    if hard:
        print(f"\n-- HARD {len(hard)}건 --")
        for item in hard:
            print(f"  X {item}")
        print("\n결과: FAIL")
        sys.exit(1)

    print("\n결과: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 정상 픽스처로 PASS 확인**

```bash
python tools/validate_problems.py tools/samples/valid_sample.md
```

기대 출력:
```
== 검사 대상: 3개 항목 ==

결과: PASS
```
기대 종료 코드: `0`
`P1-03`의 다중 URL이 형식 오류로 잡히지 않아야 한다.

- [ ] **Step 6: 위반 픽스처로 FAIL 확인**

```bash
python tools/validate_problems.py tools/samples/invalid_sample.md
```

기대: `HARD 3건` 이상 출력되고 아래 3건이 모두 포함될 것
- `P2-01 필수 필드 누락: 근거 URL`
- `P2-02 근거 URL 형식 불량: 'not-a-url'`
- `P2-02 ID 중복`

그리고 `WARN`에 `당사자가 뭉뚱그려짐: '소상공인'`과 `해결책 서술 의심 키워드: 'AI로'`가 포함될 것.
기대 종료 코드: `1`

- [ ] **Step 7: 최소 개수 옵션 확인**

```bash
python tools/validate_problems.py tools/samples/valid_sample.md --min 5
```

기대: `HARD` 목록에 `문제 개수 미달: 3개 (최소 5개 필요)` 포함, 결과 `FAIL`, 종료 코드 `1`

- [ ] **Step 8: 커밋**

```bash
git add tools/
git commit -m "feat: 문제 스키마 검증 스크립트 추가

- 필수 필드 누락, ID 중복, URL 형식/도달성을 HARD 오류로 판정
- 해결책 키워드, 뭉뚱그린 당사자를 WARN으로 보고
- 정상/위반 픽스처로 동작 검증"
git push
```

---

## Task 2: 리서치 헌장 작성 (Phase 1)

**목적:** 병렬 에이전트 6개가 동시에 움직이므로, 규칙이 프롬프트에 그대로 삽입될 수 있는 단일 문서로 존재해야 한다.

**Files:**
- Create: `docs/research/00-research-brief.md`
- Create: `docs/research/prompts/divergent-template.md`
- Create: `docs/research/PROGRESS.md`
- Create: `docs/research/01-divergent/.gitkeep`

**Interfaces:**
- Consumes: Task 1의 문제 블록 형식
- Produces: `00-research-brief.md` (모든 발산 프롬프트에 전문 삽입되는 헌장), `divergent-template.md` (`{{AXIS_ID}}`, `{{AXIS_NAME}}`, `{{AXIS_SCOPE}}`, `{{MIN_COUNT}}`, `{{OUTPUT_PATH}}` 5개 플레이스홀더를 가진 템플릿)

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p docs/research/01-divergent docs/research/prompts
touch docs/research/01-divergent/.gitkeep
```

- [ ] **Step 2: 리서치 헌장 작성**

`docs/research/00-research-brief.md`:

```markdown
# 리서치 헌장 — 금융 현안 발굴

## 0. 이 문서의 지위
본 문서는 리서치 규칙의 단일 출처다. 모든 발산·검증 에이전트 프롬프트에 **전문이 그대로 삽입**된다. 요약본을 대신 넣지 않는다.

## 1. 이번 리서치가 산출하는 것
**검증된 금융 현안 목록과 우선순위.** "주제"나 "서비스 아이디어"가 아니다.
해결책 설계는 이 리서치가 끝난 뒤 별도 사이클에서 진행한다.

## 2. 대회 제약 (맥락)
- 대회: 2026 금융 AI Challenge (주최·주관 금융보안원 / 후원 금융위원회)
- 공동개최사: 하나은행, 신한은행, 카카오뱅크, KB증권, 생명보험협회
- 마감: 2026-09-07 10:00 (기획서 + 기능명세서 + 웹서비스 URL)
- 데이터 미제공 — 데이터 확보는 참가자 책임
- 1차 심사 기준: **주제 적합성, 부적격 여부**
- 발표 심사: 상위 11팀 내외, 2026-10-13 오프라인

## 3. 절대 금지 사항
1. **해결책·서비스·기능을 서술하지 말 것**
2. **"AI로 ~하면 된다" 류의 서술 금지**
3. **기술 스택·모델·기법 언급 금지** (LLM, RAG, 챗봇, 에이전트, 추천 시스템 등)
4. 오직 **"무엇이 잘못되어 있는가"**만 기술할 것

위반 시 해당 항목은 반려된다. 판단이 서지 않으면 "이 문장이 없어도 문제가 설명되는가?"를 물어보고, 설명된다면 그 문장을 지운다.

## 4. 문제 스키마 (필드 7개, 값은 각각 한 줄)

| 필드 | 규칙 |
|---|---|
| `문제 한줄` | **"[누가] [어떤 상황에서] [무엇 때문에] [어떤 손해·불편을 겪는다]"** 템플릿 준수 |
| `당사자` | 구체적 집단. "소상공인" 금지, "개업 1년 미만 요식업 자영업자" 수준으로 |
| `발생 맥락` | 언제·어디서 발생하는가 |
| `피해 규모` | 정량 수치 + 기준연도. 모르면 `수치없음`이라고만 쓸 것 (추측 금지) |
| `현재 대응` | 지금 어떻게 처리되고 있는가 (수작업 / 부분 해결 / 방치) |
| `근거 URL` | 최소 1개, `http://` 또는 `https://`로 시작하는 완전한 URL. 없으면 항목 폐기 |
| `관련 업권` | `은행` / `인터넷은행` / `증권` / `생보` / `보안` / `무관` 중 택1 |

### 출력 형식 (이 형식을 벗어나면 자동 검증에서 탈락한다)

```
### P1-01
- 문제 한줄: 개업 1년 미만 요식업 자영업자가 정책자금을 신청할 때 자격 요건이 기관마다 흩어져 있어 신청 가능한 상품을 놓친다
- 당사자: 개업 1년 미만 요식업 자영업자
- 발생 맥락: 정책자금 공고 확인 및 신청 준비 시점
- 피해 규모: 수치없음
- 현재 대응: 소상공인시장진흥공단 상담센터 전화 문의에 의존
- 근거 URL: https://www.semas.or.kr/
- 관련 업권: 은행
```

- `ID`는 `P{축번호}-{2자리 일련번호}` (예: `P3-07`)
- 필드 값에 개행을 넣지 말 것
- 필드 순서를 바꾸지 말 것

## 5. 발산 단계 행동 규칙
1. **판단 금지** — 풀기 어렵다는 이유로 스스로 탈락시키지 말 것
2. **해결책 금지** — §3 준수
3. **정량 근거 우선** — 수치 있는 문제를 우선 수집, 없으면 `수치없음` 표기
4. **최소 개수 충족** — 부족하면 축을 더 잘게 쪼개서라도 채울 것
5. **출처 실재 확인** — URL을 실제로 열어본 뒤 인용할 것. 기억에 의존해 URL을 만들어 쓰지 말 것

## 6. 6개 발산 축

| 축 | 조사 대상 | 최소 산출 |
|---|---|---|
| P1 | 공고 세부주제 예시 7개가 전제하는 근본 문제 역추출 + 인접 문제 확장 | 15개 |
| P2 | 업권별 현안 — 업계 리포트, 협회 자료, 금융지주 IR·연차보고서의 리스크 언급 | 15개 |
| P3 | 소비자 페르소나별 페인포인트 — 금융민원 통계, 소비자원 상담 사례, 실태조사 | 15개 |
| P4 | 채널·프로세스 마찰 — 창구/앱/콜센터/오픈뱅킹에서 사용자가 이탈·실패하는 지점 | 10개 |
| P5 | 감독당국·정책이 공식 지목한 문제 — 금융위·금감원·금융보안원 보도자료, 국정과제, 제재·지적 사항 | 15개 |
| P6 | 사고·피해·손실 통계 — 보이스피싱, 보험사기, 금융사기, 디지털 소외 실태 | 10개 |

축 간 중복은 허용한다. 여러 축에서 독립적으로 도출된 문제는 실재성이 높다는 신호로 취급한다.

## 7. 참고: 대회 공고의 세부주제 예시 7개
1. 창업기업 및 신규 소상공인을 위한 AI 맞춤형 금융 매칭 서비스
2. 국내 체류 외국인 고객의 금융 정착을 돕는 AI Agent
3. 보이스피싱 등 이상금융거래 탐지 시 맞춤형 행동 요령을 제공하는 AI 금융 보안 비서
4. AI와 비정형 데이터 분석을 통한 혁신·벤처기업의 다차원 성장성 평가 및 투자 매칭 플랫폼
5. 청년층 자산 형성 및 고령층·장애인 디지털 격차 해소를 위한 AI 기반 포용적 금융서비스
6. 이상금융거래 및 보험사기 등을 AI로 분석하여 탐지할 수 있는 서비스
7. 프론티어 AI 공격 방어를 위한 대화형 AI 보안 대응 비서

**주의:** 위 7개는 이미 해결책 형태로 서술되어 있다. 그대로 베끼지 말고, 각각이 **전제하고 있는 문제**가 무엇인지 역추출하는 데 사용한다.
```

- [ ] **Step 3: 발산 프롬프트 템플릿 작성**

`docs/research/prompts/divergent-template.md`:

```markdown
# 발산 에이전트 프롬프트 템플릿

사용법: 아래 플레이스홀더 5개를 축별 값으로 치환하고, `{{RESEARCH_BRIEF}}` 자리에
`docs/research/00-research-brief.md` **전문**을 붙여넣어 서브에이전트에 전달한다.

- `{{AXIS_ID}}` — 축 번호 (예: `P1`)
- `{{AXIS_NAME}}` — 축 이름 (예: `공고 예시 역추출`)
- `{{AXIS_SCOPE}}` — 이 축이 조사할 범위 서술
- `{{MIN_COUNT}}` — 최소 산출 개수
- `{{OUTPUT_PATH}}` — 산출 파일 경로

---

## 프롬프트 본문

당신은 2026 금융 AI Challenge 참가팀의 리서처다.
당신의 임무는 **한국 금융 분야의 실재하는 문제를 발굴하는 것**이며,
**해결책을 제안하는 것이 아니다.**

담당 축: **{{AXIS_ID}} — {{AXIS_NAME}}**
조사 범위: {{AXIS_SCOPE}}
최소 산출: **{{MIN_COUNT}}개**
산출 파일: `{{OUTPUT_PATH}}`

### 반드시 지킬 것
1. 아래 리서치 헌장의 **§3 절대 금지 사항**과 **§4 출력 형식**을 그대로 따른다.
2. 웹 검색을 사용해 실제 출처를 찾는다. **URL을 기억에서 만들어 쓰지 않는다.**
   인용하려는 페이지를 실제로 열어 내용이 주장과 일치하는지 확인한다.
3. 최소 산출 개수를 채운다. 부족하면 축을 더 잘게 쪼개서라도 채운다.
4. **판단하지 않는다.** "이건 풀기 어렵겠다", "이건 이미 해결됐겠다" 같은 이유로
   항목을 스스로 빼지 않는다. 걸러내는 일은 다음 단계에서 한다.
5. 검색은 한국어 자료를 우선한다. 감독기관·협회·연구기관 자료를 언론 기사보다 우선한다.

### 산출 방법
`{{OUTPUT_PATH}}` 파일을 생성하고, 첫 줄에 `# {{AXIS_ID}} — {{AXIS_NAME}}`을 쓴 뒤
문제 블록을 이어서 작성한다. ID는 `{{AXIS_ID}}-01`부터 순번을 매긴다.

### 자체 검증
작성을 마치면 아래를 실행하고 `PASS`가 나올 때까지 수정한다.

```bash
python tools/validate_problems.py {{OUTPUT_PATH}} --min {{MIN_COUNT}}
```

`WARN`은 무시해도 되지만, `해결책 서술 의심 키워드` 경고는 반드시 확인하고
해당 문장이 해결책을 서술하고 있으면 지운다.

### 최종 보고
파일 경로와 작성한 문제 개수만 한 줄로 보고한다. 문제 내용을 본문에 반복하지 않는다.

---

## 리서치 헌장 (전문)

{{RESEARCH_BRIEF}}
```

- [ ] **Step 3-1: 헌장에 요약 블록 규약 추가**

`00-research-brief.md` 끝에 아래 섹션을 덧붙인다. 발산 에이전트가 요약 블록을 잘못된 위치에 넣으면 검증기가 깨지므로, 헌장에 못을 박아둔다.

```markdown
## 8. 요약 블록 (필수)

산출 파일 최상단에 아래 블록을 넣는다.

- **항목 수:** N개
- **주요 패턴:** [반복 관찰된 경향 2~3개, 각 한 줄]
- **특이 사항:** [예상 밖 발견, 근거가 유독 강하거나 약한 지점]
- **다음 단계 유의점:** [다음 담당자가 알아야 할 것]

**위치 규칙:** 요약 블록은 **첫 번째 문제 블록 헤딩보다 반드시 앞**에 온다.
뒤에 오면 요약의 `- 항목 수: N개` 줄이 직전 문제의 필드로 잘못 흡수되어
검증에 실패한다. 또한 요약 블록 안에서 `P1-01` 형태의 문자열을
세 번째 수준 헤딩(`###`)으로 쓰지 않는다.
```

- [ ] **Step 3-2: 진행 보고서 생성**

`docs/research/PROGRESS.md`:

```markdown
# 금융 현안 발굴 리서치 — 진행 기록

각 Task 종료 시 맨 아래에 섹션을 덧붙인다. 기존 내용은 고치지 않는다.

관련 문서
- 설계: `docs/superpowers/specs/2026-07-20-financial-problem-research-design.md`
- 계획: `docs/superpowers/plans/2026-07-20-financial-problem-research.md`

---

## Task 1 — 검증 스크립트 구축

- **상태:** 완료
- **산출:** `tools/validate_problems.py`, `tools/samples/valid_sample.md`, `tools/samples/invalid_sample.md`
- **수치:** 정상 픽스처 3항목 PASS / 위반 픽스처 HARD 3건 검출
- **판단:** 발산보다 검증기를 먼저 만들어, 에이전트가 스스로 형식을 교정하게 함
- **다음 Task에 넘기는 것:** 근거 URL은 쉼표 구분 다중 값을 허용함

## Task 2 — 리서치 헌장 작성

- **상태:** 완료
- **산출:** `docs/research/00-research-brief.md`, `docs/research/prompts/divergent-template.md`
- **수치:** 헌장 N줄 (상한 120줄)
- **판단:** [작성 시 기록]
- **다음 Task에 넘기는 것:** [작성 시 기록]
```

- [ ] **Step 4: 헌장 분량 확인 (중단 조건)**

```bash
wc -l docs/research/00-research-brief.md
```

기대: 140줄 이하 (§8 요약 블록 규약 포함). 초과 시 §7 참고 섹션부터 축약한다. 에이전트가 읽지 않을 분량이면 없는 것과 같다.

- [ ] **Step 5: 완료 게이트 확인**

다음을 눈으로 확인한다.
- [ ] `00-research-brief.md`에 스키마 7개 필드가 표로 명문화되어 있다
- [ ] `00-research-brief.md`에 금지 사항 4개가 §3에 명문화되어 있다
- [ ] `00-research-brief.md`에 출력 형식 예시 블록이 포함되어 있다 (요약본 아님)
- [ ] `00-research-brief.md` §8에 요약 블록 형식과 **위치 규칙**이 명시되어 있다
- [ ] `divergent-template.md`에 플레이스홀더 5개(`{{AXIS_ID}}` `{{AXIS_NAME}}` `{{AXIS_SCOPE}}` `{{MIN_COUNT}}` `{{OUTPUT_PATH}}`)와 `{{RESEARCH_BRIEF}}`가 모두 존재한다
- [ ] `PROGRESS.md`에 Task 1·2 섹션이 기록되어 있고, Task 2의 `판단`·`다음 Task에 넘기는 것`이 실제 내용으로 채워져 있다

- [ ] **Step 6: 커밋**

```bash
git add docs/research/
git commit -m "docs: 리서치 헌장 및 발산 프롬프트 템플릿 작성

- 스키마 7필드, 금지사항 4개, 출력형식을 단일 출처로 고정
- 요약 블록 위치 규칙 명시 (검증기 파싱 충돌 방지)
- 발산 에이전트 공통 프롬프트 템플릿 (플레이스홀더 5개)
- 진행 기록 PROGRESS.md 신설"
git push
```

---

## Task 3: 발산 축 P1~P3 실행

**목적:** 3개 축을 먼저 돌려 산출물 형식과 품질을 확인한다. 6개를 한꺼번에 돌리고 나서 형식 문제를 발견하면 전량 재작업이 된다.

**Files:**
- Create: `docs/research/01-divergent/p1-notice-reverse.md`
- Create: `docs/research/01-divergent/p2-industry.md`
- Create: `docs/research/01-divergent/p3-persona.md`

**Interfaces:**
- Consumes: `docs/research/00-research-brief.md`, `docs/research/prompts/divergent-template.md`, `tools/validate_problems.py`
- Produces: P1/P2/P3 문제 블록 (ID 접두사 `P1-` `P2-` `P3-`), 합계 45개 이상

- [ ] **Step 1: 축별 프롬프트 3개 조립**

`divergent-template.md`의 플레이스홀더를 아래 값으로 치환하고, `{{RESEARCH_BRIEF}}` 자리에 `00-research-brief.md` 전문을 붙인다.

| | P1 | P2 | P3 |
|---|---|---|---|
| `{{AXIS_ID}}` | `P1` | `P2` | `P3` |
| `{{AXIS_NAME}}` | 공고 예시 역추출 | 업권별 현안 | 소비자 페르소나 페인포인트 |
| `{{MIN_COUNT}}` | `15` | `15` | `15` |
| `{{OUTPUT_PATH}}` | `docs/research/01-divergent/p1-notice-reverse.md` | `docs/research/01-divergent/p2-industry.md` | `docs/research/01-divergent/p3-persona.md` |

`{{AXIS_SCOPE}}` 값:

- **P1:** 헌장 §7의 세부주제 예시 7개를 하나씩 검토하여, 각 예시가 **전제하고 있는 근본 문제**를 역추출한다. 그 다음 각 문제의 인접 문제(같은 당사자의 다른 불편, 같은 상황의 다른 실패 지점)를 확장한다. 예시 문구를 그대로 베끼지 않는다.
- **P2:** 은행 / 인터넷전문은행 / 증권 / 생명보험 / 금융보안 5개 업권을 각각 조사한다. 금융지주·주요 금융사의 사업보고서·IR 자료에 서술된 리스크 요인, 업권 협회(은행연합회, 금융투자협회, 생명보험협회)의 발간물, 금융연구원·보험연구원·자본시장연구원의 최근 보고서에서 업계가 스스로 문제라고 인정한 지점을 찾는다.
- **P3:** 청년(사회초년생) / 고령층(65세 이상) / 장애인 / 국내 체류 외국인 / 신규 창업자 / 자영업자 6개 페르소나를 각각 조사한다. 금융감독원 금융민원 통계, 한국소비자원 상담·피해구제 사례, 금융위·통계청의 금융이해력 및 접근성 실태조사에서 실제 접수된 불편을 찾는다.

- [ ] **Step 2: 서브에이전트 3개 병렬 실행**

3개 프롬프트를 **한 메시지에서 동시에** 디스패치한다. 순차 실행하면 3배 걸린다.

- [ ] **Step 3: 산출 파일 존재 확인**

```bash
ls -la docs/research/01-divergent/
```

기대: `p1-notice-reverse.md`, `p2-industry.md`, `p3-persona.md` 3개 파일 존재

- [ ] **Step 4: 축별 스키마 검증**

```bash
python tools/validate_problems.py docs/research/01-divergent/p1-notice-reverse.md --min 15
python tools/validate_problems.py docs/research/01-divergent/p2-industry.md --min 15
python tools/validate_problems.py docs/research/01-divergent/p3-persona.md --min 15
```

기대: 3개 모두 `결과: PASS`, 종료 코드 `0`
`FAIL`이면 해당 축 에이전트에게 오류 목록을 그대로 전달하여 수정시킨다.

- [ ] **Step 5: 해결책 누출 육안 점검**

검증기의 `WARN` 중 `해결책 서술 의심 키워드` 항목을 전부 열어본다. 실제로 해결책을 서술한 문장이면 지운다. (예: "~를 안내하는 서비스가 필요하다"는 해결책이므로 삭제, "~에 대한 안내가 없다"는 문제 서술이므로 유지)

- [ ] **Step 6: 품질 샘플 점검**

각 축에서 임의로 2개씩, 총 6개 항목을 골라 아래를 확인한다.
- [ ] `근거 URL`을 실제로 열었을 때 페이지가 존재하고, 내용이 `문제 한줄`의 주장을 뒷받침한다
- [ ] `당사자`가 뭉뚱그려지지 않았다
- [ ] `문제 한줄`이 템플릿(누가/어떤 상황에서/무엇 때문에/어떤 손해)을 지킨다

한 건이라도 URL이 내용과 불일치하면, 해당 축 전체를 재검토 대상으로 본다. 환각은 대개 단발이 아니다.

- [ ] **Step 6-1: 요약 블록 확인 및 보완**

P1/P2/P3 각 파일 최상단에 요약 블록이 있는지 확인한다. 에이전트가 빠뜨렸으면 직접 작성한다. 항목은 `항목 수` / `주요 패턴` / `특이 사항` / `다음 단계 유의점` 4가지다.

위치를 반드시 확인한다.

```bash
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p1-notice-reverse.md | head -5
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p2-industry.md | head -5
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p3-persona.md | head -5
```

기대: 각 파일에서 `한눈에 보기`의 줄 번호가 첫 `### P` 줄 번호보다 **작을 것**. 크면 요약이 문제 블록 뒤에 있다는 뜻이므로 앞으로 옮기고 Step 4 검증을 다시 돌린다.

- [ ] **Step 6-2: 진행 기록 추가**

`docs/research/PROGRESS.md` 맨 아래에 덧붙인다.

```markdown
## Task 3 — 발산 축 P1~P3

- **상태:** 완료
- **산출:** `docs/research/01-divergent/p1-notice-reverse.md`, `p2-industry.md`, `p3-persona.md`
- **수치:** P1 N개 / P2 N개 / P3 N개 (합계 N개), 스키마 검증 PASS
- **판단:** [해결책 누출로 삭제한 문장 수, 프롬프트를 보완했다면 그 내용과 이유]
- **다음 Task에 넘기는 것:** [P4~P6 실행 시 반영할 프롬프트 수정 사항. 없으면 "없음"]
```

- [ ] **Step 7: 커밋**

```bash
git add docs/research/
git commit -m "docs: 발산 축 P1~P3 문제 발굴 결과

- P1 공고 예시 역추출 / P2 업권별 현안 / P3 페르소나 페인포인트
- 스키마 검증 통과, 샘플 URL 실증 확인"
git push
```

---

## Task 4: 발산 축 P4~P6 실행

**목적:** Task 3에서 형식·품질이 확인된 프롬프트로 나머지 3축을 돌린다. Task 3에서 프롬프트 보완이 필요했다면 그 수정을 반영한 뒤 실행한다.

**Files:**
- Create: `docs/research/01-divergent/p4-channel.md`
- Create: `docs/research/01-divergent/p5-regulator.md`
- Create: `docs/research/01-divergent/p6-loss-stats.md`

**Interfaces:**
- Consumes: Task 2의 헌장·템플릿, Task 3에서 확인된 프롬프트 보완 사항
- Produces: P4/P5/P6 문제 블록 (ID 접두사 `P4-` `P5-` `P6-`), 합계 35개 이상

- [ ] **Step 1: Task 3 피드백 반영**

Task 3에서 프롬프트를 보완했다면(예: 특정 지시가 무시됨, 형식 이탈 반복) 그 수정을 `divergent-template.md`에 반영한다. 보완할 것이 없으면 이 단계를 건너뛴다.

- [ ] **Step 2: 축별 프롬프트 3개 조립**

| | P4 | P5 | P6 |
|---|---|---|---|
| `{{AXIS_ID}}` | `P4` | `P5` | `P6` |
| `{{AXIS_NAME}}` | 채널·프로세스 마찰 | 감독당국 지목 문제 | 사고·피해 통계 |
| `{{MIN_COUNT}}` | `10` | `15` | `10` |
| `{{OUTPUT_PATH}}` | `docs/research/01-divergent/p4-channel.md` | `docs/research/01-divergent/p5-regulator.md` | `docs/research/01-divergent/p6-loss-stats.md` |

`{{AXIS_SCOPE}}` 값:

- **P4:** 영업점 창구 / 모바일 앱 / 인터넷뱅킹 / 콜센터·ARS / 오픈뱅킹 / 마이데이터 6개 채널을 각각 조사한다. 각 채널에서 이용자가 **중도 이탈하거나 업무를 완료하지 못하는 지점**을 찾는다. 금융회사 민원 공시, 소비자보호 실태평가 결과, 접근성 실태조사에서 근거를 찾는다.
- **P5:** 금융위원회·금융감독원·금융보안원이 **공식 문서에서 직접 문제라고 지목한 사안**만 수집한다. 보도자료, 정책 추진 계획, 감독·검사 결과 발표, 제재 및 개선 요구 사항, 국정과제 관련 금융 분야 항목을 대상으로 한다. 기관이 문제로 규정한 표현을 가능한 한 그대로 인용한다.
- **P6:** 보이스피싱·전기통신금융사기 / 보험사기 / 이상금융거래 / 불완전판매 / 금융 디지털 소외 5개 영역의 **피해·손실 통계**를 수집한다. 금융감독원 및 경찰청 발표 통계, 금융보안원 보고서, 보험개발원·보험연구원 자료를 우선한다. **모든 항목에 연도가 명시된 정량 수치를 포함시킨다.**

- [ ] **Step 3: 서브에이전트 3개 병렬 실행**

3개 프롬프트를 한 메시지에서 동시에 디스패치한다.

- [ ] **Step 4: 축별 스키마 검증**

```bash
python tools/validate_problems.py docs/research/01-divergent/p4-channel.md --min 10
python tools/validate_problems.py docs/research/01-divergent/p5-regulator.md --min 15
python tools/validate_problems.py docs/research/01-divergent/p6-loss-stats.md --min 10
```

기대: 3개 모두 `결과: PASS`

- [ ] **Step 5: P6 정량 수치 확인**

```bash
grep -c "수치없음" docs/research/01-divergent/p6-loss-stats.md
```

기대: `0`
P6는 통계 축이므로 `수치없음` 항목이 있으면 안 된다. 1건 이상이면 해당 항목에 수치를 보강하거나 삭제한다.

- [ ] **Step 6: 전체 발산 산출량 확인**

```bash
python tools/validate_problems.py docs/research/01-divergent/ --min 80
```

기대: `검사 대상: 80개 이상`, `결과: PASS`
80개 미만이면 산출량이 가장 적은 축에 추가 발산을 지시한다. 단, 총 100개를 넘으면 추가 발산을 중단한다(검증 비용이 개수에 비례).

- [ ] **Step 6-1: 요약 블록 확인 및 위치 검사**

```bash
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p4-channel.md | head -5
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p5-regulator.md | head -5
grep -n "한눈에 보기\|^### P" docs/research/01-divergent/p6-loss-stats.md | head -5
```

기대: 각 파일에서 `한눈에 보기` 줄 번호 < 첫 `### P` 줄 번호. 누락 시 직접 작성한다.

- [ ] **Step 6-2: 진행 기록 추가**

`docs/research/PROGRESS.md` 맨 아래에 덧붙인다.

```markdown
## Task 4 — 발산 축 P4~P6

- **상태:** 완료
- **산출:** `docs/research/01-divergent/p4-channel.md`, `p5-regulator.md`, `p6-loss-stats.md`
- **수치:** P4 N개 / P5 N개 / P6 N개, 6축 합계 N개, P6 수치없음 0건
- **판단:** [Task 3 피드백을 반영했다면 무엇을 어떻게 고쳤는지]
- **다음 Task에 넘기는 것:** [축 간 눈에 띄는 중복 주제, 통합 시 주의할 점]
```

- [ ] **Step 7: 커밋**

```bash
git add docs/research/
git commit -m "docs: 발산 축 P4~P6 문제 발굴 결과

- P4 채널 마찰 / P5 감독당국 지목 / P6 피해 통계
- 6축 발산 완료, 전체 스키마 검증 통과"
git push
```

---

## Task 5: 문제 풀 통합 및 중복 제거 (Phase 2 게이트)

**목적:** 6개 파일에 흩어진 문제를 하나의 풀로 합치고 중복을 제거한다. **중복 횟수를 기록**하는 것이 핵심이다. 여러 축에서 독립 도출된 문제는 Phase 5에서 가점 근거가 된다.

**Files:**
- Create: `docs/research/02-problem-pool.md`

**Interfaces:**
- Consumes: `docs/research/01-divergent/*.md` 전체
- Produces: 통합 문제 풀. 기존 7개 필드에 아래 2개 필드가 추가된 확장 블록

  ```
  - 중복 출처: P1-03, P5-11
  - 중복 횟수: 3
  ```
  `중복 횟수`는 병합 전 원본 항목 수(자기 자신 포함). 중복이 없으면 `중복 출처: 없음` / `중복 횟수: 1`

- [ ] **Step 1: 병합 규칙 확정**

두 항목은 아래를 **모두** 만족할 때만 동일 문제로 본다.
- `당사자`가 같거나 한쪽이 다른 쪽에 포함된다
- `문제 한줄`의 손해·불편이 같은 종류다

당사자가 같아도 불편의 종류가 다르면 별개 문제다. (예: "고령층이 앱 이체를 못 한다"와 "고령층이 보이스피싱에 취약하다"는 별개)

- [ ] **Step 2: 통합 파일 생성**

`docs/research/02-problem-pool.md`를 만들고 첫 줄에 `# 통합 문제 풀`을 쓴다. 6축 항목을 전부 옮기되, 병합된 항목은 대표 항목 1개만 남기고 `중복 출처`·`중복 횟수` 필드를 추가한다.

ID는 **원본 ID를 유지**한다. 새로 부여하지 않는다 — 원본 추적이 끊기면 Phase 3에서 근거를 되짚을 수 없다.

병합 시 필드 선택 규칙:
- `피해 규모` — 수치가 있는 쪽을 채택. 둘 다 있으면 출처 등급이 높은 쪽(정부·감독기관 > 협회 > 언론)
- `근거 URL` — 병합된 모든 항목의 URL을 쉼표로 이어 붙인다
- 나머지 필드 — 더 구체적인 쪽을 채택

- [ ] **Step 3: 통합 결과 검증**

```bash
python tools/validate_problems.py docs/research/02-problem-pool.md --min 40
```

기대: `결과: PASS`, 검사 대상 40~60개

40개 미만이면 병합이 과했다는 뜻이다. Step 1 규칙을 다시 적용해 잘못 합친 항목을 분리한다.
60개 초과여도 진행한다 — Phase 3에서 걸러진다.

- [ ] **Step 4: 중복 신호 요약**

```bash
grep "중복 횟수" docs/research/02-problem-pool.md | sort | uniq -c | sort -rn
```

기대: 중복 횟수 분포가 출력된다. `중복 횟수: 2` 이상인 항목이 최소 3건은 나와야 정상이다. 0건이면 축들이 완전히 분리되어 동작한 것이므로, 병합 규칙(Step 1)을 너무 좁게 적용했는지 재확인한다.

- [ ] **Step 5: 완료 게이트 확인**

- [ ] 6개 축 파일이 모두 통합 반영되었다
- [ ] 통합 후 40개 이상 남았다
- [ ] 스키마 검증 `PASS` (위반 0건)
- [ ] `중복 횟수: 2` 이상 항목이 존재한다

- [ ] **Step 5-1: 요약 블록 작성**

`02-problem-pool.md` 최상단(첫 `### P` 헤딩 앞)에 넣는다.

```markdown
## 한눈에 보기

- **항목 수:** N개 (원본 N개 → 병합 N건 → 최종 N개)
- **주요 패턴:** [당사자·업권·문제 유형별 분포에서 눈에 띄는 경향 2~3개]
- **특이 사항:** [중복 횟수 3 이상 항목, 근거가 유독 강한 문제군]
- **다음 단계 유의점:** [검증 단계에서 특히 반증을 의심해야 할 항목]
```

- [ ] **Step 5-2: 진행 기록 추가**

```markdown
## Task 5 — 문제 풀 통합 및 중복 제거

- **상태:** 완료
- **산출:** `docs/research/02-problem-pool.md`
- **수치:** 원본 N개 → 병합 N건 → 최종 N개, 중복 횟수 2 이상 N건
- **판단:** [병합 판정이 애매했던 사례와 어떻게 결정했는지]
- **다음 Task에 넘기는 것:** [근거가 약해 보여 우선 검증이 필요한 항목 ID]
```

- [ ] **Step 6: 커밋**

```bash
git add docs/research/
git commit -m "docs: 6축 문제 풀 통합 및 중복 제거

- 중복 출처/중복 횟수 필드 추가로 다축 도출 신호 보존
- 스키마 검증 통과"
git push
```

---

## Task 6: 문제 실재성 검증 (Phase 3)

**목적:** 발산 산출물은 아직 "주장"이다. 근거 등급을 매기고, **반증을 적극적으로 탐색**하고, URL을 실제로 열어 확인한다. **이 Task는 생략 불가다.**

**Files:**
- Create: `docs/research/03-problem-validation.md`
- Modify: `docs/research/02-problem-pool.md` (탈락 항목에 탈락 표시)

**Interfaces:**
- Consumes: `docs/research/02-problem-pool.md`
- Produces: 생존 문제 목록. 각 항목에 아래 3개 필드가 추가됨

  ```
  - 근거 등급: A
  - 반증 결과: 유사 서비스 없음. 2025년 제도 개선 계획 있으나 시행 전
  - URL 실증: 확인 (본문에 해당 통계 존재)
  ```

- [ ] **Step 1: URL 도달성 일괄 검사**

```bash
python tools/validate_problems.py docs/research/02-problem-pool.md --check-urls
```

기대: 도달 실패 URL이 `HARD` 목록에 출력된다.
도달 실패 항목은 대체 출처를 찾아 교체하고, 못 찾으면 해당 항목을 탈락시킨다.

이 단계는 **환각 URL을 기계적으로 걸러내는 1차 필터**다. 다만 "페이지가 존재한다"와 "내용이 주장을 뒷받침한다"는 다른 문제이므로 Step 3의 내용 대조가 별도로 필요하다.

- [ ] **Step 2: 반증 탐색 서브에이전트 실행**

문제 풀을 10개 내외 묶음으로 나눠 병렬 디스패치한다. 각 에이전트에 아래 프롬프트를 전달한다.

```
당신은 2026 금융 AI Challenge 참가팀의 검증 담당이다.
당신의 임무는 아래 문제 항목들이 **가짜임을 입증하는 것**이다.
지지하는 근거를 찾지 말고, 반박하는 근거를 찾아라.

각 항목에 대해 다음 3가지를 조사하고 결과를 기록하라.

1. **기존 해결책 탐색** — 이 문제를 이미 해결하는 상용 서비스·공공 서비스가
   존재하는가? 국내 금융사 앱, 핀테크 서비스, 정부·공공기관 서비스를 검색하라.
   존재한다면 서비스명과 URL, 그리고 그 서비스가 이 문제를 얼마나 덮고 있는지
   (완전 해결 / 부분 해결 / 무관)를 적어라.

2. **제도 변화 탐색** — 이 문제를 제거하거나 축소하는 법령·규제·정책 변화가
   이미 시행되었거나 시행 예정인가? 시행일과 출처를 적어라.

3. **근거 신선도 확인** — 인용된 통계의 기준 연도를 확인하라.
   2023년 이전 데이터라면 최신 수치를 찾아 갱신하거나 `구버전 통계`로 표시하라.

그리고 각 항목의 근거 URL에 실제로 접속하여, 페이지 내용이 `문제 한줄`의
주장을 뒷받침하는지 확인하라. 뒷받침하지 않으면 `URL 실증: 불일치`로 기록하라.

각 항목에 대해 아래 3개 필드를 산출하라.

- 근거 등급: A(정부·감독기관 공식 통계·보도자료) / B(협회·연구기관 보고서) /
  C(언론 보도) / D(일화·블로그·근거 없는 추정) 중 하나
- 반증 결과: 위 1~3의 조사 결과를 한 줄로 요약
- URL 실증: `확인` 또는 `불일치` 또는 `도달 실패`

**주의:** 문제를 옹호하지 마라. 애매하면 부정적으로 판정하라.
살아남는 문제만 진짜다.
```

- [ ] **Step 3: 탈락 판정 적용**

아래 조건 중 하나라도 해당하면 탈락시킨다.

| 조건 | 처리 |
|---|---|
| 근거 등급 `D`이고 상향 근거 확보 실패 | 탈락 |
| 반증 결과에 기존 서비스가 **완전 해결**로 확인됨 | 탈락 |
| 제도 변화로 문제가 이미 제거됨 | 탈락 |
| `URL 실증: 불일치` 또는 `도달 실패`이고 대체 출처 확보 실패 | 탈락 |
| 금융 주제 범위 밖 | 탈락 |

탈락 항목은 `02-problem-pool.md`에서 지우지 말고 `- 상태: 탈락(사유)` 필드를 추가한다. 나중에 "왜 이 문제를 뺐지?"라는 질문이 반드시 나온다.

- [ ] **Step 4: 생존 목록 작성**

`docs/research/03-problem-validation.md`에 생존 항목만 옮긴다. 파일 첫머리에 아래 요약을 넣는다.

```markdown
# 문제 실재성 검증 결과

## 한눈에 보기

- **항목 수:** 검증 대상 N개 → 생존 N개 (A등급 N / B등급 N / C등급 N)
- **탈락 내역:** 근거부족 N / 기존해결 N / 제도변화 N / URL불일치 N
- **주요 패턴:** [어떤 축에서 온 문제가 많이 죽었는지, 죽은 이유의 공통점]
- **특이 사항:** [반증에서 뜻밖에 강하게 살아남은 문제, 반대로 예상 밖으로 죽은 문제]
- **다음 단계 유의점:** [채점 시 점수가 갈릴 것으로 보이는 지점]
```

`한눈에 보기`는 첫 `### P` 헤딩보다 앞에 위치시킨다.

- [ ] **Step 5: 생존 항목 재검증**

```bash
python tools/validate_problems.py docs/research/03-problem-validation.md --min 15 --check-urls
```

기대: `결과: PASS`, 검사 대상 15~30개, URL 도달 실패 0건

- [ ] **Step 6: 완료 게이트 및 중단 조건 확인**

**완료 게이트**
- [ ] 전 항목에 `근거 등급` 부여 완료
- [ ] 전 항목에 `반증 결과` 1줄 이상 기록
- [ ] 생존 항목 URL 100% 도달 확인 (`--check-urls` PASS)
- [ ] 생존 항목 15개 이상

**중단 조건**
- 생존 15개 미만 → Task 3/4로 되돌아가 축을 추가한다 (예: 해외 금융 현안의 국내 적용 가능성 축)
- 생존 40개 초과 → 근거 등급 `A`/`B` 항목만 남기고 `C` 등급은 잘라낸다

- [ ] **Step 6-1: 진행 기록 추가**

```markdown
## Task 6 — 문제 실재성 검증

- **상태:** 완료
- **산출:** `docs/research/03-problem-validation.md`, `02-problem-pool.md`(탈락 표시)
- **수치:** 검증 N개 → 생존 N개 (A N / B N / C N), 탈락 N개, URL 도달 실패 0건
- **판단:** [탈락 판정이 애매했던 사례와 결정 근거. 특히 "부분 해결"을 어디까지 생존으로 봤는지]
- **다음 Task에 넘기는 것:** [채점 시 ④미해결도가 논쟁이 될 항목 ID]
```

**이 기록은 특히 중요하다.** 발표 심사 질의응답에서 "왜 이 문제를 골랐나"만큼이나 "왜 저 문제는 안 골랐나"가 자주 나온다. 탈락 근거가 남아 있어야 답할 수 있다.

- [ ] **Step 7: 커밋**

```bash
git add docs/research/
git commit -m "docs: 문제 실재성 검증 완료

- 근거 등급 판정 + 반증 탐색 + URL 실증
- 탈락 항목은 사유와 함께 풀에 보존"
git push
```

---

## Task 7: 우선순위 스코어링 (Phase 4)

**목적:** 생존 문제를 6축으로 채점해 상위 8~12개를 뽑는다. **해결 가능성은 평가하지 않는다.** 문제 자체의 매력도만 본다.

**Files:**
- Create: `docs/research/04-priority-matrix.md`

**Interfaces:**
- Consumes: `docs/research/03-problem-validation.md`
- Produces: 가중 합계 기준 정렬된 순위표. 각 행은 `ID | 문제 요약 | ①~⑥ 점수 | 가중합계 | 채점 근거`

- [ ] **Step 1: 채점 기준 파일 헤더 작성**

`docs/research/04-priority-matrix.md` 첫머리에 채점 기준을 복사해 넣는다. 채점 도중 기준을 찾아 다른 파일을 열게 되면 기준이 표류한다.

```markdown
# 문제 우선순위 스코어링

## 채점 축과 가중치

| 축 | 질문 | 가중치 |
|---|---|---|
| ① 실재성 | 근거가 얼마나 단단한가 | ×1.0 |
| ② 심각도 | 당사자 1인이 겪는 고통·손실이 얼마나 큰가 | ×1.0 |
| ③ 규모 | 몇 명이 / 얼마의 금액이 영향받는가 | ×1.0 |
| ④ 미해결도 | 지금 방치되어 있거나 수작업으로 처리되는가 | ×1.5 |
| ⑤ 심사 적합성 | 공고 주제 범위·주최기관 관심사와 얼마나 맞는가 | ×1.5 |
| ⑥ 시의성 | "왜 지금인가"에 답할 수 있는가 | ×1.0 |

가중합계 = ①+②+③+⑥ + (④×1.5) + (⑤×1.5), 최대 40점

## 점수 앵커

**① 실재성** — 5: A등급 근거 + 최근 2년 내 정량 수치 / 3: B~C등급 근거 + 수치 있음 / 1: 수치 없음, 정성 서술만

**④ 미해결도** — 5: 현재 아무 대응이 없거나 전적으로 수작업 / 3: 부분적 해결책은 있으나 사각지대가 넓음 / 1: 이미 성숙한 상용 서비스가 존재

**⑤ 심사 적합성** — 5: 공고 주제 범위 내 + 금융보안원 또는 공동개최사(하나·신한·카카오뱅크·KB증권·생보협) 업권에 명확히 귀속 / 3: 공고 주제 범위 내이나 특정 기관 귀속이 불분명 / 1: 금융 주제이나 공고 취지와 거리가 있음

**②③⑥** — 5: 명확·큼·강함 / 3: 보통 / 1: 약함

2점과 4점은 인접 앵커 사이 값으로 사용한다.
```

- [ ] **Step 2: 전 항목 채점**

각 생존 항목에 6축 점수를 매기고, **각 점수마다 근거를 한 줄씩** 남긴다. 근거 없는 점수는 나중에 재현할 수 없다.

`04-priority-matrix.md`에 아래 형식으로 기록한다.

```markdown
## P5-03 (가중합계 34.0)

> 문제 요약: 65세 이상 이용자가 모바일뱅킹 이체 화면에서 ...

| 축 | 점수 | 근거 |
|---|---|---|
| ① 실재성 | 5 | 금융감독원 2025년 실태조사 정량 수치 |
| ② 심각도 | 4 | 이체 실패 시 대체 수단이 영업점 방문뿐 |
| ③ 규모 | 5 | 해당 연령대 이용자 N만 명 |
| ④ 미해결도 | 4 | 일부 은행 간편모드 존재하나 커버리지 제한 |
| ⑤ 심사 적합성 | 5 | 공고 예시 5번 직접 대응, 은행 3사 슬롯 |
| ⑥ 시의성 | 3 | 고령화 추세 지속, 특정 시점 계기는 약함 |
```

- [ ] **Step 3: 가중합계 검산**

무작위로 3개 항목을 골라 손으로 계산해 표기값과 일치하는지 확인한다.
예: ①5 ②4 ③5 ④4 ⑤5 ⑥3 → (5+4+5+3) + (4×1.5) + (5×1.5) = 17 + 6 + 7.5 = **30.5**

- [ ] **Step 4: 정렬 및 상위 선별**

가중합계 내림차순으로 정렬하고, 파일 최상단에 순위 요약표를 추가한다.

```markdown
## 순위 요약

| 순위 | ID | 가중합계 | 문제 한줄 요약 | 관련 업권 |
|---|---|---|---|---|
| 1 | P5-03 | 34.0 | ... | 은행 |
```

상위 8~12개를 `**상위권**` 표시한다.

- [ ] **Step 5: 완료 게이트 및 중단 조건 확인**

**완료 게이트**
- [ ] 전 생존 항목에 6축 점수 + 축별 근거 1줄 기록
- [ ] 가중합계 검산 3건 일치
- [ ] 순위 요약표 작성, 상위 8~12개 식별

**중단 조건** — 점수 재조정을 2회 넘게 반복하지 않는다. 3회째 조정은 원하는 항목을 올리기 위한 사후 합리화일 가능성이 높다.

- [ ] **Step 5-1: 진행 기록 추가**

```markdown
## Task 7 — 우선순위 스코어링

- **상태:** 완료
- **산출:** `docs/research/04-priority-matrix.md`
- **수치:** 채점 N개, 최고 가중합계 N점 / 상위권 컷 N점, 검산 3건 일치
- **판단:** [점수 재조정을 했다면 몇 회, 무엇을 왜 바꿨는지. 앵커 해석이 갈린 축]
- **다음 Task에 넘기는 것:** [순위는 낮지만 클러스터 구성상 버리기 아까운 항목 ID]
```

- [ ] **Step 6: 커밋**

```bash
git add docs/research/
git commit -m "docs: 문제 우선순위 스코어링 완료

- 6축 가중 채점(미해결도·심사적합성 ×1.5), 축별 근거 기록
- 상위 8~12개 식별"
git push
```

---

## Task 8: 유망 문제 영역 선정 (Phase 5)

**목적:** 상위 항목을 영역으로 묶고, 다음 사이클(해결책 설계)이 바로 착수할 수 있는 문제 정의서를 만든다. **해결책은 여전히 쓰지 않는다.**

**Files:**
- Create: `docs/research/05-shortlist.md`

**Interfaces:**
- Consumes: `docs/research/04-priority-matrix.md`, `docs/research/02-problem-pool.md`(중복 횟수 필드)
- Produces: 최종 산출물. 유망 문제 영역 3~5개, 각각 1페이지 문제 정의서 + 데이터 지형 메모

- [ ] **Step 1: 클러스터링**

상위 8~12개를 문제 성격별로 묶는다. 초기 클러스터 후보:
- 사기·보안 (보이스피싱, 이상거래, 보험사기)
- 포용금융 (고령층, 장애인, 외국인, 청년)
- 기업금융 (창업기업, 소상공인, 벤처 성장성 평가)
- 프로세스·채널 효율 (창구, 앱, 콜센터 마찰)

어느 클러스터에도 안 들어가는 항목은 억지로 넣지 말고 단독 영역으로 둔다.

- [ ] **Step 2: 중복 도출 가점 적용**

`02-problem-pool.md`의 `중복 횟수` 필드를 확인한다. 중복 횟수 2 이상인 문제를 포함한 클러스터를 우선한다. 독립적인 여러 축에서 반복 발견되었다는 것은 문제 실재성의 독립 신호다.

- [ ] **Step 3: 영역 3~5개 선정**

클러스터를 아래 기준으로 정렬해 상위 3~5개를 고른다.
1. 클러스터 내 최고 가중합계
2. 클러스터 내 항목 수 (많을수록 문제 영역이 두껍다)
3. 중복 횟수 2 이상 항목 포함 여부

**5개를 초과해 선정하지 않는다.** 다음 사이클의 부하가 영역 수에 비례한다.

- [ ] **Step 4: 영역별 문제 정의서 작성**

각 영역에 대해 아래 형식으로 작성한다.

```markdown
## 영역 N: [영역명]

**포함 문제 ID:** P5-03, P3-08, P6-02

### 문제 서술
[이 영역이 다루는 문제를 3~5문장으로. 해결책 언급 금지]

### 당사자
[구체적 집단과 추정 규모]

### 피해 규모
| 지표 | 수치 | 기준연도 | 출처 |
|---|---|---|---|
| ... | ... | ... | [URL] |

### 현재 대응
[지금 어떻게 처리되고 있는가. 기존 서비스가 있다면 무엇이고 어디까지 덮는가]

### 왜 지금인가
[제도 변화·환경 변화·통계 추세 중 이 시점을 정당화하는 근거. 없으면 "특정 계기 없음"이라고 명시]

### 근거 출처
- [URL] — 무엇을 뒷받침하는지
```

- [ ] **Step 5: 데이터 지형 메모 작성**

각 영역에 아래를 덧붙인다. **영역당 30분을 넘기지 않는다.** 초과하면 `미확인`으로 남긴다.

```markdown
### 데이터 지형 메모 (참고용, 우선순위 미반영)
- 접근 가능한 공개 데이터/API: [명칭과 제공기관, 또는 `미확인`]
- 비고: 존재 여부와 명칭까지만 기록. **활용 방안은 쓰지 않는다.**
```

이 메모는 다음 사이클의 출발점 역할만 한다. 여기에 활용 아이디어를 쓰기 시작하면 해결책 설계가 검증 없이 시작된다.

- [ ] **Step 6: 해결책 누출 최종 점검**

```bash
grep -nE "AI로|LLM|RAG|챗봇|에이전트|추천 시스템|자동화하여|플랫폼을|솔루션|서비스를 구축|앱을 개발" docs/research/05-shortlist.md
```

기대: 출력 없음.
출력이 있으면 각 줄을 열어 해결책 서술인지 확인하고 삭제한다. (예: 대회 공고 예시를 인용한 부분이라면 인용 표시가 명확한지 확인)

- [ ] **Step 7: 사이클 완료 조건 확인**

- [ ] `00-research-brief.md` 작성 완료
- [ ] `01-divergent/` 6개 파일 생성, 총 80개 이상
- [ ] `02-problem-pool.md` 중복 제거 완료, 스키마 위반 0건
- [ ] `03-problem-validation.md` 생존 전건에 근거 등급 + 반증 결과 기록
- [ ] 생존 문제 근거 URL 100% 도달 검증 완료
- [ ] `04-priority-matrix.md` 6축 점수 + 채점 근거 기록
- [ ] `05-shortlist.md` 유망 문제 영역 3~5개, 각 1페이지 문제 정의서 포함
- [ ] 각 문제 정의서에 데이터 지형 메모 첨부 (`미확인` 허용)
- [ ] Step 6 grep 결과 없음 (해결책 서술 0건)
- [ ] `PROGRESS.md`에 Task 1~8 전 섹션이 기록되어 있다

- [ ] **Step 7-1: 최종 진행 기록 추가**

```markdown
## Task 8 — 유망 문제 영역 선정

- **상태:** 완료 — 리서치 사이클 종료
- **산출:** `docs/research/05-shortlist.md`
- **수치:** 클러스터 N개 → 선정 N개 영역, 포함 문제 N개, 데이터 지형 `미확인` N건
- **판단:** [클러스터 경계를 어떻게 그었는지, 탈락시킨 클러스터와 그 이유]
- **다음 사이클에 넘기는 것:** 해결책 설계 시 반영할 제약 4가지 (팀 역량 공백 / 배포 가동 요구 / 데이터 미제공 / 1차 심사 주제 적합성)

---

## 리서치 사이클 종료

- 최종 산출물: `docs/research/05-shortlist.md`
- 다음 단계: 해결책 설계 사이클 (별도 brainstorming → spec → plan)
```

- [ ] **Step 8: 커밋**

```bash
git add docs/research/
git commit -m "docs: 유망 금융 현안 영역 3~5개 선정

- 클러스터링 + 다축 중복 도출 가점 적용
- 영역별 문제 정의서 및 데이터 지형 메모 작성
- 리서치 사이클 종료"
git push
```

---

## 리서치 종료 후

이 계획이 끝나면 **해결책 설계 사이클**을 새로 시작한다. 그 사이클에서 반드시 반영해야 할 이월 사항:

1. **팀 역량 공백** — ML/LLM/도메인은 강점, **웹 풀스택·배포가 공백**이다. 복잡한 UI가 필수인 해결책은 감점 요인으로 다뤄야 한다.
2. **배포 가동 요구** — 웹서비스 URL이 2026-09-07 11:00 ~ 09-11 23:59 동안 접속 가능해야 한다. 미가동은 결격이다. 배포 방식 결정을 뒤로 미루지 않는다.
3. **데이터 미제공** — 데이터 확보 경로가 없는 해결책은 더미 데이터 데모로 끝난다. Task 8의 데이터 지형 메모가 출발점이다.
4. **1차 심사는 주제 적합성** — 해결책이 공고 주제 범위 안에 있음이 기획서 첫 페이지에서 드러나야 한다.
