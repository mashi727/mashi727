"""README.md の自動生成区間と、Now の活動カード SVG を組み直す。

- NOW   : 直近 window_days 日のコミット数が多い上位 N 件(ワークロード順)。
          各項目は <details> の開閉式タブで、中に活動カード(assets/now/<repo>.svg)と、
          リポジトリの README から拾った画面画像を置く。1 位だけ最初から開く。
- INDEX : 分野ごとの一覧。分野も行も最近更新した順

分類・説明文・画像の上書きは projects.json で管理する。未登録の公開リポジトリは
Others に入り、GitHub の description を使う。標準ライブラリのみ。
    GITHUB_TOKEN=... python3 scripts/build_readme.py
"""
import base64
import html
import json
import os
import posixpath
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
README = ROOT / "README.md"
CARD_DIR = ROOT / "assets" / "now"
NBH = "‑"  # 改行されないハイフン(表の列幅が狭いときに名前・日付が割れないように)
JST = timezone(timedelta(hours=9))
RANK = ["🥇", "🥈", "🥉", "4.", "5.", "6."]
# README の画像のうち、画面写真ではないもの(バッジ類)
BADGE = re.compile(r"shields\.io|badge|/actions/|codecov|badgen|fury\.io|\.svg(\?|$)", re.I)


# --- GitHub API ------------------------------------------------------------
def api_get(url: str) -> tuple[list | dict, str | None]:
    """GitHub REST API を叩き、(JSON, 次ページの URL) を返す。"""
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        m = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link") or "")
        return json.load(r), (m.group(1) if m else None)


def fetch_repos(user: str) -> list[dict]:
    repos, _ = api_get(f"https://api.github.com/users/{user}/repos?per_page=100&type=owner&sort=pushed")
    excluded = set(CONFIG["exclude"])
    repos = [
        r for r in repos
        if not (r["private"] or r["fork"] or r["archived"] or r["name"] in excluded)
    ]
    return sorted(repos, key=lambda r: r["pushed_at"], reverse=True)


