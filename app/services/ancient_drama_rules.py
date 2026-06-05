from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AncientSceneRule:
    """Rule bundle for a common ancient-costume short-drama scene."""

    scene_type: str
    keywords: tuple[str, ...]
    foreground: str
    background: str
    lighting: str
    equipment: str
    prompt_style: str


ANCIENT_SCENE_RULES: tuple[AncientSceneRule, ...] = (
    AncientSceneRule(
        scene_type="皇宫",
        keywords=("皇宫", "宫", "宫殿", "寝殿", "御书房", "金銮殿", "御花园"),
        foreground="朱红宫柱、宫灯、香炉与垂落珠帘",
        background="金瓦殿宇、龙纹屏风、御案与层叠宫墙",
        lighting="殿内金色侧光与烛火交织，肃穆压迫，空间层次深",
        equipment="广角镜头，低机位稳定器",
        prompt_style="皇家礼制，朱红金色配色，庄严对称构图，权力压迫感",
    ),
    AncientSceneRule(
        scene_type="王府",
        keywords=("王府", "王府长廊", "王府庭院", "王府后院", "王爷府"),
        foreground="雕花廊柱、雨帘、石灯与青砖地面",
        background="王府回廊、月洞门、庭院假山与暖色灯笼",
        lighting="冷暖对比的烛火与月色，雅致中带压抑情绪",
        equipment="35mm电影镜头，稳定器缓慢推进",
        prompt_style="王府宅院，精致木作，青砖黛瓦，古装短剧质感",
    ),
    AncientSceneRule(
        scene_type="后宅",
        keywords=("后宅", "后院", "内宅", "闺房", "院内", "宅院"),
        foreground="纱帘、花窗、绣凳与半掩木门",
        background="深宅庭院、回廊阴影、侍女身影与盆景",
        lighting="柔和窗光夹杂暗部阴影，私密压抑，暗流涌动",
        equipment="50mm定焦镜头，门框式构图",
        prompt_style="深宅内院，女性古装服饰，细腻情绪，窥视感构图",
    ),
    AncientSceneRule(
        scene_type="花厅",
        keywords=("花厅", "厅中", "正厅", "偏厅", "厅内"),
        foreground="茶盏、花几、屏风边缘与垂帘",
        background="花厅陈设、木雕桌椅、插花与侍立仆从",
        lighting="室内柔光与窗棂光斑，典雅克制，人物关系紧绷",
        equipment="中焦镜头，横移轨道",
        prompt_style="古典会客花厅，礼仪感，精致陈设，人物对峙",
    ),
    AncientSceneRule(
        scene_type="书房",
        keywords=("书房", "御书房", "案前", "书案", "藏书阁"),
        foreground="案卷、烛台、砚台、毛笔与展开信笺",
        background="书架、屏风、窗棂、卷轴与烛火暗影",
        lighting="烛火暖光与窗外冷光交织，智谋感强，暗部层次明显",
        equipment="50mm定焦镜头，浅景深特写",
        prompt_style="古代书房，谋略氛围，案卷文书，高细节道具",
    ),
    AncientSceneRule(
        scene_type="京城街道",
        keywords=("京城街道", "京城", "街道", "长街", "街头", "集市", "市集", "酒楼", "客栈"),
        foreground="摊贩幡旗、行人衣袖、马车轮与街边灯笼",
        background="京城长街、商铺牌匾、人群、马车与远处城楼",
        lighting="自然天光或灯火烟火气，市井热闹，层次丰富",
        equipment="广角镜头，斯坦尼康跟拍",
        prompt_style="古代京城市井，商铺牌匾，人群烟火气，动态街景",
    ),
    AncientSceneRule(
        scene_type="城门",
        keywords=("城门", "城楼", "宫门", "城墙", "门楼"),
        foreground="旌旗、守卫长矛、马蹄尘土与厚重城门",
        background="高大城墙、城楼剪影、守军队列与远处天光",
        lighting="硬朗侧光，尘土透光，气氛紧张而开阔",
        equipment="广角镜头，低机位摇臂",
        prompt_style="古代城门，守卫列阵，旌旗猎猎，大场面史诗感",
    ),
    AncientSceneRule(
        scene_type="军营",
        keywords=("军营", "营帐", "校场", "点兵", "主营", "帐中"),
        foreground="兵器架、火盆、铠甲、战鼓与沙盘",
        background="营帐群、军旗、列队士兵、马匹与夜间火把",
        lighting="火盆暖光与冷色天光对比，肃杀紧迫，金属高光明显",
        equipment="35mm镜头，手持稳定器",
        prompt_style="古代军营，甲胄兵器，战前紧张，硬朗电影质感",
    ),
    AncientSceneRule(
        scene_type="山林",
        keywords=("山林", "密林", "竹林", "林中", "山道", "悬崖"),
        foreground="树枝、竹叶、雾气、湿石与草丛",
        background="层叠山林、蜿蜒小径、薄雾与远处人影",
        lighting="林间斑驳自然光，雾气柔化背景，危险潜伏",
        equipment="长焦镜头，跟拍稳定器",
        prompt_style="古代山林，薄雾，危险潜伏，武侠电影感",
    ),
    AncientSceneRule(
        scene_type="夜袭",
        keywords=("夜袭", "刺杀", "黑衣人", "潜入", "偷袭", "追杀", "埋伏"),
        foreground="黑衣人剪影、刀刃寒光、飞檐阴影与火把边缘",
        background="高墙屋脊、深夜庭院、巡逻守卫与冷蓝夜色",
        lighting="低照度冷蓝月光与跳动火光强反差，紧张肃杀",
        equipment="24mm广角镜头，手持跟拍，高速快切",
        prompt_style="夜袭动作场面，黑衣刺客，刀光，强反差低照度，紧张动势",
    ),
    AncientSceneRule(
        scene_type="婚宴",
        keywords=("婚宴", "大婚", "喜堂", "拜堂", "红烛", "洞房", "喜宴"),
        foreground="红烛、喜帕、酒盏、红绸与花瓣",
        background="喜堂宾客、囍字屏风、红色帷幔与灯火",
        lighting="红金暖光，烛火摇曳，喜庆表象下暗藏冲突",
        equipment="35mm镜头，环绕轨道",
        prompt_style="古代婚宴，红金色调，喜堂红烛，华丽服饰，戏剧冲突",
    ),
    AncientSceneRule(
        scene_type="公堂",
        keywords=("公堂", "衙门", "堂上", "审案", "县衙", "大堂", "惊堂木"),
        foreground="惊堂木、案桌、令签、跪地衣摆与衙役水火棍",
        background="明镜高悬匾额、堂柱、衙役队列与围观百姓",
        lighting="正面硬光与堂内阴影形成威压，庄严冷峻",
        equipment="广角镜头，低机位对称构图",
        prompt_style="古代公堂审案，明镜高悬，威严对称，强戏剧张力",
    ),
)

