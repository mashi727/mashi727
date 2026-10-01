# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

GitHub プロフィールページ（`github.com/mashi727`）の README を管理する専用リポジトリ。

```
mashi727/
├── README.md                 # プロフィール本体。<!-- X:START/END --> の区間は自動生成
├── projects.json             # 各リポジトリの分野・説明文、Showcase、除外リスト
├── assets/banner.svg         # 冒頭のバナー（scripts/make_banner.py で生成）
├── scripts/
│   ├── build_readme.py       # NOW / SHOWCASE / INDEX 区間を最終 push 順で再生成（標準ライブラリのみ）
│   └── make_banner.py        # バナー SVG の生成
└── .github/workflows/
    ├── readme.yml            # 毎日 06:17 JST と projects.json 変更時に build_readme.py を実行し、差分があればコミット
    └── snake.yml             # 日次でコントリビューションの snake SVG を output ブランチへ生成
```

## README の構成

1. バナー（SVG）、一行の紹介、技術バッジ — 手書き
2. **⚡ Now** — 直近 `window_days` 日のコミット数（default ブランチ）が多い上位 `now_count` 件。同数は最終 push 順、0 件は出さない（自動）
3. **✦ Showcase** — `projects.json` の `showcase`。スクリーンショット付き（自動・更新順）
4. **🗂 All projects** — 分野ごとの表。分野も行も最終 push の新しい順（自動）
5. Contribution graph（snake、`<details>` 内）— 手書き

## 編集時の注意点

- **自動生成区間（マーカーの間）を手で編集しない。** 次の実行で上書きされる。変えたいときは `projects.json` か `build_readme.py` を直す。
- 説明文は `projects.json` の `desc` が優先。未登録の公開リポジトリは自動で `Others` に入り、GitHub の description が使われる。新規公開したら `projects.json` に分野と説明を足す。
- 説明文はリポジトリの README / description を一次資料として書く。名前から推測しない。
- 公開物なので実名・所属は書かない。表示名は `Massy` のみ。
- Showcase の画像はスクリーンショットが実際の動作を示すものに限る（起動直後の空画面は載せない）。
- バナーのアニメーションは「止まっても完成形が見える」ように作る（`<img>` 経由では SMIL の進行が環境依存のため）。
- ローカル確認: `GITHUB_TOKEN=$(gh auth token) python3 scripts/build_readme.py`（2 回目は `unchanged` になるのが正常）。

## Commit Guidelines

`Add ...` / `Update ...` / `Remove ...` の命令形で始める。
