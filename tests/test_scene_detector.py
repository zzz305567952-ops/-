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


def test_detects_ancient_drama_scene_types() -> None:
    text = """第1场 后宅 花厅 内 日
夫人落座。

第2场 京城街道 外 日
百姓围观。

第3场 城门 外 黄昏
守卫列阵。

第4场 军营 主帐 内 夜
将军展开沙盘。

第5场 山林 外 晨
刺客潜伏。

第6场 夜袭 王府 外 夜
黑衣人翻上屋脊。

第7场 婚宴 喜堂 内 夜
红烛摇曳。

第8场 公堂 内 日
县令拍下惊堂木。
"""

    scenes = detect_scenes(text)

    assert [scene.scene_type for scene in scenes] == [
        "后宅",
        "京城街道",
        "城门",
        "军营",
        "山林",
        "夜袭",
        "婚宴",
        "公堂",
    ]
