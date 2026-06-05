# 古装短剧分镜生成工具

一个基于 **FastAPI + Python** 的第二阶段工具，用于上传 Word 剧本，自动解析文本、识别场景、拆分镜头，并导出 Excel 分镜表。

## 第二阶段功能

- 上传 `.docx` 剧本文件
- 使用 `python-docx` 解析剧本文本
- 自动识别常见场景标题格式
- 结构化识别剧本元素：
  - 场景
  - 人物
  - 动作
  - 对白
  - 情绪
  - 时间
  - 地点
- 按场景自动拆分镜头
- 生成古装短剧分镜字段：
  - 镜头序列
  - 景别
  - 拍摄角度
  - 运镜
  - 时长(s)
  - 前景
  - 背景
  - 画面内容
  - 台词
  - 光影氛围
  - 镜头设备
  - Flux绘图提示词
- 内置古装剧专用规则：皇宫、王府、后宅、花厅、书房、京城街道、城门、军营、山林、夜袭、婚宴、公堂
- 使用 `openpyxl` 按固定中文表头导出 `.xlsx` Excel 文件

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

`scenes` 中会包含 `characters`、`actions`、`dialogues`、`emotions`、`scene_type` 等结构化识别结果。

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
      "duration": 4,
      "foreground": "雕花廊柱、雨帘、石灯与青砖地面",
      "background": "王府空间延展，王府回廊、月洞门、庭院假山与暖色灯笼",
      "visual_content": "以王府 长廊 内 夜作为开场交代，呈现王府的空间格局、主要人物的位置与古装戏剧情绪。",
      "dialogue": "",
      "lighting_mood": "低照度冷蓝夜色，火把或烛火跳动，强反差制造紧张感。",
      "camera_equipment": "35mm电影镜头，稳定器缓慢推进",
      "flux_prompt": "古装短剧电影剧照，古装人物，王府，王府宅院，精致木作，青砖黛瓦，古装短剧质感，..."
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
夜袭 王府 外 夜
婚宴 喜堂 内 夜
公堂 内 日
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

当前第二阶段继续使用规则算法完成自动识别和分镜生成，优先保证本地可运行和完整链路闭环。后续可以接入大模型，将 `app/services/script_analyzer.py` 或 `app/services/storyboard_generator.py` 中的规则生成替换或增强为 AI 生成，以获得更细腻的镜头语言和绘图提示词。
