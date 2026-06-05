from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import DialogueLine, Scene, StoryboardShot
from app.services.ancient_drama_rules import AncientSceneRule, match_scene_rule

ANCIENT_STYLE_SUFFIX = "高细节古装服化道，真实布料纹理，电影感构图，cinematic lighting，shallow depth of field，16:9"
INSERT_WORDS = ("玉佩", "信", "血", "匕首", "酒杯", "簪", "剑", "刀", "令牌", "圣旨", "惊堂木", "红烛", "喜帕")
ACTION_FAST_WORDS = ("冲", "跑", "追", "打", "拔剑", "拔刀", "刺", "逃", "夜袭", "刺杀", "黑衣人", "潜入")


@dataclass(frozen=True)
class ShotSeed:
    kind: str
    text: str
    speaker: str | None = None
    dialogue: str = ""
    emotion: str | None = None


def generate_storyboard(scenes: list[Scene]) -> list[StoryboardShot]:
    """Generate storyboard shots for analyzed scenes with ancient-drama film-language rules."""
    shots: list[StoryboardShot] = []
    for scene in scenes:
        seeds = _build_shot_seeds(scene)
        for shot_index, seed in enumerate(seeds, start=1):
            shots.append(_seed_to_shot(scene, seed, shot_index))
    return shots


def _build_shot_seeds(scene: Scene) -> list[ShotSeed]:
    seeds = [ShotSeed(kind="establishing", text=f"交代场景：{scene.title or scene.scene_type or '未命名场景'}")]

    for action in scene.actions:
        seeds.append(ShotSeed(kind=_classify_action(action, scene), text=action, emotion=_find_emotion(action, scene)))

    for dialogue in scene.dialogues:
        seeds.append(_dialogue_to_seed(dialogue, scene))

    if len(seeds) == 1 and scene.raw_text.strip():
        seeds.append(ShotSeed(kind="action", text=scene.raw_text.strip()))
    return seeds


def _dialogue_to_seed(dialogue: DialogueLine, scene: Scene) -> ShotSeed:
    emotion = _find_emotion(dialogue.content, scene)
    return ShotSeed(
        kind="emotion" if emotion else "dialogue",
        text=f"{dialogue.speaker}说：{dialogue.content}",
        speaker=dialogue.speaker,
        dialogue=dialogue.raw_text,
        emotion=emotion,
    )


def _classify_action(text: str, scene: Scene) -> str:
    if any(word in text for word in INSERT_WORDS):
        return "insert"
    if _find_emotion(text, scene):
        return "emotion"
    if any(word in text for word in ACTION_FAST_WORDS) or scene.scene_type == "夜袭":
        return "action_fast"
    return "action"


def _find_emotion(text: str, scene: Scene) -> str | None:
    return next((emotion for emotion in scene.emotions if emotion and emotion in text), None)


def _seed_to_shot(scene: Scene, seed: ShotSeed, shot_index: int) -> StoryboardShot:
    rule = match_scene_rule(scene.title, scene.location, scene.scene_type, seed.text)
    sequence = f"{scene.sequence}-{shot_index}"
    shot_size = _shot_size(seed, rule)
    camera_angle = _camera_angle(seed, rule)
    camera_movement = _camera_movement(seed, rule)
    duration = _duration(seed)
    foreground = _foreground(scene, seed, rule)
    background = _background(scene, seed, rule)
    visual_content = _visual_content(scene, seed, rule)
    lighting_mood = _lighting_mood(scene, seed, rule)
    camera_equipment = _camera_equipment(seed, rule)
    flux_prompt = _flux_prompt(
        scene=scene,
        seed=seed,
        rule=rule,
        shot_size=shot_size,
        camera_angle=camera_angle,
        camera_movement=camera_movement,
        foreground=foreground,
        background=background,
        visual_content=visual_content,
        lighting_mood=lighting_mood,
        camera_equipment=camera_equipment,
    )

    return StoryboardShot(
        sequence=sequence,
        shot_size=shot_size,
        camera_angle=camera_angle,
        camera_movement=camera_movement,
        duration=duration,
        foreground=foreground,
        background=background,
        visual_content=visual_content,
        dialogue=seed.dialogue,
        lighting_mood=lighting_mood,
        camera_equipment=camera_equipment,
        flux_prompt=flux_prompt,
    )


def _shot_size(seed: ShotSeed, rule: AncientSceneRule) -> str:
    if seed.kind == "establishing":
        return "远景" if rule.scene_type in {"城门", "军营", "山林", "京城街道"} else "全景"
    if seed.kind == "dialogue":
        return "中近景"
    if seed.kind == "emotion":
        return "特写"
    if seed.kind == "insert":
        return "特写"
    if seed.kind == "action_fast":
        return "中景"
    return "中景"


