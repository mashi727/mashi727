# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

GitHub プロフィールページ（`github.com/mashi727`）の README を管理する専用リポジトリ。コードは含まない。

```
mashi727/
├── README.md                 # プロフィールページ本体
└── .github/workflows/
    └── snake.yml             # 日次でコントリビューションの snake SVG を output ブランチへ生成
```

## README.md の構成

1. **ヘッダー**（中央寄せ）: 表示名 `Massy`、一行の紹介（日本語）と英語のサブタイトル、技術バッジ（shields.io）
2. **Highlight**: 代表作 1 件（現在は Chaptr）を 2 カラムの表で、左に説明・右にスクリーンショット
3. **分野別の一覧**: `Video & Audio` / `Documents & PDF` / `Measurement & Science` / `CLI & Utilities` の 4 表
   - 行の形式: `| [**repo-name**](https://github.com/mashi727/repo-name) | 日本語で一文の説明 |`
4. **Contribution graph**: `<details>` 内に snake SVG（`output` ブランチ、ライト/ダークを `<picture>` で切替）

## 編集時の注意点

- **公開物なので実名・所属は書かない。** 表示名は `Massy` のみ。
- 第三者の統計カード（github-readme-stats 等）は、レート制限で表示が崩れることと情報量の少なさから外した。戻す場合はその点を承知のうえで。
- 説明文はリポジトリの README / description を一次資料として書く。名前から推測しない。
- 新しいリポジトリを公開したら、該当する分野の表に 1 行追加する。どれにも当てはまらなければ分野を新設する。
- snake の SVG は `output` ブランチにあるので、`snake.yml` を消すと末尾の画像が止まる。

## Commit Guidelines

`Add ...` / `Update ...` / `Remove ...` の命令形で始める。
