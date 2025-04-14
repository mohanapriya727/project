import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load dataset
st.title("CSV File Uploader")

# File uploader widget
uploaded_file = st.file_uploader("C:\\Users\\ELCOT\\Documents\\IMDB.csv", type="csv")

if uploaded_file is not None:
    # Read the CSV file as a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the dataframe
    st.write("Here is your data:")
    st.dataframe(df)

#genre based rating leaders
st.header("Top-Rated Movie for each genre")
top_rated_per_genre = df.loc[df.groupby('Genre')['Rating'].idxmax()][['Genre', 'Title', 'Rating']]
st.write(top_rated_per_genre)


#correlation analysis
st.header ("Correlation Analysis: Rating vs Voting Counts")
sns.scatterplot(data=df, x='Votes', y='Rating')
plt.title ('Correlation between Ratings and Voteing Counts')
st.pyplot(plt)


#rating by genre heatmap
st.header("Rating by Genre Heatmap")
rating_by_genre = df.pivot_table(values='Rating', index='Genre', aggfunc='mean')
sns.heatmap(rating_by_genre,annot=True, cmap='coolwarm')
plt.title('Average Rating by Genre')
st.pyplot(plt)

#top 10 movie by rating and voting counts
st.header("Top 10 Movies by rating and VotingCounts")
top_movies = df.nlargest(10, 'Rating')[['Title', 'Rating', 'Votes']]
st.write(top_movies)

#genre distribution
st.header("Genre Distribution")
genre_counts = df['Genre'].value_counts()
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.xticks(rotation=45)
plt.title('Count of Movies by Genre')
st.pyplot(plt)

#average duration by genre
st.header("Average Duration by Genre")
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
avg_duration = df.groupby('Genre')['Duration'].mean().sort_values()
plt.figure(figsize=(10, 5))
avg_duration.plot(kind='bar')
plt.title('Average Movie Duration by Genre')
st.pyplot(plt)

#voting trends by genre
def clean_votes(vote):
    vote = vote.strip()  # Remove leading/trailing spaces
    vote = vote.replace(',', '')  # Remove commas
    vote = vote.replace('(', '').replace(')', '')  # Remove parentheses
    vote = vote.upper()  # In case 'k' is lowercase
    if 'K' in vote:
        try:
            return float(vote.replace('K', '')) * 1000
        except:
            return None
    try:
        return float(vote)
    except:
        return None  # or np.nan
df['Votes'] = df['Votes'].apply(clean_votes)
st.header("Voting Trends by Genre")
avg_votes = df.groupby('Genre')['Votes'].mean().sort_values()
plt.figure(figsize=(10, 5))
avg_votes.plot(kind='bar')
plt.title("Average Voting Counts by Genre")
st.pyplot(plt)

#rating distribution
st.header("Rating Distribution")
plt.figure(figsize=(10,5))
sns.histplot(df['Rating'],bins=20)
plt.title("Distribution of Movie Ratings")
st.pyplot(plt)

#most popular genres by voting
st.header("Most Popular Genres by Voting")
popular_genres = df.groupby('Genre')['Votes'].sum()
plt.figure(figsize=(10, 5))
popular_genres.plot(kind='pie')
plt.title('Most Popular Genresby Voting')
st.pyplot(plt)


#duration extrems
st.header("Shorest and Longest Movie")
shortest_movie = df.loc[df['Duration'].idxmin()][['Title', 'Duration']]
longest_movie = df.loc[df['Duration'].idxmax()][['Title', 'Duration']]
st.write("Shorest Movie:", shortest_movie)
st.write("Longest Movie:", longest_movie)

