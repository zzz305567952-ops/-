import pytest

pytest.importorskip("pydantic", reason="pydantic 未安装；请先运行 pip install -r requirements.txt 后执行脚本分析测试。")

from app.models.schemas import Scene
from app.services.script_analyzer import analyze_scene


def test_analyzes_script_elements() -> None:
    scene = Scene(
        id="scene-1",
        sequence=1,
        title="王府 长廊 内 夜",
        location="王府",
        interior_exterior="内",
        time_of_day="夜",
        raw_text="苏清月站在廊下，眼眶含泪。\n苏清月（冷笑）：你终究还是来了。\n萧景珩从雨中走来。",
    )

    analyzed = analyze_scene(scene)

    assert analyzed.scene_type == "王府"
    assert "苏清月" in analyzed.characters
    assert "萧景珩" in analyzed.characters
    assert analyzed.dialogues[0].speaker == "苏清月"
    assert analyzed.dialogues[0].content == "你终究还是来了。"
    assert "冷笑" in analyzed.emotions
    assert any("站在廊下" in action for action in analyzed.actions)
