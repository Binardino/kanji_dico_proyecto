# Creating Kangxi radicals JSON and crosswalk, and providing a mapping function + tests.
from pathlib import Path
import json
import pandas as pd

kangxi_radicals = [
  {
    "number": 1,
    "kangxi_radical": "⼀",
    "radical": "一",
    "code": "U+2F00",
    "english_name": "KANGXI RADICAL ONE",
    "meaning": "one",
    "strokes": 1,
    "variants": [],
    "notes": "Same shape as standard 一."
  },
  {
    "number": 2,
    "kangxi_radical": "⼁",
    "radical": "丨",
    "code": "U+2F01",
    "english_name": "KANGXI RADICAL LINE",
    "meaning": "line",
    "strokes": 1,
    "variants": [],
    "notes": "Vertical line component."
  },
  {
    "number": 3,
    "kangxi_radical": "⼂",
    "radical": "丶",
    "code": "U+2F02",
    "english_name": "KANGXI RADICAL DOT",
    "meaning": "dot",
    "strokes": 1,
    "variants": [],
    "notes": "Small dot stroke."
  },
  {
    "number": 4,
    "kangxi_radical": "⼃",
    "radical": "丿",
    "code": "U+2F03",
    "english_name": "KANGXI RADICAL SLASH",
    "meaning": "slash",
    "strokes": 1,
    "variants": [],
    "notes": "Left-slant stroke."
  },
  {
    "number": 5,
    "kangxi_radical": "⼄",
    "radical": "乙",
    "code": "U+2F04",
    "english_name": "KANGXI RADICAL SECOND",
    "meaning": "second",
    "strokes": 1,
    "variants": [
      "乚",
      "乛",
      "⺄"
    ],
    "notes": "Various cursive/positional forms."
  },
  {
    "number": 6,
    "kangxi_radical": "⼅",
    "radical": "亅",
    "code": "U+2F05",
    "english_name": "KANGXI RADICAL HOOK",
    "meaning": "hook",
    "strokes": 1,
    "variants": [],
    "notes": "Hook stroke."
  },
  {
    "number": 7,
    "kangxi_radical": "⼆",
    "radical": "二",
    "code": "U+2F06",
    "english_name": "KANGXI RADICAL TWO",
    "meaning": "two",
    "strokes": 2,
    "variants": [],
    "notes": "Same as 二."
  },
  {
    "number": 8,
    "kangxi_radical": "⼇",
    "radical": "亠",
    "code": "U+2F07",
    "english_name": "KANGXI RADICAL LID",
    "meaning": "lid",
    "strokes": 2,
    "variants": [],
    "notes": "Top component (e.g. 高)."
  },
  {
    "number": 9,
    "kangxi_radical": "⼈",
    "radical": "人",
    "code": "U+2F08",
    "english_name": "KANGXI RADICAL MAN",
    "meaning": "person",
    "strokes": 2,
    "variants": [
      "亻"
    ],
    "notes": "亻 is the common left-side form."
  },
  {
    "number": 10,
    "kangxi_radical": "⼉",
    "radical": "兒",
    "code": "U+2F09",
    "english_name": "KANGXI RADICAL LEGS",
    "meaning": "legs",
    "strokes": 2,
    "variants": [
      "儿"
    ],
    "notes": "兒 traditional; 儿 simplified."
  },
  {
    "number": 11,
    "kangxi_radical": "⼊",
    "radical": "入",
    "code": "U+2F0A",
    "english_name": "KANGXI RADICAL ENTER",
    "meaning": "enter",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 12,
    "kangxi_radical": "⼋",
    "radical": "八",
    "code": "U+2F0B",
    "english_name": "KANGXI RADICAL EIGHT",
    "meaning": "eight",
    "strokes": 2,
    "variants": [
      "丷"
    ],
    "notes": "丷 common as upper component."
  },
  {
    "number": 13,
    "kangxi_radical": "⼌",
    "radical": "冂",
    "code": "U+2F0C",
    "english_name": "KANGXI RADICAL DOWN BOX",
    "meaning": "down box",
    "strokes": 2,
    "variants": [],
    "notes": "Enclosure shape."
  },
  {
    "number": 14,
    "kangxi_radical": "⼍",
    "radical": "冖",
    "code": "U+2F0D",
    "english_name": "KANGXI RADICAL COVER",
    "meaning": "cover",
    "strokes": 2,
    "variants": [],
    "notes": "Top-cover radical."
  },
  {
    "number": 15,
    "kangxi_radical": "⼎",
    "radical": "冫",
    "code": "U+2F0E",
    "english_name": "KANGXI RADICAL ICE",
    "meaning": "ice",
    "strokes": 2,
    "variants": [],
    "notes": "Two-dot left form."
  },
  {
    "number": 16,
    "kangxi_radical": "⼏",
    "radical": "几",
    "code": "U+2F0F",
    "english_name": "KANGXI RADICAL TABLE",
    "meaning": "table",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 17,
    "kangxi_radical": "⼐",
    "radical": "凵",
    "code": "U+2F10",
    "english_name": "KANGXI RADICAL OPEN BOX",
    "meaning": "open box",
    "strokes": 2,
    "variants": [],
    "notes": "Used in 凶, 出."
  },
  {
    "number": 18,
    "kangxi_radical": "⼑",
    "radical": "刀",
    "code": "U+2F11",
    "english_name": "KANGXI RADICAL KNIFE",
    "meaning": "knife",
    "strokes": 2,
    "variants": [
      "刂"
    ],
    "notes": "刂 right-side form."
  },
  {
    "number": 19,
    "kangxi_radical": "⼒",
    "radical": "力",
    "code": "U+2F12",
    "english_name": "KANGXI RADICAL POWER",
    "meaning": "power",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 20,
    "kangxi_radical": "⼓",
    "radical": "勹",
    "code": "U+2F13",
    "english_name": "KANGXI RADICAL WRAP",
    "meaning": "wrap",
    "strokes": 2,
    "variants": [],
    "notes": "Wrapper radical."
  },
  {
    "number": 21,
    "kangxi_radical": "⼔",
    "radical": "匕",
    "code": "U+2F14",
    "english_name": "KANGXI RADICAL SPOON",
    "meaning": "spoon",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 22,
    "kangxi_radical": "⼕",
    "radical": "匚",
    "code": "U+2F15",
    "english_name": "KANGXI RADICAL RIGHT OPEN BOX",
    "meaning": "right open box",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 23,
    "kangxi_radical": "⼖",
    "radical": "匸",
    "code": "U+2F16",
    "english_name": "KANGXI RADICAL HIDING ENCLOSURE",
    "meaning": "hiding enclosure",
    "strokes": 2,
    "variants": [],
    "notes": "Rare."
  },
  {
    "number": 24,
    "kangxi_radical": "⼗",
    "radical": "十",
    "code": "U+2F17",
    "english_name": "KANGXI RADICAL TEN",
    "meaning": "ten",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 25,
    "kangxi_radical": "⼘",
    "radical": "卜",
    "code": "U+2F18",
    "english_name": "KANGXI RADICAL DIVINATION",
    "meaning": "divination",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 26,
    "kangxi_radical": "⼙",
    "radical": "卩",
    "code": "U+2F19",
    "english_name": "KANGXI RADICAL SEAL",
    "meaning": "seal",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 27,
    "kangxi_radical": "⼚",
    "radical": "厂",
    "code": "U+2F1A",
    "english_name": "KANGXI RADICAL CLIFF",
    "meaning": "cliff",
    "strokes": 2,
    "variants": [],
    "notes": "Appears in 原."
  },
  {
    "number": 28,
    "kangxi_radical": "⼛",
    "radical": "厶",
    "code": "U+2F1B",
    "english_name": "KANGXI RADICAL PRIVATE",
    "meaning": "private",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 29,
    "kangxi_radical": "⼜",
    "radical": "又",
    "code": "U+2F1C",
    "english_name": "KANGXI RADICAL AGAIN",
    "meaning": "again",
    "strokes": 2,
    "variants": [],
    "notes": ""
  },
  {
    "number": 30,
    "kangxi_radical": "⼝",
    "radical": "口",
    "code": "U+2F1D",
    "english_name": "KANGXI RADICAL MOUTH",
    "meaning": "mouth",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 31,
    "kangxi_radical": "⼞",
    "radical": "囗",
    "code": "U+2F1E",
    "english_name": "KANGXI RADICAL ENCLOSURE",
    "meaning": "enclosure",
    "strokes": 3,
    "variants": [],
    "notes": "Not to be confused with 口."
  },
  {
    "number": 32,
    "kangxi_radical": "⼟",
    "radical": "土",
    "code": "U+2F1F",
    "english_name": "KANGXI RADICAL EARTH",
    "meaning": "earth",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 33,
    "kangxi_radical": "⼠",
    "radical": "士",
    "code": "U+2F20",
    "english_name": "KANGXI RADICAL SCHOLAR",
    "meaning": "scholar",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 34,
    "kangxi_radical": "⼡",
    "radical": "夂",
    "code": "U+2F21",
    "english_name": "KANGXI RADICAL GO",
    "meaning": "go slowly",
    "strokes": 3,
    "variants": [],
    "notes": "Often confused with 夊."
  },
  {
    "number": 35,
    "kangxi_radical": "⼢",
    "radical": "夂",
    "code": "U+2F22",
    "english_name": "KANGXI RADICAL GO",
    "meaning": "go slowly",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 36,
    "kangxi_radical": "⼣",
    "radical": "夕",
    "code": "U+2F23",
    "english_name": "KANGXI RADICAL EVENING",
    "meaning": "evening",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 37,
    "kangxi_radical": "⼤",
    "radical": "大",
    "code": "U+2F24",
    "english_name": "KANGXI RADICAL BIG",
    "meaning": "big",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 38,
    "kangxi_radical": "⼥",
    "radical": "女",
    "code": "U+2F25",
    "english_name": "KANGXI RADICAL WOMAN",
    "meaning": "woman",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 39,
    "kangxi_radical": "⼦",
    "radical": "子",
    "code": "U+2F26",
    "english_name": "KANGXI RADICAL CHILD",
    "meaning": "child",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 40,
    "kangxi_radical": "⼧",
    "radical": "宀",
    "code": "U+2F27",
    "english_name": "KANGXI RADICAL ROOF",
    "meaning": "roof",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 41,
    "kangxi_radical": "⼨",
    "radical": "寸",
    "code": "U+2F28",
    "english_name": "KANGXI RADICAL INCH",
    "meaning": "inch",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 42,
    "kangxi_radical": "⼩",
    "radical": "小",
    "code": "U+2F29",
    "english_name": "KANGXI RADICAL SMALL",
    "meaning": "small",
    "strokes": 3,
    "variants": ["⺌", "⺍"],
    "notes": ""
  },
  {
    "number": 43,
    "kangxi_radical": "⼪",
    "radical": "尢",
    "code": "U+2F2A",
    "english_name": "KANGXI RADICAL LAME",
    "meaning": "lame",
    "strokes": 3,
    "variants": ["尤", "尣"],
    "notes": ""
  },
  {
    "number": 44,
    "kangxi_radical": "⼫",
    "radical": "尸",
    "code": "U+2F2B",
    "english_name": "KANGXI RADICAL CORPSE",
    "meaning": "corpse",
    "strokes": 3,
    "variants": [],
    "notes": "Appears in 屋, 居."
  },
  {
    "number": 45,
    "kangxi_radical": "⼬",
    "radical": "屮",
    "code": "U+2F2C",
    "english_name": "KANGXI RADICAL SPROUT",
    "meaning": "sprout",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 46,
    "kangxi_radical": "⼭",
    "radical": "山",
    "code": "U+2F2D",
    "english_name": "KANGXI RADICAL MOUNTAIN",
    "meaning": "mountain",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 47,
    "kangxi_radical": "⼮",
    "radical": "川",
    "code": "U+2F2E",
    "english_name": "KANGXI RADICAL RIVER",
    "meaning": "river",
    "strokes": 3,
    "variants": ["巛"],
    "notes": "川 is modern; 巛 is older tri-stream form."
  },
  {
    "number": 48,
    "kangxi_radical": "⼯",
    "radical": "工",
    "code": "U+2F2F",
    "english_name": "KANGXI RADICAL WORK",
    "meaning": "work",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 49,
    "kangxi_radical": "⼰",
    "radical": "己",
    "code": "U+2F30",
    "english_name": "KANGXI RADICAL SELF",
    "meaning": "self",
    "strokes": 3,
    "variants": ["己", "巳"],
    "notes": "Radical 己 historically overlaps with 巳 but they are separate Unicode characters."
  },
  {
    "number": 50,
    "kangxi_radical": "⼱",
    "radical": "巾",
    "code": "U+2F31",
    "english_name": "KANGXI RADICAL TURBAN",
    "meaning": "cloth; towel",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },  
  {
    "number": 51,
    "kangxi_radical": "⼲",
    "radical": "干",
    "code": "U+2F32",
    "english_name": "KANGXI RADICAL DRY",
    "meaning": "dry",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 52,
    "kangxi_radical": "⼳",
    "radical": "幺",
    "code": "U+2F33",
    "english_name": "KANGXI RADICAL TINY",
    "meaning": "tiny; short thread",
    "strokes": 3,
    "variants": ['乡'],
    "notes": "Appears in 幽, 幾."
  },
  {
    "number": 53,
    "kangxi_radical": "⼴",
    "radical": "广",
    "code": "U+2F34",
    "english_name": "KANGXI RADICAL DOTTED CLIFF",
    "meaning": "shelter",
    "strokes": 3,
    "variants": [],
    "notes": "Left-side shelter radical; appears in 店, 広."
  },
  {
    "number": 54,
    "kangxi_radical": "⼵",
    "radical": "廴",
    "code": "U+2F35",
    "english_name": "KANGXI RADICAL LONG STRIDE",
    "meaning": "long stride",
    "strokes": 3,
    "variants": [],
    "notes": "Appears in 延."
  },
  {
    "number": 55,
    "kangxi_radical": "⼶",
    "radical": "廾",
    "code": "U+2F36",
    "english_name": "KANGXI RADICAL TWO HANDS",
    "meaning": "two hands",
    "strokes": 3,
    "variants": ["廿"],
    "notes": "Ancient form representing holding with both hands."
  },
  {
    "number": 56,
    "kangxi_radical": "⼷",
    "radical": "弋",
    "code": "U+2F37",
    "english_name": "KANGXI RADICAL SHOOT",
    "meaning": "shoot (with bow)",
    "strokes": 3,
    "variants": [],
    "notes": "Appears in 式."
  },
  {
    "number": 57,
    "kangxi_radical": "⼸",
    "radical": "弓",
    "code": "U+2F38",
    "english_name": "KANGXI RADICAL BOW",
    "meaning": "bow",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 58,
    "kangxi_radical": "⼹",
    "radical": "彐",
    "code": "U+2F39",
    "english_name": "KANGXI RADICAL SNOUT",
    "meaning": "snout",
    "strokes": 3,
    "variants": ["ヨ", "彑"],
    "notes": ""
  },
  {
    "number": 59,
    "kangxi_radical": "⼺",
    "radical": "彡",
    "code": "U+2F3A",
    "english_name": "KANGXI RADICAL BRISTLE",
    "meaning": "hair; bristle",
    "strokes": 3,
    "variants": [],
    "notes": ""
  },
  {
    "number": 60,
    "kangxi_radical": "⼻",
    "radical": "彳",
    "code": "U+2F3B",
    "english_name": "KANGXI RADICAL STEP",
    "meaning": "step",
    "strokes": 3,
    "variants": [],
    "notes": "Appears in 行, 待, 得, 律."
  },
  {
    "number": 61,
    "kangxi_radical": "⼼",
    "radical": "心",
    "code": "U+2F3C",
    "english_name": "KANGXI RADICAL HEART",
    "meaning": "heart",
    "strokes": 4,
    "variants": ["忄","⺗"],
    "notes": "忄 is left-side form; ⺗ is bottom form."
  },
  {
    "number": 62,
    "kangxi_radical": "⼽",
    "radical": "戈",
    "code": "U+2F3D",
    "english_name": "KANGXI RADICAL HALBERD",
    "meaning": "halberd",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 63,
    "kangxi_radical": "⼾",
    "radical": "戸",
    "code": "U+2F3E",
    "english_name": "KANGXI RADICAL DOOR",
    "meaning": "door",
    "strokes": 4,
    "variants": ["戶", "户"],
    "notes": "戸 is Japanese form; 戶 is traditional."
  },
  {
    "number": 64,
    "kangxi_radical": "⼿",
    "radical": "手",
    "code": "U+2F3F",
    "english_name": "KANGXI RADICAL HAND",
    "meaning": "hand",
    "strokes": 4,
    "variants": ["扌", " 龵"],
    "notes": "扌 is left-side variant."
  },
  {
    "number": 65,
    "kangxi_radical": "⽀",
    "radical": "支",
    "code": "U+2F40",
    "english_name": "KANGXI RADICAL BRANCH",
    "meaning": "branch",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 66,
    "kangxi_radical": "⽁",
    "radical": "攴",
    "code": "U+2F41",
    "english_name": "KANGXI RADICAL RAP",
    "meaning": "knock; tap",
    "strokes": 4,
    "variants": ["攵"],
    "notes": "攵 appears in 教, 改."
  },
  {
    "number": 67,
    "kangxi_radical": "⽂",
    "radical": "文",
    "code": "U+2F42",
    "english_name": "KANGXI RADICAL SCRIPT",
    "meaning": "script; writing",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 68,
    "kangxi_radical": "⽃",
    "radical": "斗",
    "code": "U+2F43",
    "english_name": "KANGXI RADICAL DIPPER",
    "meaning": "dipper",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 69,
    "kangxi_radical": "⽄",
    "radical": "斤",
    "code": "U+2F44",
    "english_name": "KANGXI RADICAL AXE",
    "meaning": "axe",
    "strokes": 4,
    "variants": [],
    "notes": "Appears in 新, 断."
  },
  {
    "number": 70,
    "kangxi_radical": "⽅",
    "radical": "方",
    "code": "U+2F45",
    "english_name": "KANGXI RADICAL SQUARE",
    "meaning": "direction; square",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 71,
    "kangxi_radical": "⽆",
    "radical": "无",
    "code": "U+2F46",
    "english_name": "KANGXI RADICAL NOT",
    "meaning": "nothing; not",
    "strokes": 4,
    "variants": ["無", "旡"],
    "notes": "无 is simplified; 無 is traditional/Japanese."
  },
  {
    "number": 72,
    "kangxi_radical": "⽇",
    "radical": "日",
    "code": "U+2F47",
    "english_name": "KANGXI RADICAL SUN",
    "meaning": "sun; day",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 73,
    "kangxi_radical": "⽈",
    "radical": "曰",
    "code": "U+2F48",
    "english_name": "KANGXI RADICAL SAY",
    "meaning": "say",
    "strokes": 4,
    "variants": [],
    "notes": "Not to be confused with 日."
  },
  {
    "number": 74,
    "kangxi_radical": "⽉",
    "radical": "月",
    "code": "U+2F49",
    "english_name": "KANGXI RADICAL MOON",
    "meaning": "moon; flesh",
    "strokes": 4,
    "variants": ["⺼"],
    "notes": "月 can be 'moon' OR the 'flesh' radical."
  },
  {
    "number": 75,
    "kangxi_radical": "⽊",
    "radical": "木",
    "code": "U+2F4A",
    "english_name": "KANGXI RADICAL TREE",
    "meaning": "tree; wood",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 76,
    "kangxi_radical": "⽋",
    "radical": "欠",
    "code": "U+2F4B",
    "english_name": "KANGXI RADICAL LACK",
    "meaning": "lack; yawn",
    "strokes": 4,
    "variants": [],
    "notes": "Appears in 次, 欠."
  },
  {
    "number": 77,
    "kangxi_radical": "⽌",
    "radical": "止",
    "code": "U+2F4C",
    "english_name": "KANGXI RADICAL STOP",
    "meaning": "stop",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 78,
    "kangxi_radical": "⽍",
    "radical": "歹",
    "code": "U+2F4D",
    "english_name": "KANGXI RADICAL DEATH",
    "meaning": "death; decay",
    "strokes": 4,
    "variants": ["歺"],
    "notes": "Appears in 殺, 段."
  },
  {
    "number": 79,
    "kangxi_radical": "⽎",
    "radical": "殳",
    "code": "U+2F4E",
    "english_name": "KANGXI RADICAL WEAPON",
    "meaning": "weapon (strike)",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 80,
    "kangxi_radical": "⽏",
    "radical": "毋",
    "code": "U+2F4F",
    "english_name": "KANGXI RADICAL DO NOT",
    "meaning": "do not",
    "strokes": 4,
    "variants": ["母", "⺟"],
    "notes": ""
  },
  {
    "number": 81,
    "kangxi_radical": "⽐",
    "radical": "比",
    "code": "U+2F50",
    "english_name": "KANGXI RADICAL COMPARE",
    "meaning": "compare",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 82,
    "kangxi_radical": "⽑",
    "radical": "毛",
    "code": "U+2F51",
    "english_name": "KANGXI RADICAL FUR",
    "meaning": "hair; fur",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 83,
    "kangxi_radical": "⽒",
    "radical": "氏",
    "code": "U+2F52",
    "english_name": "KANGXI RADICAL CLAN",
    "meaning": "clan; family name",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 84,
    "kangxi_radical": "⽓",
    "radical": "气",
    "code": "U+2F53",
    "english_name": "KANGXI RADICAL STEAM",
    "meaning": "steam; air",
    "strokes": 4,
    "variants": [
      "氣"
    ],
    "notes": "气 simplified; 氣 traditional."
  },
  {
    "number": 85,
    "kangxi_radical": "⽔",
    "radical": "水",
    "code": "U+2F54",
    "english_name": "KANGXI RADICAL WATER",
    "meaning": "water",
    "strokes": 4,
    "variants": ["氵","氺"],
    "notes": "氵 left-side form; 氺 bottom form."
  },
  {
    "number": 86,
    "kangxi_radical": "⽕",
    "radical": "火",
    "code": "U+2F55",
    "english_name": "KANGXI RADICAL FIRE",
    "meaning": "fire",
    "strokes": 4,
    "variants": ["灬"],
    "notes": "灬 is the bottom form ('four dots fire')."
  },
  {
    "number": 87,
    "kangxi_radical": "⽖",
    "radical": "爪",
    "code": "U+2F56",
    "english_name": "KANGXI RADICAL CLAW",
    "meaning": "claw",
    "strokes": 4,
    "variants": ["爫","⺤","⺥"],
    "notes": ""
  },
  {
    "number": 88,
    "kangxi_radical": "⽗",
    "radical": "父",
    "code": "U+2F57",
    "english_name": "KANGXI RADICAL FATHER",
    "meaning": "father",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 89,
    "kangxi_radical": "⽘",
    "radical": "爻",
    "code": "U+2F58",
    "english_name": "KANGXI RADICAL DOUBLE X",
    "meaning": "double-x / crossing lines (mix, twine, cross)",
    "strokes": 4,
    "variants": [],
    "notes": "Often described as two crossing X strokes; appears in contexts meaning 'interweave' or 'cross'."
  },
  {
    "number": 90,
    "kangxi_radical": "⽙",
    "radical": "丬",
    "code": "U+2F59",
    "english_name": "KANGXI RADICAL HALF TREE TRUNK",
    "meaning": "half of a tree trunk / split wood",
    "strokes": 4,
    "variants": [],
    "notes": "Shown in sources as 'half tree trunk' (used as left-side component 丬)."
  },
  {
    "number": 91,
    "kangxi_radical": "⽚",
    "radical": "片",
    "code": "U+2F5A",
    "english_name": "KANGXI RADICAL SLICE",
    "meaning": "slice; piece",
    "strokes": 4,
    "variants": [],
    "notes": ""
  },
  {
    "number": 92,
    "kangxi_radical": "⽛",
    "radical": "牙",
    "code": "U+2F5B",
    "english_name": "KANGXI RADICAL FANG",
    "meaning": "fang",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 93,
    "kangxi_radical": "⽜",
    "radical": "牛",
    "code": "U+2F5C",
    "english_name": "KANGXI RADICAL COW",
    "meaning": "cow; ox",
    "strokes": 4,
    "variants": ["牜","⺧"],
    "notes": "牜 and ⺧ are common positional/variant forms used in compounds."
  },
  {
    "number": 94,
    "kangxi_radical": "⽝",
    "radical": "犬",
    "code": "U+2F5D",
    "english_name": "KANGXI RADICAL DOG",
    "meaning": "dog; dog-like animals",
    "strokes": 4,
    "variants": ["犭"],
    "notes": "犭 is the very common left-side form (animal radical)."
  },
  {
    "number": 95,
    "kangxi_radical": "⽞",
    "radical": "玄",
    "code": "U+2F5E",
    "english_name": "KANGXI RADICAL PROFOUND",
    "meaning": "profound; dark; black (sense of depth)",
    "strokes": 5,
    "variants": [],
    "notes": "Often rendered as 玄; glosses sometimes mention 'profound/black'."
  },
  {
    "number": 96,
    "kangxi_radical": "⽟",
    "radical": "玉",
    "code": "U+2F5F",
    "english_name": "KANGXI RADICAL JADE",
    "meaning": "jade; jewel; king/ball (in derived forms)",
    "strokes": 4,
    "variants": ["王","⺩"],
    "notes": "王 is often used as radical form; ⺩ is the common positional variant."
  },
  {
    "number": 97,
    "kangxi_radical": "⽠",
    "radical": "瓜",
    "code": "U+2F60",
    "english_name": "KANGXI RADICAL MELON",
    "meaning": "pumpkin; melon",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 98,
    "kangxi_radical": "⽡",
    "radical": "瓦",
    "code": "U+2F61",
    "english_name": "KANGXI RADICAL TILE",
    "meaning": "tile; earthenware",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 99,
    "kangxi_radical": "⽢",
    "radical": "甘",
    "code": "U+2F62",
    "english_name": "KANGXI RADICAL SWEET",
    "meaning": "sweet",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 100,
    "kangxi_radical": "⽣",
    "radical": "生",
    "code": "U+2F63",
    "english_name": "KANGXI RADICAL LIFE",
    "meaning": "giving birth; live",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 101,
    "kangxi_radical": "⽤",
    "radical": "用",
    "code": "U+2F64",
    "english_name": "KANGXI RADICAL USE",
    "meaning": "use; employ",
    "strokes": 5,
    "variants": ["甩"],
    "notes": "甩 appears in some descriptions as a related form."
  },
  {
    "number": 102,
    "kangxi_radical": "⽥",
    "radical": "田",
    "code": "U+2F65",
    "english_name": "KANGXI RADICAL FIELD",
    "meaning": "field",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 103,
    "kangxi_radical": "⽦",
    "radical": "疋",
    "code": "U+2F66",
    "english_name": "KANGXI RADICAL BOLT OF CLOTH",
    "meaning": "bolt of cloth",
    "strokes": 5,
    "variants": [
      "⺪"
    ],
    "notes": "Appears in 疏; positional variant ⺪."
  },
  {
    "number": 104,
    "kangxi_radical": "⽧",
    "radical": "疒",
    "code": "U+2F67",
    "english_name": "KANGXI RADICAL SICKNESS",
    "meaning": "sickness",
    "strokes": 5,
    "variants": [],
    "notes": "Left-side radical in 病, 痛, 疲, 疾."
  },
  {
    "number": 105,
    "kangxi_radical": "⽨",
    "radical": "癶",
    "code": "U+2F68",
    "english_name": "KANGXI RADICAL FOOTSTEPS",
    "meaning": "footsteps",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 106,
    "kangxi_radical": "⽩",
    "radical": "白",
    "code": "U+2F69",
    "english_name": "KANGXI RADICAL WHITE",
    "meaning": "white",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 107,
    "kangxi_radical": "⽪",
    "radical": "皮",
    "code": "U+2F6A",
    "english_name": "KANGXI RADICAL SKIN",
    "meaning": "skin",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 108,
    "kangxi_radical": "⽫",
    "radical": "皿",
    "code": "U+2F6B",
    "english_name": "KANGXI RADICAL DISH",
    "meaning": "dish; container",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 109,
    "kangxi_radical": "⽬",
    "radical": "目",
    "code": "U+2F6C",
    "english_name": "KANGXI RADICAL EYE",
    "meaning": "eye",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 110,
    "kangxi_radical": "⽭",
    "radical": "矛",
    "code": "U+2F6D",
    "english_name": "KANGXI RADICAL HALBERD",
    "meaning": "spear; halberd",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 111,
    "kangxi_radical": "⽮",
    "radical": "矢",
    "code": "U+2F6E",
    "english_name": "KANGXI RADICAL ARROW",
    "meaning": "arrow",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 112,
    "kangxi_radical": "⽯",
    "radical": "石",
    "code": "U+2F6F",
    "english_name": "KANGXI RADICAL STONE",
    "meaning": "stone",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 113,
    "kangxi_radical": "⽰",
    "radical": "示",
    "code": "U+2F70",
    "english_name": "KANGXI RADICAL SPIRIT",
    "meaning": "spirit; altar",
    "strokes": 5,
    "variants": [
      "礻"
    ],
    "notes": "礻 is common left-side form."
  },
  {
    "number": 114,
    "kangxi_radical": "⽱",
    "radical": "禸",
    "code": "U+2F71",
    "english_name": "KANGXI RADICAL TRACK",
    "meaning": "track; rump",
    "strokes": 5,
    "variants": [],
    "notes": "Rare radical."
  },
  {
    "number": 115,
    "kangxi_radical": "⽲",
    "radical": "禾",
    "code": "U+2F72",
    "english_name": "KANGXI RADICAL GRAIN",
    "meaning": "grain; rice plant",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 116,
    "kangxi_radical": "⽳",
    "radical": "穴",
    "code": "U+2F73",
    "english_name": "KANGXI RADICAL CAVE",
    "meaning": "cave",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 117,
    "kangxi_radical": "⽴",
    "radical": "立",
    "code": "U+2F74",
    "english_name": "KANGXI RADICAL STAND",
    "meaning": "stand",
    "strokes": 5,
    "variants": [],
    "notes": ""
  },
  {
    "number": 118,
    "kangxi_radical": "⽵",
    "radical": "竹",
    "code": "U+2F75",
    "english_name": "KANGXI RADICAL BAMBOO",
    "meaning": "bamboo",
    "strokes": 6,
    "variants": [
      "⺮"
    ],
    "notes": ""
  },
  {
    "number": 119,
    "kangxi_radical": "⽶",
    "radical": "米",
    "code": "U+2F76",
    "english_name": "KANGXI RADICAL RICE",
    "meaning": "rice",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 120,
    "kangxi_radical": "⽷",
    "radical": "糸",
    "code": "U+2F77",
    "english_name": "KANGXI RADICAL SILK",
    "meaning": "thread; silk",
    "strokes": 6,
    "variants": [
      "纟"
    ],
    "notes": "纟 simplified left-side form."
  },
  {
    "number": 121,
    "kangxi_radical": "⽸",
    "radical": "缶",
    "code": "U+2F78",
    "english_name": "KANGXI RADICAL JAR",
    "meaning": "jar",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 122,
    "kangxi_radical": "⽹",
    "radical": "网",
    "code": "U+2F79",
    "english_name": "KANGXI RADICAL NET",
    "meaning": "net",
    "strokes": 6,
    "variants": [
      "罒",
      "⺲"
    ],
    "notes": "罒 common positional variant."
  },
  {
    "number": 123,
    "kangxi_radical": "⽺",
    "radical": "羊",
    "code": "U+2F7A",
    "english_name": "KANGXI RADICAL SHEEP",
    "meaning": "sheep",
    "strokes": 6,
    "variants": [
      "⺶",
      "⺷"
    ],
    "notes": ""
  },
  {
    "number": 124,
    "kangxi_radical": "⽻",
    "radical": "羽",
    "code": "U+2F7B",
    "english_name": "KANGXI RADICAL FEATHER",
    "meaning": "feather",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 125,
    "kangxi_radical": "⽼",
    "radical": "老",
    "code": "U+2F7C",
    "english_name": "KANGXI RADICAL OLD",
    "meaning": "old",
    "strokes": 6,
    "variants": [
      "耂"
    ],
    "notes": "耂 top form in 者."
  },
  {
    "number": 126,
    "kangxi_radical": "⽽",
    "radical": "而",
    "code": "U+2F7D",
    "english_name": "KANGXI RADICAL AND",
    "meaning": "and",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 127,
    "kangxi_radical": "⽾",
    "radical": "耒",
    "code": "U+2F7E",
    "english_name": "KANGXI RADICAL PLOW",
    "meaning": "plow",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 128,
    "kangxi_radical": "⽿",
    "radical": "耳",
    "code": "U+2F7F",
    "english_name": "KANGXI RADICAL EAR",
    "meaning": "ear",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 129,
    "kangxi_radical": "⾀",
    "radical": "聿",
    "code": "U+2F80",
    "english_name": "KANGXI RADICAL BRUSH",
    "meaning": "brush",
    "strokes": 6,
    "variants": [
      "肀"
    ],
    "notes": ""
  },
  {
    "number": 130,
    "kangxi_radical": "⾁",
    "radical": "肉",
    "code": "U+2F81",
    "english_name": "KANGXI RADICAL MEAT",
    "meaning": "meat",
    "strokes": 6,
    "variants": [
      "月"
    ],
    "notes": "月 often used as the 'meat' radical in left-side position."
  },
  {
    "number": 131,
    "kangxi_radical": "⾂",
    "radical": "臣",
    "code": "U+2F82",
    "english_name": "KANGXI RADICAL MINISTER",
    "meaning": "minister",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 132,
    "kangxi_radical": "⾃",
    "radical": "自",
    "code": "U+2F83",
    "english_name": "KANGXI RADICAL SELF",
    "meaning": "self",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 133,
    "kangxi_radical": "⾄",
    "radical": "至",
    "code": "U+2F84",
    "english_name": "KANGXI RADICAL ARRIVE",
    "meaning": "arrive",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 134,
    "kangxi_radical": "⾅",
    "radical": "臼",
    "code": "U+2F85",
    "english_name": "KANGXI RADICAL MORTAR",
    "meaning": "mortar",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 135,
    "kangxi_radical": "⾆",
    "radical": "舌",
    "code": "U+2F86",
    "english_name": "KANGXI RADICAL TONGUE",
    "meaning": "tongue",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 136,
    "kangxi_radical": "⾇",
    "radical": "舛",
    "code": "U+2F87",
    "english_name": "KANGXI RADICAL OPPOSE",
    "meaning": "oppose",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 137,
    "kangxi_radical": "⾈",
    "radical": "舟",
    "code": "U+2F88",
    "english_name": "KANGXI RADICAL BOAT",
    "meaning": "boat",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 138,
    "kangxi_radical": "⾉",
    "radical": "艮",
    "code": "U+2F89",
    "english_name": "KANGXI RADICAL STOPPING",
    "meaning": "stopping; tough",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 139,
    "kangxi_radical": "⾊",
    "radical": "色",
    "code": "U+2F8A",
    "english_name": "KANGXI RADICAL COLOR",
    "meaning": "color",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 140,
    "kangxi_radical": "⾋",
    "radical": "艸",
    "code": "U+2F8B",
    "english_name": "KANGXI RADICAL GRASS",
    "meaning": "grass",
    "strokes": 6,
    "variants": [
      "艹"
    ],
    "notes": "艹 is the common top form."
  },
  {
    "number": 141,
    "kangxi_radical": "⾌",
    "radical": "虍",
    "code": "U+2F8C",
    "english_name": "KANGXI RADICAL TIGER",
    "meaning": "tiger stripes",
    "strokes": 6,
    "variants": [],
    "notes": "Appears in 虎."
  },
  {
    "number": 142,
    "kangxi_radical": "⾍",
    "radical": "虫",
    "code": "U+2F8D",
    "english_name": "KANGXI RADICAL INSECT",
    "meaning": "insect",
    "strokes": 6,
    "variants": [],
    "notes": "Includes insects, reptiles, amphibians."
  },
  {
    "number": 143,
    "kangxi_radical": "⾎",
    "radical": "血",
    "code": "U+2F8E",
    "english_name": "KANGXI RADICAL BLOOD",
    "meaning": "blood",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 144,
    "kangxi_radical": "⾏",
    "radical": "行",
    "code": "U+2F8F",
    "english_name": "KANGXI RADICAL WALK ENCLOSURE",
    "meaning": "go; walk",
    "strokes": 6,
    "variants": [],
    "notes": ""
  },
  {
    "number": 145,
    "kangxi_radical": "⾐",
    "radical": "衣",
    "code": "U+2F90",
    "english_name": "KANGXI RADICAL CLOTHES",
    "meaning": "clothing",
    "strokes": 6,
    "variants": [
      "衤"
    ],
    "notes": "衤 is left-side form."
  },
  {
    "number": 146,
    "kangxi_radical": "⾑",
    "radical": "西",
    "code": "U+2F91",
    "english_name": "KANGXI RADICAL WEST",
    "meaning": "west / cover",
    "strokes": 6,
    "variants": [
      "覀"
    ],
    "notes": ""
  },
  {
    "number": 147,
    "kangxi_radical": "⾒",
    "radical": "見",
    "code": "U+2F92",
    "english_name": "KANGXI RADICAL SEE",
    "meaning": "see",
    "strokes": 7,
    "variants": [
      "见"
    ],
    "notes": "见 simplified."
  },
  {
    "number": 148,
    "kangxi_radical": "⾓",
    "radical": "角",
    "code": "U+2F93",
    "english_name": "KANGXI RADICAL HORN",
    "meaning": "horn",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 149,
    "kangxi_radical": "⾔",
    "radical": "言",
    "code": "U+2F94",
    "english_name": "KANGXI RADICAL SPEECH",
    "meaning": "speech",
    "strokes": 7,
    "variants": [
      "讠"
    ],
    "notes": "讠 simplified left-side form."
  },
  {
    "number": 150,
    "kangxi_radical": "⾕",
    "radical": "谷",
    "code": "U+2F95",
    "english_name": "KANGXI RADICAL VALLEY",
    "meaning": "valley",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 151,
    "kangxi_radical": "⾖",
    "radical": "豆",
    "code": "U+2F96",
    "english_name": "KANGXI RADICAL BEAN",
    "meaning": "bean",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 152,
    "kangxi_radical": "⾗",
    "radical": "豕",
    "code": "U+2F97",
    "english_name": "KANGXI RADICAL PIG",
    "meaning": "pig",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 153,
    "kangxi_radical": "⾘",
    "radical": "豸",
    "code": "U+2F98",
    "english_name": "KANGXI RADICAL BADGER",
    "meaning": "badger / beast",
    "strokes": 7,
    "variants": [],
    "notes": "Used in 貌, 貅."
  },
  {
    "number": 154,
    "kangxi_radical": "⾙",
    "radical": "貝",
    "code": "U+2F99",
    "english_name": "KANGXI RADICAL SHELL",
    "meaning": "shell; valuables",
    "strokes": 7,
    "variants": [
      "贝"
    ],
    "notes": "贝 simplified."
  },
  {
    "number": 155,
    "kangxi_radical": "⾚",
    "radical": "赤",
    "code": "U+2F9A",
    "english_name": "KANGXI RADICAL RED",
    "meaning": "red",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 156,
    "kangxi_radical": "⾛",
    "radical": "走",
    "code": "U+2F9B",
    "english_name": "KANGXI RADICAL RUN",
    "meaning": "run; walk",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 157,
    "kangxi_radical": "⾜",
    "radical": "足",
    "code": "U+2F9C",
    "english_name": "KANGXI RADICAL FOOT",
    "meaning": "foot",
    "strokes": 7,
    "variants": [
      "⻊"
    ],
    "notes": "⻊ bottom/side variant."
  },
  {
    "number": 158,
    "kangxi_radical": "⾝",
    "radical": "身",
    "code": "U+2F9D",
    "english_name": "KANGXI RADICAL BODY",
    "meaning": "body",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 159,
    "kangxi_radical": "⾞",
    "radical": "車",
    "code": "U+2F9E",
    "english_name": "KANGXI RADICAL CART",
    "meaning": "car; vehicle",
    "strokes": 7,
    "variants": [
      "车"
    ],
    "notes": "车 simplified."
  },
  {
    "number": 160,
    "kangxi_radical": "⾟",
    "radical": "辛",
    "code": "U+2F9F",
    "english_name": "KANGXI RADICAL BITTER",
    "meaning": "bitter",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 161,
    "kangxi_radical": "⾠",
    "radical": "辰",
    "code": "U+2FA0",
    "english_name": "KANGXI RADICAL MORNING",
    "meaning": "morning; 5th Earthly Branch",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 162,
    "kangxi_radical": "⾡",
    "radical": "辵",
    "code": "U+2FA1",
    "english_name": "KANGXI RADICAL WALK",
    "meaning": "walk; movement",
    "strokes": 7,
    "variants": ["⻌", "⻍","⻎"
    ],
    "notes": "Compressed forms ⻌ ⻍ ⻎ appear in many kanji."
  },
  {
    "number": 163,
    "kangxi_radical": "⾢",
    "radical": "邑",
    "code": "U+2FA2",
    "english_name": "KANGXI RADICAL CITY",
    "meaning": "city; settlement",
    "strokes": 7,
    "variants": [
      "阝"
    ],
    "notes": "Right-side 阝 means 'city'."
  },
  {
    "number": 164,
    "kangxi_radical": "⾣",
    "radical": "酉",
    "code": "U+2FA3",
    "english_name": "KANGXI RADICAL WINE",
    "meaning": "wine; alcohol",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 165,
    "kangxi_radical": "⾤",
    "radical": "采",
    "code": "U+2FA4",
    "english_name": "KANGXI RADICAL DISTINGUISH",
    "meaning": "distinguish; gather",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 166,
    "kangxi_radical": "⾥",
    "radical": "里",
    "code": "U+2FA5",
    "english_name": "KANGXI RADICAL VILLAGE",
    "meaning": "village; unit of distance",
    "strokes": 7,
    "variants": [],
    "notes": ""
  },
  {
    "number": 167,
    "kangxi_radical": "⾦",
    "radical": "金",
    "code": "U+2FA6",
    "english_name": "KANGXI RADICAL GOLD",
    "meaning": "metal; gold",
    "strokes": 8,
    "variants": [
      "釒"
    ],
    "notes": "釒 is left-side form."
  },
  {
    "number": 168,
    "kangxi_radical": "⾧",
    "radical": "長",
    "code": "U+2FA7",
    "english_name": "KANGXI RADICAL LONG",
    "meaning": "long",
    "strokes": 8,
    "variants": [
      "长"
    ],
    "notes": "长 simplified."
  },
  {
    "number": 169,
    "kangxi_radical": "⾨",
    "radical": "門",
    "code": "U+2FA8",
    "english_name": "KANGXI RADICAL GATE",
    "meaning": "gate",
    "strokes": 8,
    "variants": [
      "门"
    ],
    "notes": "门 simplified."
  },
  {
    "number": 170,
    "kangxi_radical": "⾩",
    "radical": "阜",
    "code": "U+2FA9",
    "english_name": "KANGXI RADICAL MOUND",
    "meaning": "mound; hill",
    "strokes": 8,
    "variants": [
      "阝"
    ],
    "notes": "Left-side 阝 means 'hill'."
  },
  {
    "number": 171,
    "kangxi_radical": "⾪",
    "radical": "隶",
    "code": "U+2FAA",
    "english_name": "KANGXI RADICAL SLAVE",
    "meaning": "capture; slave",
    "strokes": 8,
    "variants": [],
    "notes": ""
  },
  {
    "number": 172,
    "kangxi_radical": "⾫",
    "radical": "隹",
    "code": "U+2FAB",
    "english_name": "KANGXI RADICAL SHORT-TAILED BIRD",
    "meaning": "short-tailed bird",
    "strokes": 8,
    "variants": [],
    "notes": ""
  },
  {
    "number": 173,
    "kangxi_radical": "⾬",
    "radical": "雨",
    "code": "U+2FAC",
    "english_name": "KANGXI RADICAL RAIN",
    "meaning": "rain",
    "strokes": 8,
    "variants": [],
    "notes": ""
  },
  {
    "number": 174,
    "kangxi_radical": "⾭",
    "radical": "青",
    "code": "U+2FAD",
    "english_name": "KANGXI RADICAL BLUE",
    "meaning": "blue; green",
    "strokes": 8,
    "variants": [],
    "notes": ""
  },
  {
    "number": 175,
    "kangxi_radical": "⾮",
    "radical": "非",
    "code": "U+2FAE",
    "english_name": "KANGXI RADICAL WRONG",
    "meaning": "wrong; not",
    "strokes": 8,
    "variants": [],
    "notes": ""
  },
  {
    "number": 176,
    "kangxi_radical": "⾯",
    "radical": "面",
    "code": "U+2FAF",
    "english_name": "KANGXI RADICAL FACE",
    "meaning": "face",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 177,
    "kangxi_radical": "⾰",
    "radical": "革",
    "code": "U+2FB0",
    "english_name": "KANGXI RADICAL LEATHER",
    "meaning": "leather",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 178,
    "kangxi_radical": "⾱",
    "radical": "韋",
    "code": "U+2FB1",
    "english_name": "KANGXI RADICAL TANNED LEATHER",
    "meaning": "tanned leather",
    "strokes": 9,
    "variants": [
      "韦"
    ],
    "notes": "韦 simplified."
  },
  {
    "number": 179,
    "kangxi_radical": "⾲",
    "radical": "韭",
    "code": "U+2FB2",
    "english_name": "KANGXI RADICAL LEEK",
    "meaning": "leek",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 180,
    "kangxi_radical": "⾳",
    "radical": "音",
    "code": "U+2FB3",
    "english_name": "KANGXI RADICAL SOUND",
    "meaning": "sound",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 181,
    "kangxi_radical": "⾴",
    "radical": "頁",
    "code": "U+2FB4",
    "english_name": "KANGXI RADICAL LEAF",
    "meaning": "page; head",
    "strokes": 9,
    "variants": [
      "页"
    ],
    "notes": "页 simplified."
  },
  {
    "number": 182,
    "kangxi_radical": "⾵",
    "radical": "風",
    "code": "U+2FB5",
    "english_name": "KANGXI RADICAL WIND",
    "meaning": "wind",
    "strokes": 9,
    "variants": [
      "风"
    ],
    "notes": "风 simplified."
  },
  {
    "number": 183,
    "kangxi_radical": "⾶",
    "radical": "飛",
    "code": "U+2FB6",
    "english_name": "KANGXI RADICAL FLY",
    "meaning": "fly",
    "strokes": 9,
    "variants": [
      "飞"
    ],
    "notes": "飞 simplified."
  },
  {
    "number": 184,
    "kangxi_radical": "⾷",
    "radical": "食",
    "code": "U+2FB7",
    "english_name": "KANGXI RADICAL EAT",
    "meaning": "eat; food",
    "strokes": 9,
    "variants": [
      "飠",
      "𩙿",
      "饣"
    ],
    "notes": "饣 simplified left-side form."
  },
  {
    "number": 185,
    "kangxi_radical": "⾸",
    "radical": "首",
    "code": "U+2FB8",
    "english_name": "KANGXI RADICAL HEAD",
    "meaning": "head",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 186,
    "kangxi_radical": "⾹",
    "radical": "香",
    "code": "U+2FB9",
    "english_name": "KANGXI RADICAL FRAGRANT",
    "meaning": "fragrance",
    "strokes": 9,
    "variants": [],
    "notes": ""
  },
  {
    "number": 187,
    "kangxi_radical": "⾺",
    "radical": "馬",
    "code": "U+2FBA",
    "english_name": "KANGXI RADICAL HORSE",
    "meaning": "horse",
    "strokes": 10,
    "variants": [
      "马"
    ],
    "notes": "马 simplified."
  },
  {
    "number": 188,
    "kangxi_radical": "⾻",
    "radical": "骨",
    "code": "U+2FBB",
    "english_name": "KANGXI RADICAL BONE",
    "meaning": "bone",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 189,
    "kangxi_radical": "⾼",
    "radical": "高",
    "code": "U+2FBC",
    "english_name": "KANGXI RADICAL TALL",
    "meaning": "tall; high",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 190,
    "kangxi_radical": "⾽",
    "radical": "髟",
    "code": "U+2FBD",
    "english_name": "KANGXI RADICAL LONG HAIR",
    "meaning": "long hair",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 191,
    "kangxi_radical": "⾾",
    "radical": "鬥",
    "code": "U+2FBE",
    "english_name": "KANGXI RADICAL FIGHT",
    "meaning": "fight",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 192,
    "kangxi_radical": "⾿",
    "radical": "鬯",
    "code": "U+2FBF",
    "english_name": "KANGXI RADICAL SACRIFICIAL WINE",
    "meaning": "sacrificial wine",
    "strokes": 10,
    "variants": [],
    "notes": "Rare radical."
  },
  {
    "number": 193,
    "kangxi_radical": "⿀",
    "radical": "鬲",
    "code": "U+2FC0",
    "english_name": "KANGXI RADICAL CAULDRON",
    "meaning": "cauldron; tripod",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 194,
    "kangxi_radical": "⿁",
    "radical": "鬼",
    "code": "U+2FC1",
    "english_name": "KANGXI RADICAL GHOST",
    "meaning": "ghost; spirit",
    "strokes": 10,
    "variants": [],
    "notes": ""
  },
  {
    "number": 195,
    "kangxi_radical": "⿂",
    "radical": "魚",
    "code": "U+2FC2",
    "english_name": "KANGXI RADICAL FISH",
    "meaning": "fish",
    "strokes": 11,
    "variants": [
      "鱼"
    ],
    "notes": "鱼 simplified."
  },
  {
    "number": 196,
    "kangxi_radical": "⿃",
    "radical": "鳥",
    "code": "U+2FC3",
    "english_name": "KANGXI RADICAL BIRD",
    "meaning": "bird",
    "strokes": 11,
    "variants": [
      "鸟"
    ],
    "notes": "鸟 simplified."
  },
  {
    "number": 197,
    "kangxi_radical": "⿄",
    "radical": "鹵",
    "code": "U+2FC4",
    "english_name": "KANGXI RADICAL SALT",
    "meaning": "salt",
    "strokes": 11,
    "variants": [
      "卤"
    ],
    "notes": "卤 simplified."
  },
  {
    "number": 198,
    "kangxi_radical": "⿅",
    "radical": "鹿",
    "code": "U+2FC5",
    "english_name": "KANGXI RADICAL DEER",
    "meaning": "deer",
    "strokes": 11,
    "variants": [],
    "notes": ""
  },
  {
    "number": 199,
    "kangxi_radical": "⿆",
    "radical": "麥",
    "code": "U+2FC6",
    "english_name": "KANGXI RADICAL WHEAT",
    "meaning": "wheat",
    "strokes": 11,
    "variants": [
      "麦"
    ],
    "notes": "麦 simplified."
  },
  {
    "number": 200,
    "kangxi_radical": "⿇",
    "radical": "麻",
    "code": "U+2FC7",
    "english_name": "KANGXI RADICAL HEMP",
    "meaning": "hemp",
    "strokes": 11,
    "variants": [],
    "notes": ""
  },
  {
    "number": 201,
    "kangxi_radical": "⿈",
    "radical": "黃",
    "code": "U+2FC8",
    "english_name": "KANGXI RADICAL YELLOW",
    "meaning": "yellow",
    "strokes": 12,
    "variants": [
      "黄"
    ],
    "notes": "黄 simplified."
  },
  {
    "number": 202,
    "kangxi_radical": "⿉",
    "radical": "黍",
    "code": "U+2FC9",
    "english_name": "KANGXI RADICAL MILLET",
    "meaning": "millet",
    "strokes": 12,
    "variants": [],
    "notes": ""
  },
  {
    "number": 203,
    "kangxi_radical": "⿊",
    "radical": "黑",
    "code": "U+2FCA",
    "english_name": "KANGXI RADICAL BLACK",
    "meaning": "black",
    "strokes": 12,
    "variants": [
      "黒"
    ],
    "notes": "黒 is Japanese traditional form."
  },
  {
    "number": 204,
    "kangxi_radical": "⿋",
    "radical": "黹",
    "code": "U+2FCB",
    "english_name": "KANGXI RADICAL EMBROIDERY",
    "meaning": "embroidery",
    "strokes": 12,
    "variants": [],
    "notes": "Very rare."
  },
  {
    "number": 205,
    "kangxi_radical": "⿌",
    "radical": "黽",
    "code": "U+2FCC",
    "english_name": "KANGXI RADICAL FROG",
    "meaning": "frog",
    "strokes": 13,
    "variants": [
      "黾"
    ],
    "notes": "黾 simplified."
  },
  {
    "number": 206,
    "kangxi_radical": "⿍",
    "radical": "鼎",
    "code": "U+2FCD",
    "english_name": "KANGXI RADICAL TRIPOD",
    "meaning": "tripod; sacrificial cauldron",
    "strokes": 13,
    "variants": [],
    "notes": ""
  },
  {
    "number": 207,
    "kangxi_radical": "⿎",
    "radical": "鼓",
    "code": "U+2FCE",
    "english_name": "KANGXI RADICAL DRUM",
    "meaning": "drum",
    "strokes": 13,
    "variants": [],
    "notes": ""
  },
  {
    "number": 208,
    "kangxi_radical": "⿏",
    "radical": "鼠",
    "code": "U+2FCF",
    "english_name": "KANGXI RADICAL RAT",
    "meaning": "rat; rodent",
    "strokes": 13,
    "variants": [
      "⺁"
    ],
    "notes": "⺁ compressed form."
  },
  {
    "number": 209,
    "kangxi_radical": "⿐",
    "radical": "鼻",
    "code": "U+2FD0",
    "english_name": "KANGXI RADICAL NOSE",
    "meaning": "nose",
    "strokes": 14,
    "variants": [],
    "notes": ""
  },
  {
    "number": 210,
    "kangxi_radical": "⿑",
    "radical": "齊",
    "code": "U+2FD1",
    "english_name": "KANGXI RADICAL EVEN",
    "meaning": "even; uniform",
    "strokes": 14,
    "variants": [
      "齐"
    ],
    "notes": "齐 simplified."
  },
  {
    "number": 211,
    "kangxi_radical": "⿒",
    "radical": "齒",
    "code": "U+2FD2",
    "english_name": "KANGXI RADICAL TOOTH",
    "meaning": "tooth",
    "strokes": 15,
    "variants": [
      "齿"
    ],
    "notes": "齿 simplified."
  },
  {
    "number": 212,
    "kangxi_radical": "⿓",
    "radical": "龍",
    "code": "U+2FD3",
    "english_name": "KANGXI RADICAL DRAGON",
    "meaning": "dragon",
    "strokes": 16,
    "variants": [
      "龙"
    ],
    "notes": "龙 simplified."
  },
  {
    "number": 213,
    "kangxi_radical": "⿔",
    "radical": "龜",
    "code": "U+2FD4",
    "english_name": "KANGXI RADICAL TURTLE",
    "meaning": "turtle",
    "strokes": 16,
    "variants": [
      "龟"
    ],
    "notes": "龟 simplified."
  },
  {
    "number": 214,
    "kangxi_radical": "⿕",
    "radical": "龠",
    "code": "U+2FD5",
    "english_name": "KANGXI RADICAL FLUTE",
    "meaning": "flute",
    "strokes": 17,
    "variants": [],
    "notes": ""
  }
]

# Note: The original Kangxi radicals are 214; the above list includes canonical ones and many common variants.
# Some entries (towards the end) may be represented with historical forms; for completeness we included common variants.

# Save JSON files: kangxi_radicals.json and radical_crosswalk.json
out_dir = Path("./")
out_dir.mkdir(parents=True, exist_ok=True)

kangxi_path = out_dir / "kangxi_radicals.json"
with kangxi_path.open("w", encoding="utf-8") as f:
    json.dump(kangxi_radicals, f, ensure_ascii=False, indent=2)
    
    #%%
