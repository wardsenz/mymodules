# -*- coding: utf-8 -*-
#     FTG Shortener
#     Copyright (C) 2020 h3xcode

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils
import logging
import asyncio
import re
import requests
import json


logger = logging.getLogger(__name__)


@loader.tds
class ShortMod(loader.Module):
    """Shorting long URL's"""
    strings = {"name": "Shorter",
               "need_link": "<b>Ссылка не указана</b>",
               "key_not_found": "<b>API ключ не найден</b>",
               "result": "<b>Ссылка:</b> {}",
               "error": "<b>Ошибка:</b> {}",
               "doc_client_key": "Ключ из https://hydrugz.live/red/user/tools (Development API)",
               "doc_api_url": "Адрес АПИ"}

    def __init__(self):
        self.config = loader.ModuleConfig("CLIENT_KEY", "KEY", lambda m: self.strings("doc_client_key", m),
                                          "API_URL", "https://kutr.ml/api/", lambda m: self.strings("doc_api_url", m))

    async def shortcmd(self, message):
        """.short <link>"""
        args = utils.get_args(message)
        if self.config["CLIENT_KEY"] == "KEY":
            await utils.answer(message, self.strings("key_not_found", message))
            return
        if message.is_reply:
            url = (await message.get_reply_message()).text
        else:
            if len(args) == 0:
                await utils.answer(message, self.strings("need_link", message))
                return
            url = args[0]
        params = {"url": url,
                  "key": self.config["CLIENT_KEY"]}
        req = requests.get(self.config["API_URL"], params=params).text
        shrt = json.loads(re.sub('hydrugz.live/red/', 'kutr.ml/', str(req)))
        if shrt["error"]:
            await utils.answer(message, self.strings("error", message).format(shrt["msg"]))
        else:
            await utils.answer(message, self.strings("result", message).format(shrt["short"].replace("https://hydrugz.live/red/", "kutr.ml/")))