def _camera_angle(seed: ShotSeed, rule: AncientSceneRule) -> str:
    if rule.scene_type in {"皇宫", "公堂"} and seed.kind in {"establishing", "dialogue"}:
        return "低角度对称构图"
    if rule.scene_type == "夜袭":
        return "俯拍与仰拍切换"
    if rule.scene_type in {"后宅", "花厅"} and seed.kind != "establishing":
        return "侧面门框构图"
    if seed.kind == "dialogue":
        return "平视过肩"
    if seed.kind == "emotion":
        return "平视近距离"
    if seed.kind == "insert":
        return "俯拍特写"
    return "平视"


def _camera_movement(seed: ShotSeed, rule: AncientSceneRule) -> str:
    if seed.kind == "establishing":
        return "缓慢推进"
    if rule.scene_type == "夜袭" or seed.kind == "action_fast":
        return "手持快速跟拍"
    if rule.scene_type == "婚宴":
        return "环绕横移"
    if seed.kind == "dialogue":
        return "固定正反打"
    if seed.kind == "emotion":
        return "缓慢推近"
    if seed.kind == "insert":
        return "固定特写"
    return "轻微横移"


def _duration(seed: ShotSeed) -> int:
    if seed.kind == "establishing":
        return 4
    if seed.kind == "dialogue":
        length = len(seed.dialogue)
        if length > 30:
            return 6
        if length > 16:
            return 4
        return 3
    if seed.kind == "action_fast":
        return 2
    if seed.kind in {"emotion", "insert"}:
        return 3
    return 3


def _foreground(scene: Scene, seed: ShotSeed, rule: AncientSceneRule) -> str:
    if seed.kind == "insert":
        return f"重点物件贴近镜头，{rule.foreground}"
    if seed.speaker:
        return f"{seed.speaker}的衣袖、发饰与面部轮廓占据前景"
    return rule.foreground


def _background(scene: Scene, seed: ShotSeed, rule: AncientSceneRule) -> str:
    location = scene.location or scene.title or rule.scene_type
    return f"{location}空间延展，{rule.background}"


def _visual_content(scene: Scene, seed: ShotSeed, rule: AncientSceneRule) -> str:
    location = scene.location or scene.title or rule.scene_type
    if seed.kind == "establishing":
        people = "、".join(scene.characters[:3]) or "主要人物"
        return f"以{scene.title}作为开场交代，呈现{location}的空间格局、{people}的位置与古装戏剧情绪。"
    if seed.speaker:
        emotion = f"，带着{seed.emotion}情绪" if seed.emotion else ""
        return f"镜头对准{seed.speaker}{emotion}说话的瞬间，背景保持{location}的古装氛围与人物关系张力。"
    return seed.text


def _lighting_mood(scene: Scene, seed: ShotSeed, rule: AncientSceneRule) -> str:
    title_text = f"{scene.title} {scene.time_of_day or ''} {seed.text}"
    if "雨" in title_text:
        base = "雨幕冷蓝调，湿润反光，廊下烛火形成冷暖对比"
    elif "夜" in title_text or rule.scene_type == "夜袭":
        base = "低照度冷蓝夜色，火把或烛火跳动，强反差制造紧张感"
    elif "晨" in title_text or "天刚亮" in title_text:
        base = "晨雾柔光，低饱和青绿色调，空气清透"
    elif "昏" in title_text or "黄昏" in title_text or "暮色" in title_text:
        base = "黄昏金色侧逆光，人物轮廓清晰，情绪浓烈"
    else:
        base = rule.lighting

    if seed.kind == "emotion":
        return f"{base}，面部阴影突出人物情绪。"
    if seed.kind == "insert":
        return f"{base}，重点物件有清晰高光与浅景深。"
    return f"{base}。"


def _camera_equipment(seed: ShotSeed, rule: AncientSceneRule) -> str:
    if seed.kind == "emotion":
        return "85mm人像镜头，浅景深"
    if seed.kind == "insert":
        return "100mm微距镜头，固定机位"
    if seed.kind == "action_fast":
        return "24mm广角镜头，手持稳定器"
    return rule.equipment


def _flux_prompt(
    *,
    scene: Scene,
    seed: ShotSeed,
    rule: AncientSceneRule,
    shot_size: str,
    camera_angle: str,
    camera_movement: str,
    foreground: str,
    background: str,
    visual_content: str,
    lighting_mood: str,
    camera_equipment: str,
) -> str:
    subject = seed.speaker or "、".join(scene.characters[:2]) or "古装人物"
    return (
        f"古装短剧电影剧照，{subject}，{rule.scene_type}，{rule.prompt_style}，{visual_content}，"
        f"前景：{foreground}，背景：{background}，镜头：{shot_size}，{camera_angle}，{camera_movement}，"
        f"光影：{lighting_mood}，镜头设备：{camera_equipment}，{ANCIENT_STYLE_SUFFIX}"
    )
