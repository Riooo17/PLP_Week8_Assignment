import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("all_sources_metadata_2020-03-13.csv", low_memory=False)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Title
st.title("CORD-19 Data Explorer")
st.write("A simple exploration of COVID-19 research papers")

# Sidebar
st.sidebar.header("Filters")
years = st.sidebar.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2020))

# Filter data
filtered = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]

# Show sample data
st.subheader("Sample Data")
st.write(filtered.head())

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top Sources
st.subheader("Top Sources")
top_sources = filtered['source_x'].value_counts().head(10)
fig, ax = plt.subplots()
top_sources.plot(kind='bar', ax=ax)
ax.set_xlabel("Source")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# WordCloud
st.subheader("WordCloud of Titles")
text = " ".join(str(title) for title in filtered['title'].dropna())
if text.strip():
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("No titles available for WordCloud.")
