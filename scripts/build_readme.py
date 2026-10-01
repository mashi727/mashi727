"""README.md の自動生成区間を、公開リポジトリの最終 push 日時順で組み直す。

- NOW      : 直近に push した上位 N 件
- SHOWCASE : projects.json の showcase を最近更新した順に
- INDEX    : 分野ごとの一覧。分野も行も最近更新した順

分類と説明文は projects.json で管理する。未登録の公開リポジトリは Others に入り、
GitHub の description を使う。標準ライブラリのみ。
    python3 scripts/build_readme.py           # README.md を更新
    GITHUB_TOKEN=... python3 scripts/build_readme.py
"""
import html
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
README = ROOT / "README.md"
NBH = "\u2011"  # 改行されないハイフン(表の列幅が狭いときに名前・日付が割れないように)


def fetch_repos(user: str) -> list[dict]:
    url = f"https://api.github.com/users/{user}/repos?per_page=100&type=owner&sort=pushed"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        repos = json.load(r)
    excluded = set(CONFIG["exclude"])
    repos = [
        r for r in repos
        if not (r["private"] or r["fork"] or r["archived"] or r["name"] in excluded)
    ]
    return sorted(repos, key=lambda r: r["pushed_at"], reverse=True)


def desc_of(repo: dict) -> str:
    meta = CONFIG["projects"].get(repo["name"], {})
    return meta.get("desc") or repo.get("description") or ""


def inline(md: str) -> str:
    """HTML の中に置く説明文: エスケープしつつ `code` だけ <code> にする。"""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(md))


def build_now(repos: list[dict]) -> str:
    n = CONFIG["now_count"]
    cells = []
    for r in repos[:n]:
        lang = f"<code>{html.escape(r['language'])}</code> · " if r.get("language") else ""
        cells.append(
            f'<td valign="top" width="{100 // n}%">\n'
            f'<a href="{r["html_url"]}"><b>{html.escape(r["name"])}</b></a><br>\n'
            f"<sub>{inline(desc_of(r))}</sub><br><br>\n"
            f"<sub>{lang}🕒 {r['pushed_at'][:10]}</sub>\n</td>"
        )
    return "<table>\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"


def build_showcase(repos: list[dict]) -> str:
    pushed = {r["name"]: r["pushed_at"] for r in repos}
    items = [s for s in CONFIG["showcase"] if s["repo"] in pushed]
    items.sort(key=lambda s: pushed[s["repo"]], reverse=True)
    cells = []
    for s in items:
        url = f"https://github.com/{CONFIG['user']}/{s['repo']}"
        cells.append(
            f'<td valign="top" width="{100 // max(len(items), 1)}%">\n'
            f'<a href="{url}"><img src="{s["image"]}" alt="{html.escape(s["repo"])}" width="100%"></a><br>\n'
            f'<a href="{url}"><b>{html.escape(s["repo"])}</b></a> — {html.escape(s["tagline"])}\n</td>'
        )
    return "<table>\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"


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
    new = replace(new, "SHOWCASE", build_showcase(repos))
    new = replace(new, "INDEX", build_index(repos))
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md unchanged")


if __name__ == "__main__":
    main()
