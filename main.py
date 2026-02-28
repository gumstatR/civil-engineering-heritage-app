import streamlit as st
import numpy as  np
import pandas as pd
#from PIL import Image
import pydeck as pdk

st.title("土木遺産Webアプリ")
st.markdown("このWebアプリは作成中です〜2001年まで。")
df=pd.read_csv("dobokuisan.csv",encoding="utf-8")   #読み込み

# 表示したい順番でリストを作る
col = ["対象構造物", "所在地", "竣工年", "受賞理由","北緯","東経","施設1","施設2","施設3","施設4","施設5"]
df=df[col]

# サイドバーで表示する列を選択させる
st.sidebar.header("表示設定")
all_columns = df.columns.tolist()
    
selected_columns = st.sidebar.multiselect(
    "表示したい項目を選択してください",
     all_columns,
        default=all_columns[:3]  # 最初は左から◯番目の列だけ表示しておく設定
    )

    # 選択された列に基づいてデータを表示
def new_func():
    st.subheader("土木遺産一覧")

if selected_columns:
    new_func()
    # 選択された列だけを抽出して表示
    st.dataframe(df[selected_columns], hide_index=True, use_container_width=True,)
    # その順番でデータを抽出して表示
       
else:
        st.error("表示する項目を左のサイドバーから選んでください。")




map_df = df.rename(columns={'北緯': 'lat', '東経': 'lon'}) 
map_df = map_df.dropna(subset=['lat', 'lon']) #座標のない行を削除 
#map_df

st.subheader("土木遺産マップ")
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=map_df["lat"].mean(),
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
        "html": "<b>遺産名:</b> {対象構造物}<br/><b>所在地:</b> {所在地}",
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
