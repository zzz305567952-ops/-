import pytest

pytest.importorskip("pydantic", reason="pydantic 未安装；请先运行 pip install -r requirements.txt 后执行分镜生成测试。")

from app.models.schemas import Scene
from app.services.script_analyzer import analyze_scene
from app.services.storyboard_generator import generate_storyboard


def test_generates_required_storyboard_fields() -> None:
    scene = analyze_scene(
        Scene(
            id="scene-1",
            sequence=1,
            title="王府 长廊 内 夜",
            location="王府",
            interior_exterior="内",
            time_of_day="夜",
            raw_text="苏清月站在廊下，雨声淅沥。\n苏清月：你终究还是来了。\n萧景珩从雨中走来。",
        )
    )

    shots = generate_storyboard([scene])

    assert [shot.sequence for shot in shots] == ["1-1", "1-2", "1-3", "1-4"]
    assert shots[0].shot_size == "全景"
    assert shots[0].foreground
    assert shots[0].background
    assert shots[0].camera_equipment
    assert shots[2].dialogue == "苏清月：你终究还是来了。"
    assert shots[2].flux_prompt
    assert "Flux" not in shots[2].flux_prompt
    assert shots[2].lighting_mood


def test_generates_night_raid_specific_camera_language() -> None:
    scene = analyze_scene(
        Scene(
            id="scene-1",
            sequence=1,
            title="夜袭 王府 屋脊 外 夜",
            location="王府",
            interior_exterior="外",
            time_of_day="夜",
            raw_text="黑衣人潜入屋脊，拔刀刺向侍卫。",
        )
    )

    shots = generate_storyboard([scene])

    assert scene.scene_type == "王府" or scene.scene_type == "夜袭"
    assert any(shot.camera_movement == "手持快速跟拍" for shot in shots)
    assert any("夜袭动作场面" in shot.flux_prompt or "王府宅院" in shot.flux_prompt for shot in shots)
