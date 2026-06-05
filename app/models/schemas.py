from pydantic import BaseModel, Field


class Scene(BaseModel):
    """A detected script scene."""

    id: str
    sequence: int
    title: str
    location: str | None = None
    interior_exterior: str | None = Field(default=None, description="内/外/内外")
    time_of_day: str | None = None
    raw_text: str


class StoryboardShot(BaseModel):
    """A generated storyboard shot row."""

    sequence: str = Field(description="镜头序列")
    shot_size: str = Field(description="景别")
    camera_angle: str = Field(description="拍摄角度")
    camera_movement: str = Field(description="运镜")
    duration: str = Field(description="时长")
    visual_content: str = Field(description="画面内容")
    dialogue: str = Field(description="台词")
    lighting_mood: str = Field(description="光影氛围")
    ai_image_prompt: str = Field(description="AI绘图提示词")


class StoryboardResponse(BaseModel):
    """Full analysis response for an uploaded script."""

    filename: str
    text: str
    scenes: list[Scene]
    shots: list[StoryboardShot]


class ExportRequest(BaseModel):
    """Request body for exporting storyboard shots to Excel."""

    shots: list[StoryboardShot]
