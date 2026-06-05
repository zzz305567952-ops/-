import pytest

pytest.importorskip("openpyxl", reason="openpyxl 未安装；请先运行 pip install -r requirements.txt 后执行 Excel 导出测试。")
pytest.importorskip("pydantic", reason="pydantic 未安装；请先运行 pip install -r requirements.txt 后执行模型相关测试。")

from io import BytesIO

from openpyxl import load_workbook

from app.models.schemas import StoryboardShot
from app.services.excel_exporter import HEADERS, build_storyboard_workbook


def test_build_storyboard_workbook() -> None:
    shot = StoryboardShot(
        sequence="1-1",
        shot_size="全景",
        camera_angle="平视",
        camera_movement="缓慢推进",
        duration="3秒",
        visual_content="王府长廊雨夜。",
        dialogue="",
        lighting_mood="冷蓝雨夜。",
        ai_image_prompt="古装人物，王府长廊。",
    )

    workbook_bytes = build_storyboard_workbook([shot])
    workbook = load_workbook(BytesIO(workbook_bytes))
    worksheet = workbook.active

    assert [cell.value for cell in worksheet[1]] == HEADERS
    assert worksheet["A2"].value == "1-1"
    assert worksheet["F2"].value == "王府长廊雨夜。"
