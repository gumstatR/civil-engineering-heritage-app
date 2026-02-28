import streamlit as st
import numpy as  np
import pandas as pd
#from PIL import Image
import pydeck as pdk

st.title("土木遺産Webアプリ")
st.markdown("このWebアプリは作成中です。")
df=pd.read_csv("dobokuisan.csv",encoding="utf-8")   #読み込み

# 表示したい順番でリストを作る
col = ["対象構造物", "都道府県","市町村",  "竣工年", "受賞理由","北緯","東経","施設1","施設2","施設3","施設4","施設5"]
df=df[col]

st.subheader("🔍土木遺産検索")
# 1行を2つのカラムに分ける（都道府県とキーワード）
col1, col2 = st.columns(2)
with col1:
    # 1. 地方と都道府県のグループ分け（辞書）
    region_map = {
        "北海道・東北": ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
        "関東": ["茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県"],
        "中部": ["新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県"],
        "近畿": ["三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県"],
        "中国・四国": ["鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県"],
        "九州・沖縄": ["福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]
    }

    # 2. まず「地方」を選んでもらう
    selected_region = st.selectbox("① 地方を選択", ["すべて"] + list(region_map.keys()))

    # 3. 地方に応じて「都道府県」の選択肢を切り替える
    if selected_region != "すべて":
        # 選んだ地方に属する県だけをリストにする
        prefs_in_region = region_map[selected_region]
        target_pref = st.selectbox("② 都道府県を選択", ["すべて"] + prefs_in_region)
    else:
        # 「すべて」の場合は全件から選べるようにする（以前と同じ）
        all_prefs = sorted([p for p in df["都道府県"].unique() if isinstance(p, str)])
        target_pref = st.selectbox("② 都道府県を選択", ["すべて"] + all_prefs)






with col2:
    search_query = st.text_input("キーワードを入力（名称や受賞理由など）", "")

# --- 検索処理 ---
search_df = df.copy()

if target_pref != "すべて":
    search_df = search_df[search_df["都道府県"] == target_pref]

if search_query:
    search_df = search_df[
        search_df["対象構造物"].str.contains(search_query, case=False, na=False) |
        search_df["受賞理由"].str.contains(search_query, case=False, na=False)
    ]

st.write(f"検索結果: {len(search_df)} 件")

display_cols = ["対象構造物", "都道府県", "市町村", "竣工年", "受賞理由"] 

if not search_df.empty:
    # 検索で見つかったデータだけを表示
    st.dataframe(search_df[display_cols], hide_index=True, use_container_width=True)
else:
    st.info("該当する土木遺産が見つかりませんでした。")




map_df = search_df.rename(columns={'北緯': 'lat', '東経': 'lon'})
map_df = map_df.dropna(subset=['lat', 'lon']) #座標のない行を削除 

if not map_df.empty:
    st.subheader("土木遺産マップ")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=map_df["lat"].mean(), # データがある時だけ平均を計算
            longitude=map_df["lon"].mean(),
            zoom=5,
            pitch=0,
        ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_color="[200, 30, 0, 160]", # ドットの色（赤）
            get_radius=100,            # 地図上のサイズ
            radius_min_pixels=5,       # 引きで見ても◯ピクセル以下にならない
            radius_max_pixels=10,      # 寄りで見ても◯ピクセル以上にならない
            pickable=True,
        ),
    ],
    tooltip={
        "html": "<b>遺産名:</b> {対象構造物}<br/><b>所在地:</b> {都道府県}",
        "style": {"color": "white"}
    }
))




# text=st.text_input("あなたの趣味を教えてください")
# "あなたの趣味は",text


# condition=st.slider("あなたの今の調子は？",0,100,50)
# "あなたのコンディションは：",condition
# if condition>80:
#     st.write("VERY GOOD!")

# else:"頑張って！"
                 


# st.write("Display Image")

# if st.checkbox("写真を見る"):
#     img= Image.open("###.jpg")
#     st.image(img,caption="◯◯の写真です")

# option=st.selectbox(
#     "あなたが好きな数字を教えてください",
#     list(range(1,11))
# )
# "あなたの好きな数字は",option,"です。"

# #おまけ
# #streamlit run main.pyでローカルで確認できる。
# #初期設定①git init, ②git remote add ofigin https:/// 
# #　①git add . ②git commit -m"◯◯◯".　③git push origin main
