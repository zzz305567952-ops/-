from pydantic import BaseModel, Field


class DialogueLine(BaseModel):
    """A structured dialogue line detected from script text."""

    speaker: str = Field(description="人物")
    content: str = Field(description="对白内容")
    raw_text: str = Field(description="原始对白行")


class Scene(BaseModel):
    """A detected script scene with structured screenplay elements."""

    id: str
    sequence: int
    title: str
    location: str | None = None
    interior_exterior: str | None = Field(default=None, description="内/外/内外")
    time_of_day: str | None = None
    raw_text: str
    characters: list[str] = Field(default_factory=list, description="人物")
    actions: list[str] = Field(default_factory=list, description="动作")
    dialogues: list[DialogueLine] = Field(default_factory=list, description="对白")
    emotions: list[str] = Field(default_factory=list, description="情绪")
    scene_type: str | None = Field(default=None, description="古装剧场景类型")


class StoryboardShot(BaseModel):
    """A generated storyboard shot row."""

    sequence: str = Field(description="镜头序列")
    shot_size: str = Field(description="景别")
    camera_angle: str = Field(description="拍摄角度")
    camera_movement: str = Field(description="运镜")
    duration: int = Field(description="时长(s)")
    foreground: str = Field(description="前景")
    background: str = Field(description="背景")
    visual_content: str = Field(description="画面内容")
    dialogue: str = Field(description="台词")
    lighting_mood: str = Field(description="光影氛围")
    camera_equipment: str = Field(description="镜头设备")
    flux_prompt: str = Field(description="Flux绘图提示词")


class StoryboardResponse(BaseModel):
    """Full analysis response for an uploaded script."""

    filename: str
    text: str
    scenes: list[Scene]
    shots: list[StoryboardShot]


class ExportRequest(BaseModel):
    """Request body for exporting storyboard shots to Excel."""

    shots: list[StoryboardShot]
