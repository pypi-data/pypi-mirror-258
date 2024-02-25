#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : config.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/13
# Last Modified Date: 2023 11/19
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Optional

import yaml

DEFAULT_HOOK_KEY = 'default'
EMPTY = ''
RESERVED_WORDS = [DEFAULT_HOOK_KEY, EMPTY]


class Hook(NamedTuple):
    app: str
    name: str
    url: str
    channel: str
    bot_name: str


class Config:
    @staticmethod
    def load(config_path: Path) -> Config:
        if config_path.exists():
            with open(config_path, 'r') as f:
                return Config(yaml.safe_load(f))
        else:
            config_path.parent.mkdir(parents=True)
            config_path.touch()
            return Config()

    @staticmethod
    def reserved_words() -> List[str]:
        return RESERVED_WORDS

    def __init__(self, d: dict = dict()):
        self.d: dict = d

    def __contains__(self, name: str) -> bool:
        if self.d is None:
            return False

        return name in self.d.keys()

    @property
    def names(self) -> List[str]:
        if self.d is None:
            return []

        n = list(self.d.keys())
        n.remove('default')
        return n

    @property
    def default(self) -> Optional[str]:
        if DEFAULT_HOOK_KEY not in self.d:
            return None
        elif self.d[DEFAULT_HOOK_KEY] == EMPTY:
            return None
        else:
            return self.d[DEFAULT_HOOK_KEY]

    @property
    def hooks(self) -> List[Hook]:
        return [Hook(v['app'], k, v['url'], v['channel'], v['bot_name']) for k, v in self.d.items() if k != DEFAULT_HOOK_KEY]

    def hook(self, name: str) -> Optional[Hook]:
        hook = self.d[name] if name in self.d else None
        if hook is None:
            return None
        else:
            return Hook(hook['app'], name, hook['url'], hook['channel'], hook['bot_name'])

    def empty(self) -> bool:
        if self.d is None:
            return True

        return len(self.d.keys()) <= 1

    def set_default(self, name: str) -> Config:
        return Config({**self.d, DEFAULT_HOOK_KEY: name})

    def add(self, name: str, url: str, channel: str, bot_name: str, app: str) -> Config:
        adding_config = {
            name: {
                'app': app,
                'url': url,
                'channel': channel,
                'bot_name': bot_name
            }
        }
        if self.d is None:
            return Config({DEFAULT_HOOK_KEY: name, **adding_config})
        elif DEFAULT_HOOK_KEY in self.d:
            return Config({**self.d, **adding_config})
        else:
            return Config({DEFAULT_HOOK_KEY: name, **self.d, **adding_config})

    def remove(self, name: str) -> Config:
        d = {**self.d}
        if name == self.default:
            d[DEFAULT_HOOK_KEY] = EMPTY
        return Config({k: v for k, v in d.items() if k != name})

    def dump(self, config_path: Path):
        if not config_path.exists():
            config_path.parent.mkdir(parents=True)

        with open(config_path, 'w') as f:
            f.write(yaml.dump(self.d))
