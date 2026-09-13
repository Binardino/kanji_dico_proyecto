// Mock fixture matching the target shape of GET /kanji/{literal} (see src/kanjidb/api/data.py, WIP).
// Real data pulled from data/raw/Unihan_CJKVI_database.txt + data/processed/kangxi_radicals.json
// + KANJIDIC2, so this mirrors exactly what the real backend will return once ready.
// Swap MOCK_KANJI lookups in app.js::fetchKanjiData() for a real fetch() once the API exists.

export const MOCK_KANJI = {
  "人": {
    literal: "人",
    readings: { on: ["ジン", "ニン"], kun: ["ひと", "-り", "-と"] },
    meanings: [
      { lang: "en", text: "person" },
      { lang: "fr", text: "être humain" },
    ],
    jlpt: "4",
    grade: "1",
    stroke_count: "2",
    decomposition: {
      char: "人", position: null, is_leaf: true, is_radical: true,
      radical_name: "man", radical_meaning: "person",
      children: [],
    },
  },

  "明": {
    literal: "明",
    readings: { on: ["メイ", "ミョウ", "ミン"], kun: ["あ.かり", "あか.るい", "あ.ける"] },
    meanings: [
      { lang: "en", text: "bright" },
      { lang: "en", text: "light" },
    ],
    jlpt: "3",
    grade: "2",
    stroke_count: "8",
    decomposition: {
      char: "明", position: null, is_leaf: false, is_radical: false,
      radical_name: null, radical_meaning: null,
      children: [
        {
          char: "日", position: "left", is_leaf: true, is_radical: true,
          radical_name: "sun", radical_meaning: "sun; day", children: [],
        },
        {
          char: "月", position: "right", is_leaf: true, is_radical: true,
          radical_name: "moon", radical_meaning: "moon; flesh", children: [],
        },
      ],
    },
  },

  "海": {
    literal: "海",
    readings: { on: ["カイ"], kun: ["うみ"] },
    meanings: [
      { lang: "en", text: "sea" },
      { lang: "en", text: "ocean" },
    ],
    jlpt: "3",
    grade: "2",
    stroke_count: "9",
    decomposition: {
      char: "海", position: null, is_leaf: false, is_radical: false,
      radical_name: null, radical_meaning: null,
      children: [
        {
          char: "氵", position: "left", is_leaf: true, is_radical: true,
          radical_name: "water", radical_meaning: "water", children: [],
        },
        {
          char: "毎", position: "right", is_leaf: false, is_radical: false,
          radical_name: null, radical_meaning: null,
          children: [
            {
              char: "𠂉", position: "top", is_leaf: true, is_radical: false,
              radical_name: null, radical_meaning: null, children: [],
            },
            {
              char: "毋", position: "bottom", is_leaf: true, is_radical: true,
              radical_name: "do not", radical_meaning: "do not", children: [],
            },
          ],
        },
      ],
    },
  },
};