def commit_dates(repo: dict, since: str) -> list[datetime]:
    """default ブランチに since 以降に入ったコミットの日時(author date)。"""
    url: str | None = f"https://api.github.com/repos/{repo['full_name']}/commits?since={since}&per_page=100"
    dates = []
    while url:
        try:
            page, url = api_get(url)
        except urllib.error.HTTPError as e:
            if e.code == 409:  # 空のリポジトリ
                return []
            raise
        for c in page:
            dates.append(datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00")))
    return dates


def workload(repos: list[dict]) -> list[tuple[dict, list[datetime]]]:
    """直近 window_days 日のコミット数が多い順。同数なら最終 push が新しい順。0 件は除く。"""
    since_dt = datetime.now(timezone.utc) - timedelta(days=CONFIG["window_days"])
    since = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    # push がそれより古いリポジトリには期間内のコミットが無いので問い合わせない
    counted = [(r, commit_dates(r, since)) for r in repos if r["pushed_at"] >= since]
    counted = [(r, d) for r, d in counted if d]
    return sorted(counted, key=lambda t: (len(t[1]), t[0]["pushed_at"]), reverse=True)


def screenshot_of(repo: dict) -> str | None:
    """README に載っている最初の画面画像の URL。projects.json の image で上書き(false で無し)。"""
    meta = CONFIG["projects"].get(repo["name"], {})
    if "image" in meta:
        return meta["image"] or None
    try:
        data, _ = api_get(f"https://api.github.com/repos/{repo['full_name']}/readme")
    except urllib.error.HTTPError:
        return None
    assert isinstance(data, dict)
    text = base64.b64decode(data["content"]).decode("utf-8", "replace")
    srcs = re.findall(r'!\[[^\]]*\]\(\s*([^)\s]+)|<img\s[^>]*?src="([^"]+)"', text)
    for md, tag in srcs:
        src = md or tag
        if BADGE.search(src):
            continue
        if src.startswith(("http://", "https://")):
            return src
        base = posixpath.dirname(data["path"])
        path = posixpath.normpath(posixpath.join(base, src))
        return f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{path}"
    return None


# --- 活動カード SVG --------------------------------------------------------
def text_width(s: str, size: float) -> float:
    return sum(size * (1.0 if ord(ch) > 0x2E7F else 0.56) for ch in s)


def wrap(s: str, size: float, width: float, max_lines: int) -> list[str]:
    lines, cur = [], ""
    for ch in s:
        if text_width(cur + ch, size) > width:
            lines.append(cur)
            cur = ch.lstrip()
            if len(lines) == max_lines:
                lines[-1] = lines[-1][:-1] + "…"
                return lines
        else:
            cur += ch
    return lines + [cur] if cur else lines


def make_card(rank: int, repo: dict, dates: list[datetime]) -> str:
    W, H = 1280, 340
    days = CONFIG["window_days"]
    today = datetime.now(JST).date()
    bins = [0] * days
    for d in dates:
        k = (today - d.astimezone(JST).date()).days
        if 0 <= k < days:
            bins[days - 1 - k] += 1
    peak = max(bins) or 1
    x0, x1, base, hmax = 64, W - 64, 300, 64
    slot = (x1 - x0) / days
    bars = []
    for i, n in enumerate(bins):
        x = x0 + i * slot + 3
        if n:
            h = max(6, hmax * n / peak)
            bars.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{slot - 6:.1f}" height="{h:.1f}" rx="3" fill="url(#bar)"/>')
        else:
            bars.append(f'<rect x="{x:.1f}" y="{base - 3}" width="{slot - 6:.1f}" height="3" rx="1.5" fill="#3a4170"/>')
    meta = CONFIG["projects"].get(repo["name"], {})
    headline = meta.get("tagline") or ""
    desc = re.sub(r"`([^`]+)`", r"\1", meta.get("desc") or repo.get("description") or "")
    desc_lines = wrap(desc, 19, 720, 2)
    esc = html.escape
    lang = esc(repo.get("language") or "")
    start = (today - timedelta(days=days - 1)).strftime("%m/%d")
    jp = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Noto Sans CJK JP','Noto Sans JP',sans-serif"
    serif = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
    y_tag = 146  # タグライン(あれば)。説明文はその下、無ければこの位置から
    y_desc = y_tag + 36 if headline else y_tag
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="{esc(repo["name"])}: {len(dates)} commits in the last {days} days">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0f22"/>'
        '<stop offset="1" stop-color="#1b1640"/></linearGradient>'
        '<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#38d6ff"/>'
        '<stop offset="1" stop-color="#ff7ad9"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>',
        f'<text x="64" y="52" font-family="-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif" font-size="14" '
        f'letter-spacing="3" fill="#7f88b8">#{rank} · LAST {days} DAYS</text>',
        f'<text x="64" y="104" font-family="{serif}" font-size="50" fill="#f4f1ff">{esc(repo["name"])}</text>',
    ]
    if headline:
        parts.append(f'<text x="66" y="{y_tag}" font-family="{jp}" font-size="21" font-weight="600" fill="#e3dcff">{esc(headline)}</text>')
    for i, line in enumerate(desc_lines):
        parts.append(f'<text x="66" y="{y_desc + i * 28}" font-family="{jp}" font-size="19" fill="#b9c0e8">{esc(line)}</text>')
    parts += [
        f'<text x="{W - 64}" y="112" text-anchor="end" font-family="{serif}" font-size="84" fill="#ffffff">{len(dates)}</text>',
        f'<text x="{W - 64}" y="142" text-anchor="end" font-family="-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif" '
        f'font-size="16" letter-spacing="2" fill="#9aa3d4">COMMITS · {lang.upper()}</text>',
        *bars,
        f'<text x="{x0}" y="{base + 24}" font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="13" fill="#6c74a6">{start}</text>',
        f'<text x="{x1}" y="{base + 24}" text-anchor="end" font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="13" fill="#6c74a6">today</text>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


# --- README の各区間 -------------------------------------------------------
def desc_of(repo: dict) -> str:
    meta = CONFIG["projects"].get(repo["name"], {})
    return meta.get("desc") or repo.get("description") or ""


def build_now(repos: list[dict]) -> str:
    top = workload(repos)[: CONFIG["now_count"]]
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    keep = set()
    blocks = []
    for i, (r, dates) in enumerate(top):
        card = CARD_DIR / f"{r['name']}.svg"
        svg = make_card(i + 1, r, dates)
        if not card.exists() or card.read_text(encoding="utf-8") != svg:
            card.write_text(svg, encoding="utf-8")
        keep.add(card.name)
        shot = screenshot_of(r)
        body = [f'<a href="{r["html_url"]}"><img src="assets/now/{card.name}" alt="{html.escape(r["name"])} の直近の活動" width="100%"></a>']
        if shot:
            body.append(f'<a href="{r["html_url"]}"><img src="{html.escape(shot)}" alt="{html.escape(r["name"])} の画面" width="100%"></a>')
        blocks.append(
            f"<details{' open' if i == 0 else ''}>\n"
            f"<summary><b>{RANK[i]} {html.escape(r['name'])}</b> — 🔥 {len(dates)} commits / {CONFIG['window_days']}日"
            f" · <sub>{html.escape(r.get('language') or '')}</sub></summary>\n<br>\n\n"
            + "\n".join(body)
            + "\n\n</details>"
        )
    for old in CARD_DIR.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
    if not blocks:
        return f"<sub>直近 {CONFIG['window_days']} 日のコミットはありません。</sub>"
    return "\n".join(blocks)


def build_index(repos: list[dict]) -> str:
    cats = CONFIG["categories"]
    groups: dict[str, list[dict]] = {}
    for r in repos:  # repos は最近 push した順なので、各分野内もその順になる
        cat = CONFIG["projects"].get(r["name"], {}).get("cat", "other")
        groups.setdefault(cat if cat in cats else "other", []).append(r)
    out = []
    # 分野は「その分野で最後に push された日時」の新しい順
    for cat in sorted(groups, key=lambda c: groups[c][0]["pushed_at"], reverse=True):
        out.append(f"#### {cats[cat]}\n")
        out.append("| Project | | Updated |\n| --- | --- | --- |")
        for r in groups[cat]:
            name = r["name"].replace("-", NBH)
            out.append(f"| [**{name}**]({r['html_url']}) | {desc_of(r)} | {r['pushed_at'][:7].replace('-', NBH)} |")
        out.append("")
    return "\n".join(out).rstrip()


def replace(text: str, key: str, body: str) -> str:
    pat = re.compile(rf"(<!-- {key}:START -->\n).*?(<!-- {key}:END -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"marker {key} not found in README.md")
    return pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def main() -> None:
    repos = fetch_repos(CONFIG["user"])
    text = README.read_text(encoding="utf-8")
    new = replace(text, "NOW", build_now(repos))
    new = replace(new, "INDEX", build_index(repos))
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md unchanged")


if __name__ == "__main__":
    main()
