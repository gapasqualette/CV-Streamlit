from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import requests
import streamlit as st
import pandas as pd
import numpy as np

def update_trend():
    st.session_state.opn = st.session_state.opn_select
    st.session_state.trend = 'All'
    st.rerun()

def update_year():
    st.session_state.year = st.session_state.year_select
    st.session_state.opn = 'All'
    st.rerun()

def update_opn():
    st.session_state.opn = st.session_state.opn_select
    st.rerun()

def opinions_movies(rate: str):
    try:
        rate = float(rate)
        if rate == 0:
            return 'Not Released'
        elif rate <= 5.0:
            return 'Bad'
        elif rate <= 6.5:
            return 'Mediocre'
        elif rate <= 8.0:
            return 'Good'
        else:
            return 'Excellent'
    except:
        return 'Not Released'

def trending_movies(rate:int):
    if rate > 0:
        return 'Trending'
    elif rate < 0: 
        return 'Not Trending'
    else:
        return 'Same Trend'

def icon_movie(rate:str):
    match rate:
        case 'Not Released':
            return '⏲'
        case 'Bad':
            return '😞'
        case 'Mediocre':
            return '😶'
        case 'Good':
            return '🙃'
        case 'Excellent':
            return '🤩'
        
#st.set_page_config('IMDB Top Trending Movies - WebScraping and Pandas (Only 25 movies)', layout='wide')

