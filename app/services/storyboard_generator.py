import re
from dataclasses import dataclass

from app.models.schemas import Scene, StoryboardShot

DIALOGUE_RE = re.compile(r"^(?P<speaker>[\u4e00-\u9fa5A-Za-z0-9_]{1,10})\s*[：:]\s*(?P<line>.+)$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])")

ANCIENT_STYLE_SUFFIX = "古装短剧，电影感构图，细腻服化道，高细节，cinematic lighting，16:9"


@dataclass(frozen=True)
class ShotSeed:
    kind: str
    text: str
    speaker: str | None = None
    dialogue: str = ""


def generate_storyboard(scenes: list[Scene]) -> list[StoryboardShot]:
    """Generate storyboard shots for detected scenes with deterministic film-language heuristics."""
    shots: list[StoryboardShot] = []
    for scene in scenes:
        seeds = _build_shot_seeds(scene)
        for shot_index, seed in enumerate(seeds, start=1):
            shots.append(_seed_to_shot(scene, seed, shot_index))
    return shots


def _build_shot_seeds(scene: Scene) -> list[ShotSeed]:
    seeds: list[ShotSeed] = []
    if scene.title:
        seeds.append(ShotSeed(kind="establishing", text=f"交代场景：{scene.title}"))

    for line in scene.raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        dialogue_match = DIALOGUE_RE.match(line)
        if dialogue_match:
            speaker = dialogue_match.group("speaker")
            dialogue = dialogue_match.group("line").strip()
            seeds.append(
                ShotSeed(
                    kind="dialogue",
                    text=f"{speaker}说：{dialogue}",
                    speaker=speaker,
                    dialogue=f"{speaker}：{dialogue}",
                )
            )
            continue

        for sentence in _split_action_line(line):
            seeds.append(ShotSeed(kind=_classify_action(sentence), text=sentence))

    return seeds or [ShotSeed(kind="establishing", text=f"交代场景：{scene.title or '未命名场景'}")]


def _split_action_line(line: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(line) if part.strip()]
    if not parts:
        return [line]

    merged: list[str] = []
    buffer = ""
    for part in parts:
        if not buffer:
            buffer = part
        elif len(buffer) < 18:
            buffer += part
        else:
            merged.append(buffer)
            buffer = part
    if buffer:
        merged.append(buffer)
    return merged


def _classify_action(text: str) -> str:
    if any(word in text for word in ("玉佩", "信", "血", "匕首", "酒杯", "簪", "剑", "令牌", "圣旨")):
        return "insert"
    if any(word in text for word in ("哭", "泪", "眼眶", "颤", "冷笑", "愣住", "震惊", "沉默")):
        return "emotion"
    if any(word in text for word in ("冲", "跑", "追", "打", "拔剑", "转身", "跪", "推门", "走来", "离去")):
        return "action"
    return "action"


def _seed_to_shot(scene: Scene, seed: ShotSeed, shot_index: int) -> StoryboardShot:
    sequence = f"{scene.sequence}-{shot_index}"
    shot_size = _shot_size(seed)
    camera_angle = _camera_angle(seed)
    camera_movement = _camera_movement(seed)
    duration = _duration(seed)
    visual_content = _visual_content(scene, seed)
    lighting_mood = _lighting_mood(scene, seed)
    ai_image_prompt = _ai_prompt(scene, seed, shot_size, camera_angle, lighting_mood, visual_content)

    return StoryboardShot(
        sequence=sequence,
        shot_size=shot_size,
        camera_angle=camera_angle,
        camera_movement=camera_movement,
        duration=duration,
        visual_content=visual_content,
        dialogue=seed.dialogue,
        lighting_mood=lighting_mood,
        ai_image_prompt=ai_image_prompt,
    )


def _shot_size(seed: ShotSeed) -> str:
    return {
        "establishing": "全景",
        "dialogue": "中近景",
        "emotion": "特写",
        "insert": "特写",
        "action": "中景",
    }.get(seed.kind, "中景")


def _camera_angle(seed: ShotSeed) -> str:
    if seed.kind == "establishing":
        return "平视广角"
    if seed.kind == "dialogue":
        return "平视过肩"
    if seed.kind == "emotion":
        return "平视近距离"
    if seed.kind == "insert":
        return "俯拍"
    return "平视"


def _camera_movement(seed: ShotSeed) -> str:
    if seed.kind == "establishing":
        return "缓慢推进"
    if seed.kind == "dialogue":
        return "固定镜头"
    if seed.kind == "emotion":
        return "缓慢推近"
    if seed.kind == "insert":
        return "固定特写"
    if any(word in seed.text for word in ("走来", "跑", "追", "离去", "转身")):
        return "跟拍"
    return "轻微横移"


def _duration(seed: ShotSeed) -> str:
    if seed.kind == "establishing":
        return "3秒"
    if seed.kind == "dialogue":
        length = len(seed.dialogue)
        if length > 28:
            return "5秒"
        if length > 14:
            return "4秒"
        return "3秒"
    if seed.kind in {"emotion", "insert"}:
        return "2秒"
    return "3秒"


def _visual_content(scene: Scene, seed: ShotSeed) -> str:
    if seed.kind == "establishing":
        return f"以{scene.title}作为开场交代，呈现古装环境、人物位置与戏剧情绪。"
    if seed.kind == "dialogue" and seed.speaker:
        return f"镜头对准{seed.speaker}，捕捉其神态与说话瞬间，背景保持{scene.location or scene.title}的古装氛围。"
    return seed.text


def _lighting_mood(scene: Scene, seed: ShotSeed) -> str:
    title_text = f"{scene.title} {scene.time_of_day or ''}"
    if "雨" in title_text:
        base = "雨幕冷蓝调，湿润反光，廊下烛火形成冷暖对比"
    elif "夜" in title_text:
        base = "夜色低照度，烛火摇曳，冷暖交织，氛围压抑"
    elif "晨" in title_text:
        base = "晨雾柔光，低饱和青绿色调，空气清透"
    elif "昏" in title_text or "黄昏" in title_text:
        base = "黄昏金色侧逆光，人物轮廓清晰，情绪浓烈"
    else:
        base = "自然柔光结合古装置景，色调典雅，层次分明"

    if seed.kind == "emotion":
        return f"{base}，面部阴影突出人物情绪。"
    if seed.kind == "insert":
        return f"{base}，重点物件有清晰高光与浅景深。"
    return f"{base}。"


def _ai_prompt(
    scene: Scene,
    seed: ShotSeed,
    shot_size: str,
    camera_angle: str,
    lighting_mood: str,
    visual_content: str,
) -> str:
    subject = seed.speaker or "古装人物"
    location = scene.location or scene.title or "古风场景"
    return (
        f"{subject}，{location}，{visual_content}，{shot_size}，{camera_angle}，"
        f"{lighting_mood}，{ANCIENT_STYLE_SUFFIX}"
    )
