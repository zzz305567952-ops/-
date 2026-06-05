from __future__ import annotations

import re

from app.models.schemas import DialogueLine, Scene
from app.services.ancient_drama_rules import match_scene_rule

DIALOGUE_RE = re.compile(
    r"^(?P<speaker>[\u4e00-\u9fa5A-Za-z0-9_]{1,12})(?:[（(](?P<mood>[^）)]+)[）)])?\s*[：:]\s*(?P<line>.+)$"
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])")

CHARACTER_TITLES = (
    "皇帝", "太后", "皇后", "贵妃", "王爷", "王妃", "世子", "郡主", "公主", "太子", "将军", "大人",
    "夫人", "小姐", "少爷", "丫鬟", "侍女", "侍卫", "捕快", "县令", "师爷", "嬷嬷", "新娘", "新郎",
)
ACTION_KEYWORDS = (
    "走", "跑", "冲", "追", "跪", "转身", "回头", "推门", "拔剑", "落座", "起身", "扶", "摔", "打",
    "拦", "递", "接", "饮酒", "掀帘", "跪拜", "行礼", "叩首", "展开", "握", "攥", "拔刀", "刺", "逃",
    "潜入", "翻身", "上马", "下马", "闯入", "退后", "逼近", "离去", "走来",
)
EMOTION_KEYWORDS = (
    "愤怒", "惊恐", "冷笑", "悲伤", "哭", "落泪", "泪", "哽咽", "隐忍", "慌张", "犹豫", "震惊",
    "羞怯", "怨恨", "杀意", "失落", "得意", "颤", "眼眶", "愣住", "沉默", "怒", "惧", "喜", "悲",
)
TIME_HINTS = ("日", "夜", "晨", "昏", "清晨", "黄昏", "雨夜", "雪夜", "午后", "傍晚", "深夜", "天刚亮", "夜色", "暮色")


def analyze_scenes(scenes: list[Scene]) -> list[Scene]:
    """Enrich detected scenes with characters, actions, dialogues, emotions and ancient-drama scene type."""
    return [analyze_scene(scene) for scene in scenes]


def analyze_scene(scene: Scene) -> Scene:
    """Return a copy of a scene with structured screenplay elements populated."""
    characters: list[str] = []
    actions: list[str] = []
    dialogues: list[DialogueLine] = []
    emotions: list[str] = []

    for line in scene.raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        dialogue_match = DIALOGUE_RE.match(line)
        if dialogue_match:
            speaker = dialogue_match.group("speaker").strip()
            content = dialogue_match.group("line").strip()
            _append_unique(characters, speaker)
            dialogues.append(DialogueLine(speaker=speaker, content=content, raw_text=line))
            mood = dialogue_match.groupdict().get("mood")
            if mood:
                _append_unique(emotions, mood.strip())
            _collect_emotions(content, emotions)
            continue

        for character in _find_characters(line):
            _append_unique(characters, character)
        for sentence in _split_action_line(line):
            if _looks_like_action(sentence):
                _append_unique(actions, sentence)
            _collect_emotions(sentence, emotions)

    scene_type = match_scene_rule(scene.title, scene.location, scene.raw_text).scene_type
    time_of_day = scene.time_of_day or _find_time_hint(scene.raw_text)

    return scene.model_copy(
        update={
            "characters": characters,
            "actions": actions,
            "dialogues": dialogues,
            "emotions": emotions,
            "time_of_day": time_of_day,
            "scene_type": scene_type,
        }
    )


def _split_action_line(line: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(line) if part.strip()]
    return parts or [line]


def _looks_like_action(text: str) -> bool:
    return any(keyword in text for keyword in ACTION_KEYWORDS) or not DIALOGUE_RE.match(text)


def _find_characters(text: str) -> list[str]:
    found = [title for title in CHARACTER_TITLES if title in text]
    # Capture likely Chinese names at the beginning of action lines, e.g. 苏清月站在廊下 / 萧景珩从雨中走来.
    leading_name = re.match(
        r"(?P<name>[\u4e00-\u9fa5]{2,4})(?=从|在|向|对|朝|站|走|跑|跪|哭|笑|怒|拔|推|转|回|递|接|扶|坐|起|看|望|闯|冲)",
        text,
    )
    if leading_name:
        found.append(leading_name.group("name"))

    for match in re.finditer(
        r"(?P<name>[\u4e00-\u9fa5]{2,4})(?=站|走|跑|跪|哭|笑|怒|拔|推|转|回|递|接|扶|坐|起|看|望|闯|冲|潜入)",
        text,
    ):
        name = match.group("name")
        if name not in CHARACTER_TITLES:
            found.append(name)
    return list(dict.fromkeys(found))


def _collect_emotions(text: str, emotions: list[str]) -> None:
    for keyword in EMOTION_KEYWORDS:
        if keyword in text:
            _append_unique(emotions, keyword)


def _find_time_hint(text: str) -> str | None:
    for hint in TIME_HINTS:
        if hint in text:
            return hint
    return None


def _append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)