st.markdown(
        """
        <style>
        .vl {
            border-left: 3px solid white;
            height: 300px; /* Altura da linha */
            position: absolute;
            left: 50%; /* Alinhamento horizontal */
            margin-left: -1px; /* Centralização */
            top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
)

url = 'https://www.imdb.com/pt/chart/moviemeter/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/90.0.4480.54"
}
page = requests.get(url, headers=headers)

soup = bs(page.content, 'html.parser')

rows = soup.select('ul.ipc-metadata-list li.ipc-metadata-list-summary-item')

dict_movies = []
position: int = 1
for row in rows:
    rating = row.select_one('span.ipc-rating-star--rating')
    #st.code(rating, language='html')
    rate = rating.text.strip() if rating else 0
    
    if rate != 0:
        rate = rate.replace(',','.')
        rate = float(rate)


    titulo_tag = row.select_one('h3.ipc-title__text')

    titulo = titulo_tag.text.strip() if titulo_tag else 'N/A'
    #st.code(titulo_tag)

    year_tag = row.select_one('div.cli-title-metadata > span.cli-title-metadata-item:nth-of-type(1)')
    year = year_tag.text.strip() if year_tag else 'N/A'
    #st.write(year)

    length_tag = row.select_one('div.cli-title-metadata > span.cli-title-metadata-item:nth-of-type(2)')
    length = length_tag.text.strip() if length_tag else 'N/A'

    if length != 'N/A':
        length = length[0:len(length) -1] 
        length_split = length.split('h ')

        hours = int(length_split[0])
        minutes = int(length_split[1])
        length = hours*60 + minutes

    age_tag = row.select_one('div.cli-title-metadata > span.cli-title-metadata-item:nth-of-type(3)')
    age = age_tag.text.strip() if age_tag else 'N/A'

    vote_count_tag = row.select_one('span.ipc-rating-star--voteCount')
    
    if vote_count_tag: 
        vote_count = vote_count_tag.text.strip()
        vote_count = vote_count[1:len(vote_count) - 1].replace(',', '.')
        try:
            vote_split = vote_count.split() 
            if len(vote_split) == 2:
                num = vote_split[0]
                unity = vote_split[1]
                if unity == 'mil':
                    vote_count = int(float(num) * 1_000)
                elif unity == 'mi':
                    vote_count = int(float(num) * 1_000_000)
                else:
                    vote_count = int(float(num))
            else:
                vote_count = int(float(vote_split[0]))
        except:
            vote_count = int(float(vote_count))
    else:
        vote_count = 0

    ranking_tag = row.select_one('span[aria-label]')
    if ranking_tag:
        ranking = ranking_tag.get('aria-label').strip()
        ranking_split = ranking.lower().split()
        if 'subiu' in ranking_split:
            ranking = int(ranking_split[1])
        elif 'desceu' in ranking_split:
            ranking = -1 * int(ranking_split[1])
        else:
            ranking = 0   

    movie_poster_tag = row.select_one('img')
    movie_poster = movie_poster_tag['src'] if movie_poster_tag else None

    dict_movies.append({
        'Position': position,
        'Title': titulo,
        'Rate': rate,
        'Year': year,
        'Length': length,
        'Age': age,
        'VoteCount': vote_count,
        'Trend': ranking,
        'Poster': movie_poster
        })
    
    position += 1

df = pd.DataFrame(dict_movies)
df['Opinion'] = df['Rate'].apply(opinions_movies)
df['Trend_Analysis'] = df['Trend'].apply(trending_movies)

st.header(f'IMDB Top Trending Movies - WebScraping and Pandas (Only Top 25 movies) - {dt.now().strftime('%d/%m/%Y')}', divider=True)

colsMain = st.columns(3)
df_validos = df[df['Rate'] != 0]
df_validos['Rate'] = df_validos['Rate'].astype(float)


with colsMain[0]:
    with st.expander('Best Rated Movie', icon=':material/star:'):
        t1_col = st.columns([35,5,60])

        # Highest Rating
        with t1_col[0]:
            idx_highest_rate = df_validos['Rate'].idxmax()
            poster_highest = df_validos.loc[idx_highest_rate, 'Poster']

            st.image(poster_highest, caption=df_validos.loc[idx_highest_rate,'Title'], use_container_width=True)

        with t1_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

        with t1_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_highest_rate, 'Rate']}/10.0** - Position: **{df_validos.loc[idx_highest_rate, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_highest_rate, 'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_highest_rate, 'Length']}** Minutes')
            st.write(f'Number of Reviews: ~**{df_validos.loc[idx_highest_rate,'VoteCount']}**')
            last_trend = df_validos.loc[idx_highest_rate,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)
    
    with st.expander('Worst Rated Movie', icon=':material/cancel:'):
        t4_col = st.columns([35,5,60])

        # Lowest Rating
        with t4_col[0]:
            idx_lowest_rate = df_validos['Rate'].idxmin()
            poster_lowest = df_validos.loc[idx_lowest_rate, 'Poster']

            st.image(poster_lowest, caption=df_validos.loc[idx_lowest_rate,'Title'], use_container_width=True)
        
        with t4_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

        with t4_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_lowest_rate, 'Rate']}/10.0** - Position: **{df_validos.loc[idx_lowest_rate, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_lowest_rate,'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_lowest_rate, 'Length']}** Minutes')
            st.write(f'Number of Reviews: ~**{df_validos.loc[idx_lowest_rate,'VoteCount']}**')
            last_trend = df_validos.loc[idx_lowest_rate,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)

with colsMain[1]:
    with st.expander('Most Reviewed Movie', icon=':material/reviews:'):
        t2_col = st.columns([35,5,60])

        with t2_col[0]:
            idx_highest_count = df_validos['VoteCount'].idxmax()
            poster_lowCount = df_validos.loc[idx_highest_count, 'Poster']
            st.image(poster_lowCount, caption=df_validos.loc[idx_highest_count,'Title'], use_container_width=True)
        
        with t2_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)
        
        with t2_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_highest_count, 'Rate']}/10.0** - **Position**: **{df_validos.loc[idx_highest_count, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_highest_count, 'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_highest_count, 'Length']}** Minutes')
            st.write(f'Number of Reviews: **~{df_validos.loc[idx_highest_count,'VoteCount']}**')
            last_trend = df_validos.loc[idx_highest_count,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)
    
    with st.expander('Least Reviewed Movie', icon=':material/hide_source:'):
        t22_col = st.columns([35,5,60])
        with t22_col[0]:
            idx_lowest_count = df_validos['VoteCount'].idxmin()
            poster_lowCount = df_validos.loc[idx_lowest_count, 'Poster']
            st.image(poster_lowCount, caption=df_validos.loc[idx_lowest_count,'Title'], use_container_width=True)
        
        with t22_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)
        
        with t22_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_lowest_count, 'Rate']}/10.0** - **Position**: **{df_validos.loc[idx_lowest_count, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_lowest_count, 'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_lowest_count, 'Length']}** Minutes')
            st.write(f'Number of Reviews: **~{df_validos.loc[idx_lowest_count,'VoteCount']}**')
            last_trend = df_validos.loc[idx_lowest_count,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)

with colsMain[2]:
    with st.expander('Most Trendy Movie', icon=':material/trending_up:'):
        aux_col = st.columns([35,5,60])
        with aux_col[0]:
            idx_highest_trend = df_validos['Trend'].idxmax()
            poster_lowCount = df_validos.loc[idx_highest_trend, 'Poster']
            st.image(poster_lowCount, caption=df_validos.loc[idx_highest_trend,'Title'], use_container_width=True)
        
        with aux_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)
        
        with aux_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_highest_trend, 'Rate']}/10.0** - **Position**: **{df_validos.loc[idx_highest_trend, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_highest_trend, 'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_highest_trend, 'Year']}** Minutes')
            st.write(f'Number of Reviews: **~{df_validos.loc[idx_highest_trend,'VoteCount']}**')
            last_trend = df_validos.loc[idx_highest_trend,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)

    with st.expander('Least Trendy Movie', icon=':material/trending_down:'):
        aux_col = st.columns([35,5,60])
        with aux_col[0]:
            idx_highest_trend = df_validos['Trend'].idxmin()
            poster_lowCount = df_validos.loc[idx_highest_trend, 'Poster']
            st.image(poster_lowCount, caption=df_validos.loc[idx_highest_trend,'Title'], use_container_width=True)
        
        with aux_col[1]:
            st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)
        
        with aux_col[2]:
            st.write(f'Rating: **{df_validos.loc[idx_highest_trend, 'Rate']}/10.0** - **Position**: **{df_validos.loc[idx_highest_trend, 'Position']}/{len(df)}**')
            st.write(f'Launched in **{df_validos.loc[idx_highest_trend, 'Year']}**')
            st.write(f'Length: **{df_validos.loc[idx_highest_trend, 'Year']}** Minutes')
            st.write(f'Number of Reviews: **~{df_validos.loc[idx_highest_trend,'VoteCount']}**')
            last_trend = df_validos.loc[idx_highest_trend,'Trend']
            if last_trend == 0:
                st.write(f'<p style="color:Orange;"><b>Kept the position since last update</b></p>', unsafe_allow_html=True)
            elif last_trend > 0:
                st.write(f'<p style="color:MediumSeaGreen;"><b>Up {last_trend} positions since last update</b></p>', unsafe_allow_html=True)
            else: 
                st.write(f'<p style="color:Red;"><b>Down {abs(last_trend)} positions since last update</b></p>', unsafe_allow_html=True)

st.subheader('Advanced Search', divider=True)

cols_boxes = st.columns(3)

if 'opn' not in st.session_state:
    st.session_state.opn = 'All'
if 'year' not in st.session_state:
    st.session_state.year = 'All'
if 'trend' not in st.session_state:
    st.session_state.trend = 'All'

df_search = df.copy()

if st.session_state.opn != 'All':
    df_search = df_search[df_search['Opinion'] == st.session_state.opn]
if st.session_state.year != 'All':
    df_search = df_search[df_search['Year'] == st.session_state.year]
if st.session_state.trend != 'All':
    df_search = df_search[df_search['Trend_Analysis'] == st.session_state.trend]

opn_list = ['All'] + sorted(df_search['Opinion'].unique())
year_list = ['All'] + sorted(df_search['Year'].unique())
trend_list = ['All'] + sorted(df_search['Trend_Analysis'].unique())

with cols_boxes[0]:
    opn = st.selectbox('Select Rate', opn_list, index=opn_list.index(st.session_state.opn), key='opn_select', on_change=update_opn)
    st.info('Bad: Below 5.0 || Mediocre: 5.1 - 6.5 || Good: 6.6 - 8.0 || Excellent: Above 8.1')

with cols_boxes[1]:
    year_select = st.selectbox('Select Year', year_list, index=year_list.index(st.session_state.year), on_change=update_year, key='year_select')
with cols_boxes[2]:
    trend = st.selectbox('Select Trend', trend_list, index=trend_list.index(st.session_state.trend), on_change=update_trend, key='trend_select')

st.divider()

cols = st.columns(3)

for index, row in df_search.reset_index().iterrows():

    aux = index % 3
    with cols[aux]:
        with st.expander(f'{row["Title"]} - {row['Year']}', icon=icon_movie(row['Opinion'])):
            cols2 = st.columns([35,5,60])
            with cols2[0]: 
                st.image(row['Poster'], caption=row['Title'], use_container_width=True)
            
            with cols2[1]:
                st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)
            
            with cols2[2]:
                st.write(index)
                st.write(f'Movie called **{row['Title']}**, launched in **{row['Year']}** and **{row['Length']}** minutes long, has a rating of **{row['Rate']}/10.0**.')

st.dataframe(df_search)