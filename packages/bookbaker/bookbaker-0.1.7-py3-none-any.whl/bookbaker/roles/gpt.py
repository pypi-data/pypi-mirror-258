from __future__ import annotations

import ujson as json
import asyncio
from random import randint
from typing import overload
from uuid import uuid4
from pydantic import Field
from asynctinydb import Query
from gptbot import Bot, Message, Role, Model
from ..misc import LANG_NAME_TABLE
from ..utils import escape_ruby, unescape_ruby
from ..classes import Context, Task
from ..classes import Book, Chapter, Episode
from .base import BaseTranslator


class GPTTranslator(BaseTranslator):
    """
    # GPTTranslator Class
    """
    name: str = Field(default_factory=lambda: f"gpt-{str(uuid4())[:8]}")
    description: str = "GPT Translator"
    max_retries: int | None = 10
    """Max retries before giving up"""
    batch_size: int = 512
    """Max characters to send in one batch"""
    max_tokens: int | None = 5000
    """Max tokens to preserve"""
    remind_interval: int | None = 10
    """Interval to remind glossaries"""
    skip_translated: bool = True
    """Skip already translated lines"""
    convert_ruby: bool = True
    """Convert <ruby> tags to simpler format for LLMs"""
    backend: Bot = Field(
        default_factory=lambda: Bot(model=Model.GPT4TurboPreview, api_key=''))

    async def translate(
            self,
            episode: Episode,
            task: Task,
            ctx: Context,
            chapter: Chapter | None = None,
            book: Book | None = None,
    ) -> Episode:

        if episode.fully_translated and self.skip_translated:
            return episode

        cli = ctx.client
        self.backend._cli = cli
        db = ctx.db
        sauce_lang = LANG_NAME_TABLE.get(task.sauce_lang.upper(), task.sauce_lang)
        target_lang = LANG_NAME_TABLE.get(task.target_lang.upper(), task.target_lang)
        logger = ctx.logger
        sess = self.backend.new_session()

        prompt = (
            "You are a professional translator, "
            f"translating text from {sauce_lang} "
            f"into fluent and native {target_lang}.\n"
            "Add the missing subject to the sentence.\n"
            "Translated nouns and pronouns must be consistent\n"
            "Rephrase sentences to make them more natural, correct errors in original content if any.\n"
            "For json input, you must output a valid json with same keys and translated values "
            "For pure text, you must output exact the same line count as input and keep '\\n' and [](^) if any\n"
        )
        if task.glossaries:
            prompt += "Translation reference you must follow, you will be constantly reminded:\n"
            prompt += '\n'.join(f"{k} : {v}" for k, v in task.glossaries)
        if book is not None:
            prompt += "\nThe book you are translating:\n"
            book_full_meta = {
                "title": book.title,
                "description": book.description,
                "series": book.series,
                "tags": list(book.tags),
            }
            prompt += f"{json.dumps(book_full_meta, ensure_ascii=False)}\n"

        prompt += "\nThe episode you are translating:\n"
        episode_meta: dict[str, str | None] = {
            "title": episode.title,
            "notes": episode.notes,
        }
        prompt += f"{json.dumps(episode_meta, ensure_ascii=False)}\n"
        prompt += "\nYou can start translating now:"

        logger.debug("%s: generated prompt: %s", self, prompt)

        self.backend.prompt = prompt

        def remind():
            if task.glossaries:
                logger.debug("%s: Sending reminder", self)
                sess.append(
                    Message(role=Role.User, content=f"[{", ".join(g[0] for g in task.glossaries)}]"))
                sess.append(
                    Message(role=Role.Assistant, content=f"[{", ".join(g[1] for g in task.glossaries)}]"))
        remind()
        cycle = 0

        @overload
        async def translate(c: dict[str, str | None]) -> dict[str, str | None]:
            ...

        @overload
        async def translate(c: list[str]) -> list[str]:
            ...

        async def translate(
                c: list[str] | dict[str, str | None]
        ) -> list[str] | dict[str, str | None]:
            nonlocal cycle
            if isinstance(c, dict):
                pstr = json.dumps(c, ensure_ascii=False)
            else:
                pstr = '\n'.join(map(lambda x: x.replace('\n', r"\n"), c))

            if self.convert_ruby:
                pstr = escape_ruby(pstr)

            logger.debug("%s: Sending prompt: %s", self, pstr)
            sess.trim(self.max_tokens)
            sess_bak = sess.messages.copy()

            retry = 0

            while True:
                self.backend.seed = randint(0, 10000)
                resp: str = "None"
                try:
                    resp = await sess.send(pstr, ensure_json=False)

                    if self.convert_ruby:
                        resp = unescape_ruby(resp)

                    logger.debug("%s: Received response: %s", self, resp)
                    if isinstance(c, list):
                        obj = resp.split('\n')
                        obj = list(
                            filter(None, map(lambda x: x.replace(r"\n", '\n'), obj)))
                        if not isinstance(obj, list):
                            raise TypeError("Expected list, got dict")
                        if len(obj) != len(c):
                            raise ValueError("Length mismatch")
                    else:
                        obj = json.loads(resp)
                        if not isinstance(obj, dict):
                            raise TypeError("Expected dict, got list")
                        if obj.keys() != c.keys():
                            raise ValueError("Key mismatch")

                    return obj

                except Exception as e:
                    logger.debug("%s: Failed to get valid response: %s", self, resp)
                    logger.exception(e)
                    sess.messages = sess_bak
                    retry += 1
                    if self.max_retries is not None and retry > self.max_retries:
                        raise RuntimeError(
                            "Failed to get valid response in %d retries" % self.max_retries)
                    await asyncio.sleep(1)
                    continue

                finally:
                    cycle += 1
                    if self.remind_interval is not None and cycle >= self.remind_interval:
                        remind()
                        cycle = 0

        if book is not None and None in (
            book.title_translated,
            book.description_translated,
            book.series_translated if book.series else ''
        ):
            book_meta: dict[str, str | None] = {
                "title": book.title,
                "description": book.description,
                "series": book.series
            }
            book_meta = await translate(book_meta)
            book.title_translated = book_meta["title"]
            book.description_translated = book_meta["description"]
            book.series_translated = book_meta["series"]

        if chapter is not None and chapter.title_translated is None:
            chapter_meta: dict[str, str | None] = {
                "title": chapter.title
            }
            chapter_meta = await translate(chapter_meta)
            chapter.title_translated = chapter_meta["title"]

        episode_meta = await translate(episode_meta)
        episode.title_translated = episode_meta["title"]
        episode.notes_translated = episode_meta["notes"]

        indexes = list[int]()
        contents = list[str]()
        c_cnt = 0
        MAX_CNT = self.batch_size

        for i, line in enumerate(episode.lines):
            if not line.content.strip():
                continue
            if self.skip_translated and line.translated is not None:
                continue
            indexes.append(i)
            contents.append(line.content)
            c_cnt += len(line.content)
            if c_cnt > MAX_CNT:
                translated = await translate(contents)
                for j, v in zip(indexes, translated):
                    o = episode.lines[j].content
                    line = episode.lines[j]
                    line.translated = v
                    line.candidates[self.name] = v
                    if not v.strip():
                        logger.warning("%s: Empty translation for %d", self, o)
                indexes.clear()
                contents.clear()
                c_cnt = 0

        if indexes:
            translated = await translate(contents)
            for j, v in zip(indexes, translated):
                line = episode.lines[j]
                line.translated = v
                line.candidates[self.name] = v
                for j, v in zip(indexes, translated):
                    o = episode.lines[j].content
                    line = episode.lines[j]
                    line.translated = v
                    line.candidates[self.name] = v
                    if not v.strip():
                        logger.warning("%s: Empty translation for %s", self, o)

        q = Query()
        if book is not None:
            await db.upsert(book.model_dump(mode="json"),
                            q.title == book.title and q.author == book.author)

        return episode
