# poker-hand-evaluator

同一の仕様書（`SPEC.md`）から作成した、ポーカー役判定プログラムの **2つの実装** と、その比較レビューを収めたリポジトリです。

## 構成

| パス | 内容 |
|---|---|
| [`pocker1/`](pocker1/) | 単一ファイル実装（`python_poker.py` のみ、152行） |
| [`pocker2/`](pocker2/) | パッケージ分割実装（`poker/` パッケージ ＋ pytest テスト58件） |
| [`REVIEW.md`](REVIEW.md) | 2実装の検証・比較レビューレポート |

`pocker1/SPEC.md` と `pocker2/SPEC.md` は同一内容です。

## 使い方

どちらの実装も同じ CLI インターフェースを持ちます。

```bash
python pocker1/python_poker.py "AS, KS, QS, JS, TS" "9H, 9D, 9C, 2S, 2H"
python pocker2/python_poker.py "AS, KS, QS, JS, TS" "9H, 9D, 9C, 2S, 2H"
```

出力:

```
Hand 1: AS, KS, QS, JS, TS => Royal Flush
Hand 2: 9H, 9D, 9C, 2S, 2H => Full House
Winner: Hand 1
```

## テスト（pocker2 のみ）

```bash
cd pocker2 && python3 -m pytest
```

> **注意**: 現状 `pytest.ini` に `pythonpath` の設定がないため、素の `pytest` ではなく `python3 -m pytest` で実行する必要があります。詳細は [`REVIEW.md`](REVIEW.md) の不具合①を参照。

## レビュー結果の要約

全 2,598,960 通り（52C5）の手札を網羅検証した結果、**両実装とも役判定・タイブレーカーに誤りはありません**。
不具合はテスト起動・例外設計・API 堅牢性といった周辺に集中しています。詳細は [`REVIEW.md`](REVIEW.md) を参照してください。
