# 古装短剧分镜生成工具

一个基于 **FastAPI + Python** 的 MVP 工具，用于上传 Word 剧本，自动解析文本、识别场景、拆分镜头，并导出 Excel 分镜表。

## MVP 功能

- 上传 `.docx` 剧本文件
- 使用 `python-docx` 解析剧本文本
- 自动识别常见场景标题格式
- 按场景自动拆分镜头
- 生成分镜字段：
  - 镜头序列
  - 景别
  - 拍摄角度
  - 运镜
  - 时长
  - 画面内容
  - 台词
  - 光影氛围
  - AI绘图提示词
- 使用 `openpyxl` 导出 `.xlsx` Excel 文件

## 技术栈

- FastAPI
- Python
- python-docx
- openpyxl
- Pydantic
- pytest

## 本地运行说明

> 当前仓库不会在测试或启动脚本中自动联网安装依赖。若运行环境可以访问 PyPI，请在本地手动安装依赖后启动服务。

### 1. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell 可使用：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 安装运行依赖

```bash
pip install -r requirements.txt
```

### 3. 启动 FastAPI

```bash
uvicorn app.main:app --reload
```

这两个命令是最小本地运行命令：

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后访问：

- API 根路径：<http://127.0.0.1:8000/>
- Swagger 文档：<http://127.0.0.1:8000/docs>

## API

### 上传 Word 并生成分镜

```http
POST /api/storyboards/from-docx
Content-Type: multipart/form-data
```

表单字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| file | File | `.docx` Word 剧本 |

返回内容包含：

- `filename`：上传文件名
- `text`：解析后的剧本文本
- `scenes`：识别出的场景
- `shots`：生成的分镜行

### 导出 Excel

```http
POST /api/storyboards/export-excel
Content-Type: application/json
```

请求体示例：

```json
{
  "shots": [
    {
      "sequence": "1-1",
      "shot_size": "全景",
      "camera_angle": "平视广角",
      "camera_movement": "缓慢推进",
      "duration": "3秒",
      "visual_content": "以王府 长廊 内 夜作为开场交代，呈现古装环境、人物位置与戏剧情绪。",
      "dialogue": "",
      "lighting_mood": "夜色低照度，烛火摇曳，冷暖交织，氛围压抑。",
      "ai_image_prompt": "古装人物，王府，以王府 长廊 内 夜作为开场交代，呈现古装环境、人物位置与戏剧情绪。，全景，平视广角，夜色低照度，烛火摇曳，冷暖交织，氛围压抑。，古装短剧，电影感构图，细腻服化道，高细节，cinematic lighting，16:9"
    }
  ]
}
```

返回：`storyboard.xlsx`。

## 支持的场景标题示例

```text
第1场 王府 长廊 内 夜
场景二：皇宫 御书房 内 日
1. 客栈 外 雨夜
【山林·外·晨】
王府 / 内 / 夜
```

## 测试

完整测试需要先安装开发依赖：

```bash
pip install -r requirements-dev.txt
pytest
```

如果当前环境无法访问 PyPI，导致 `fastapi`、`pydantic`、`python-docx`、`openpyxl` 等依赖缺失，测试会使用 `pytest.importorskip` 清晰跳过依赖相关用例，而不是在收集阶段报 `ModuleNotFoundError`。

离线环境仍可运行不依赖第三方包的静态检查：

```bash
python -m compileall app tests
pytest -q
```

## 说明

当前 MVP 使用规则算法完成自动识别和分镜生成，优先保证本地可运行和完整链路闭环。后续可以接入大模型，将 `app/services/storyboard_generator.py` 中的规则生成替换或增强为 AI 生成，以获得更细腻的镜头语言和绘图提示词。