DEFAULT_RULE = AncientSceneRule(
    scene_type="古装场景",
    keywords=(),
    foreground="古风道具、衣袖纹理与环境遮挡形成层次",
    background="古代建筑、屏风、灯笼或自然环境延展空间",
    lighting="自然柔光结合古装置景，色调典雅，层次分明",
    equipment="35mm电影镜头，稳定器",
    prompt_style="古装短剧，电影感构图，细腻服化道，高细节",
)


def match_scene_rule(*texts: str | None) -> AncientSceneRule:
    """Return the first ancient-drama scene rule matched by supplied text fragments."""
    haystack = " ".join(text for text in texts if text)
    priority_types = {"夜袭", "婚宴", "公堂"}
    for rule in ANCIENT_SCENE_RULES:
        if rule.scene_type in priority_types and any(keyword in haystack for keyword in rule.keywords):
            return rule
    for rule in ANCIENT_SCENE_RULES:
        if any(keyword in haystack for keyword in rule.keywords):
            return rule
    return DEFAULT_RULE


def all_location_keywords() -> tuple[str, ...]:
    """Flatten all location and event keywords for scene-heading detection."""
    keywords: list[str] = []
    for rule in ANCIENT_SCENE_RULES:
        keywords.extend(rule.keywords)
    return tuple(dict.fromkeys(keywords))
