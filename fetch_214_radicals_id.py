import pandas as pd

#fetch Kanji Kangxi dictionary id_number (colonnne "No.")
df_radicals = pd.read_html('https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_stroke_count')[0]

#in this df_radicals, Meaning & Reading are concatenated into the same column "Meaning and reading"
#fetch other Kanji list, which lacks of need "No." column, but has tidy differentiated "meaning" & "reading" columns
# -> dfs to be merged
df_meaning_tidy = pd.read_html('https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_frequency')[2]

df_kanji = pd.DataFrame.from_dict(kanji_dict, orient='index')

df_kanji['radicals'] = df_kanji['radicals'].astype(int)

#merge kanji dictionary with radicals
df_merged = pd.merge(df_kanji.reset_index(), df_radicals, how='left', left_on='radicals', right_on='No.')

#dict of 214 radicals
dict_radical = df_merged[['Radical (variants)', 'index']].to_dict(orient='records')
