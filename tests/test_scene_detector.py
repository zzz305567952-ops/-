import pytest

pytest.importorskip("pydantic", reason="pydantic 未安装；请先运行 pip install -r requirements.txt 后执行场景识别测试。")

from app.services.scene_detector import detect_scenes


def test_detects_common_scene_headings() -> None:
    text = """第1场 王府 长廊 内 夜
苏清月站在廊下。
苏清月：你终究还是来了。

场景二：皇宫 御书房 内 日
皇帝展开圣旨。
"""

    scenes = detect_scenes(text)

    assert len(scenes) == 2
    assert scenes[0].sequence == 1
    assert scenes[0].location == "王府"
    assert scenes[0].interior_exterior == "内"
    assert scenes[0].time_of_day == "夜"
    assert "苏清月" in scenes[0].raw_text
    assert scenes[1].sequence == 2
    assert scenes[1].location == "皇宫"


def test_falls_back_to_single_scene_when_no_heading() -> None:
    scenes = detect_scenes("苏清月站在廊下。\n萧景珩：我来了。")

    assert len(scenes) == 1
    assert scenes[0].title == "未命名场景"
