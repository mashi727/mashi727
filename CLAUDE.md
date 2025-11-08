# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

このリポジトリは、GitHubプロフィールページ（README.md）を管理するための専用リポジトリです。コードベースは含まれず、マークダウンコンテンツと自動化ワークフローで構成されています。

## Repository Structure

```
github-profile/
├── README.md                      # GitHubプロフィールページの内容
└── .github/
    └── workflows/
        ├── update-activity.yml    # 6時間ごとに最近のアクティビティを更新
        └── snake.yml             # 日次でコントリビューショングラフを生成（現在未使用）
```

## README.md の構成

README.mdは以下のセクションで構成されています：

1. **About Me**: 簡単な自己紹介と現在のフォーカスエリア
2. **Stats（左カラム）**:
   - Profile Views カウンター
   - GitHub Stats（コミット数、PR数など）
   - GitHub Streak（連続コントリビューション）
   - Most Used Languages
   - Tech Stack（使用言語、ツール、フレームワーク）
3. **Featured Projects（右カラム）**: 注目プロジェクトのリスト（名前、説明、技術スタック）
4. **Contribution Activity**: 年間のコントリビューショングラフと最近のアクティビティ

## GitHub Actions Workflows

### update-activity.yml
- **実行頻度**: 6時間ごと（cron: '0 */6 * * *'）、または手動トリガー
- **機能**: `jamesgeorge007/github-activity-readme@master` アクションを使用して、README.mdの `<!--START_SECTION:activity-->` から `<!--END_SECTION:activity-->` の間に最近のGitHubアクティビティを自動挿入
- **設定**: 最大5行のアクティビティを表示

### snake.yml
- **状態**: 現在コメントアウトまたは未使用（README.mdにはスネーク可視化が含まれていない）
- **機能**: `Platane/snk/svg-only@v3` を使用してコントリビューショングラフのSVGアニメーションを生成

## 編集時の注意点

### READMEの更新

READMEを編集する際は以下の点に注意：

1. **アクティビティセクションのマーカー保持**: `<!--START_SECTION:activity-->` と `<!--END_SECTION:activity-->` のコメントは削除しないこと（GitHub Actionsが自動更新に使用）

2. **外部サービスのURL構造**:
   - GitHub Stats: `https://github-readme-stats.vercel.app/api?username=mashi727&...`
   - Streak Stats: `https://github-readme-streak-stats.herokuapp.com/?user=mashi727&...`
   - Language Stats: `https://github-readme-stats.vercel.app/api/top-langs/?username=mashi727&...`
   - Profile Views: `https://komarev.com/ghpvc/?username=mashi727&...`
   - Contribution Graph: `https://ghchart.rshah.org/2ea043/mashi727`

3. **テーブルレイアウト**: 2カラムのテーブル構造（左30%: Stats、右70%: Featured Projects）を維持すること

4. **プロジェクトリンクの形式**:
   ```markdown
   ### 🎵 [Project Name](https://github.com/username/repo-name)
   Brief description
   `Tech` `Stack` `Tags`
   ```

### ワークフローの手動実行

```bash
# GitHub CLIを使用してワークフローを手動トリガー
gh workflow run update-activity.yml
gh workflow run snake.yml
```

### ローカルでのプレビュー

GitHubのマークダウンレンダリングをローカルで確認：

```bash
# grip（GitHub Readme Instant Preview）を使用
pip install grip
grip README.md

# ブラウザで http://localhost:6419 を開く
```

## Commit Guidelines

このリポジトリへのコミットメッセージの一般的なパターン：

- `Add [feature/section]`: 新しいセクションやプロジェクトの追加
- `Update [section]`: 既存コンテンツの更新
- `Remove [feature/section]`: セクションや要素の削除
- `Change [element] to [new format]`: レイアウトや形式の変更
- `Revert to [previous state]`: 以前の状態への復帰

## プロジェクトの追加・更新

新しいプロジェクトをFeatured Projectsに追加する際の手順：

1. プロジェクト名（絵文字付き）とGitHubリポジトリURLを設定
2. 1-2文の簡潔な説明を記載
3. 使用している主要技術をバッククォートで囲んだタグとして列挙
4. 既存のプロジェクトとの順序・重要度を考慮して配置

例：
```markdown
### 🎵 [Rehearsal Workflow](https://github.com/mashi727/rehearsal-workflow)
AI-powered tool that transforms orchestra rehearsal videos into detailed reports with chapters
`Python` `Claude AI` `Whisper` `LuaTeX`
```
