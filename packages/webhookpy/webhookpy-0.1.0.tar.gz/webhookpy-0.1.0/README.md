[![pytest](https://github.com/nattoujam/webhookpy/actions/workflows/pytest.yml/badge.svg)](https://github.com/nattoujam/webhookpy/actions/workflows/pytest.yml)

# webhookpy
webhook送信用のコマンド

## Quick Start
```bash
pip install webhookpy

name=test       # 登録名
url=https://... # webhookのURL
channel=channel # 投稿するチャンネル名
bot=bot         # botの名前

webhook add $name $url $channel $bot -d

webhook post hello!
```

## Usage
```bash
webhook --help
```
