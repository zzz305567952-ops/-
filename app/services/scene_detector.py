import re
from dataclasses import dataclass

from app.models.schemas import Scene
from app.services.ancient_drama_rules import all_location_keywords, match_scene_rule

SCENE_HEADING_PATTERNS = [
    re.compile(r"^(?:第\s*)?[一二三四五六七八九十百零〇两\d]+\s*[场幕]\b[：:、.．\s-]*(?P<title>.+)?$"),
    re.compile(r"^场景\s*[一二三四五六七八九十百零〇两\d]+[：:、.．\s-]*(?P<title>.+)?$"),
    re.compile(r"^[（(【\[]?(?:内景|外景|内|外)?\s*[一二三四五六七八九十百零〇两\d]+[、.．]\s*(?P<title>.+)$"),
    re.compile(r"^[【\[](?P<title>.+)[】\]]$"),
]

LOCATION_WORDS = (
    *all_location_keywords(),
    "殿", "庭院", "长廊", "牢房", "地牢", "祠堂", "湖边", "河边", "房间", "屋内", "门外", "院内",
)
TIME_WORDS = ("日", "夜", "晨", "昏", "清晨", "黄昏", "雨夜", "雪夜", "午后", "傍晚", "深夜", "天刚亮", "夜色", "暮色")
INTERIOR_EXTERIOR_WORDS = ("内", "外", "内景", "外景")
EVENT_LOCATION_SKIP_WORDS = ("夜袭", "刺杀", "偷袭", "追杀", "埋伏", "婚宴", "大婚")


@dataclass(frozen=True)
class HeadingCandidate:
    line_index: int
    title: str


def detect_scenes(text: str) -> list[Scene]:
    """Detect screenplay scenes from cleaned text using robust screenplay heading heuristics."""
    lines = [line.strip() for line in text.splitlines()]
    headings = _find_headings(lines)

    if not headings:
        return [
            Scene(
                id="scene-1",
                sequence=1,
                title="未命名场景",
                location=None,
                interior_exterior=None,
                time_of_day=None,
                raw_text=text.strip(),
                scene_type=match_scene_rule(text).scene_type,
            )
        ]

    scenes: list[Scene] = []
    for index, heading in enumerate(headings):
        next_line_index = headings[index + 1].line_index if index + 1 < len(headings) else len(lines)
        scene_lines = [line for line in lines[heading.line_index + 1 : next_line_index] if line]
        raw_text = "\n".join(scene_lines).strip()
        metadata = _extract_scene_metadata(heading.title)
        scenes.append(
            Scene(
                id=f"scene-{index + 1}",
                sequence=index + 1,
                title=heading.title,
                location=metadata["location"],
                interior_exterior=metadata["interior_exterior"],
                time_of_day=metadata["time_of_day"],
                raw_text=raw_text,
                scene_type=match_scene_rule(heading.title, metadata["location"], raw_text).scene_type,
            )
        )

    return scenes


def _find_headings(lines: list[str]) -> list[HeadingCandidate]:
    candidates: list[HeadingCandidate] = []
    for index, line in enumerate(lines):
        if not line:
            continue
        title = _match_explicit_heading(line)
        if title:
            candidates.append(HeadingCandidate(index, title))
            continue
        if _looks_like_semantic_heading(line):
            candidates.append(HeadingCandidate(index, line.strip("【】[] ")))
    return candidates


def _match_explicit_heading(line: str) -> str | None:
    for pattern in SCENE_HEADING_PATTERNS:
        match = pattern.match(line)
        if not match:
            continue
        title = (match.groupdict().get("title") or line).strip("：:、.． -")
        if title and not _looks_like_dialogue(title):
            return title
    return None


def _looks_like_semantic_heading(line: str) -> bool:
    if len(line) > 32 or _looks_like_dialogue(line):
        return False
    has_location = any(word in line for word in LOCATION_WORDS)
    has_time = any(re.search(rf"(?:^|[·/\s-]){re.escape(word)}(?:$|[·/\s-])", line) for word in TIME_WORDS)
    has_interior = any(re.search(rf"(?:^|[·/\s-]){re.escape(word)}(?:$|[·/\s-])", line) for word in INTERIOR_EXTERIOR_WORDS)
    return has_location and (has_time or has_interior)


def _looks_like_dialogue(line: str) -> bool:
    return bool(re.match(r"^[\u4e00-\u9fa5A-Za-z0-9_]{1,8}\s*[：:]", line))


def _extract_scene_metadata(title: str) -> dict[str, str | None]:
    tokens = [token for token in re.split(r"[·/\s｜|,，、-]+", title) if token]
    interior_exterior = next((token for token in tokens if token in INTERIOR_EXTERIOR_WORDS), None)
    time_of_day = next((token for token in tokens if token in TIME_WORDS), None)

    location = None
    for token in tokens:
        if token in INTERIOR_EXTERIOR_WORDS or token in TIME_WORDS or token in EVENT_LOCATION_SKIP_WORDS:
            continue
        if any(word in token for word in LOCATION_WORDS) or len(token) >= 2:
            location = token
            break

    return {
        "location": location,
        "interior_exterior": interior_exterior,
        "time_of_day": time_of_day,
    }
