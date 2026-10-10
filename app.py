import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title('Overall Analysis')

    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(round(max_funding)) + ' Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups', num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    ax3.tick_params(axis='x', rotation=90)
    st.pyplot(fig3)


def load_startup_details(startup):
    st.title(startup)
    s_df = df[df['startup'] == startup].sort_values('date', ascending=False)

    # basic info
    latest = s_df.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric('Industry', latest['vertical'])
    col2.metric('City', latest['city'])
    col3.metric('Total Raised', str(round(s_df['amount'].sum(), 2)) + ' Cr')

    if pd.notna(latest.get('subvertical')):
        st.write('**Sub-industry:**', latest['subvertical'])

    # funding rounds
    st.subheader('Funding Rounds')
    st.dataframe(s_df[['date', 'round', 'investors', 'amount']].reset_index(drop=True))

    # funding over time
    st.subheader('Funding Over Time')
    year_series = s_df.groupby('year')['amount'].sum()
    fig, ax = plt.subplots()
    ax.bar(year_series.index.astype(int).astype(str), year_series.values)
    ax.set_ylabel('Amount (Cr)')
    st.pyplot(fig)

    # similar startups (same vertical + city)
    st.subheader('Similar Startups')
    similar = df[(df['vertical'] == latest['vertical']) & (df['startup'] != startup)]
    similar = (similar.groupby('startup')['amount'].sum()
               .sort_values(ascending=False).head(5).reset_index())
    st.dataframe(similar)


def load_investor_details(investor):
    st.title(investor)
    inv_df = df[df['investors'].str.contains(investor, regex=False, na=False)]

    last5_df = inv_df.head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        big_series = inv_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col2:
        vertical_series = inv_df.groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    year_series = inv_df.groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
    if btn1:
        load_startup_details(selected_startup)

else:
    investor_list = sorted({i.strip() for i in df['investors'].dropna().str.split(',').sum() if i.strip()})
    selected_investor = st.sidebar.selectbox('Select Investor', investor_list)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)