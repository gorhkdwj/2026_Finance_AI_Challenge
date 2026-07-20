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
