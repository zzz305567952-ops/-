from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.models.schemas import ExportRequest, StoryboardResponse
from app.services.docx_parser import DocxParseError, parse_docx
from app.services.excel_exporter import build_storyboard_workbook
from app.services.scene_detector import detect_scenes
from app.services.script_analyzer import analyze_scenes
from app.services.storyboard_generator import generate_storyboard

app = FastAPI(
    title="古装短剧分镜生成工具",
    description="上传 Word 剧本，自动识别场景、拆分镜头并导出 Excel。",
    version="0.2.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "古装短剧分镜生成工具",
        "docs": "/docs",
        "upload_endpoint": "/api/storyboards/from-docx",
        "export_endpoint": "/api/storyboards/export-excel",
    }


@app.post("/api/storyboards/from-docx", response_model=StoryboardResponse)
async def create_storyboard_from_docx(file: UploadFile = File(...)) -> StoryboardResponse:
    """Upload a .docx script and return parsed text, detected scenes, and generated storyboard shots."""
    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="请上传 .docx 格式的 Word 剧本。")

    content = await file.read()
    try:
        text = parse_docx(content)
    except DocxParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    scenes = analyze_scenes(detect_scenes(text))
    shots = generate_storyboard(scenes)
    return StoryboardResponse(filename=file.filename, text=text, scenes=scenes, shots=shots)


@app.post("/api/storyboards/export-excel")
def export_storyboard_excel(payload: ExportRequest) -> Response:
    """Export generated or edited storyboard rows to an Excel file."""
    if not payload.shots:
        raise HTTPException(status_code=400, detail="没有可导出的分镜数据。")

    workbook_bytes = build_storyboard_workbook(payload.shots)
    headers = {"Content-Disposition": 'attachment; filename="storyboard.xlsx"'}
    return Response(
        content=workbook_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
