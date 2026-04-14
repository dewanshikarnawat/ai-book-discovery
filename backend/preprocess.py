import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')


RAW_PATH = "C:/Users/hp/AIBookDiscoveryProject/data/books/raw/books.csv" 

df = pd.read_csv(
    RAW_PATH,
    on_bad_lines="skip",
    quotechar='"'
)

print("Initial dataset shape:", df.shape)


df.columns = df.columns.str.strip()
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)


df['average_rating'] = df['average_rating'].fillna(df['average_rating'].mean())
df['num_pages'] = df['num_pages'].fillna(df['num_pages'].median())
df['ratings_count'] = df['ratings_count'].fillna(0)
df['text_reviews_count'] = df['text_reviews_count'].fillna(0)

df['authors'] = df['authors'].fillna("unknown")
df['publisher'] = df['publisher'].fillna("unknown")
df['language_code'] = df['language_code'].fillna("unknown")

print("\nMissing values after cleaning:")
print(df.isnull().sum())


def clean_title(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  
    return re.sub(r"\s+", " ", text).strip()


def clean_simple(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


df['title_clean'] = df['title'].apply(clean_title)
df['authors_clean'] = df['authors'].apply(clean_simple)
df['publisher_clean'] = df['publisher'].apply(clean_simple)


df['combined_text'] = (
    df['title_clean'] + " " +
    df['authors_clean'] + " " +
    df['publisher_clean']
)


PROCESSED_PATH = "C:/Users/hp/AIBookDiscoveryProject/data/books/preprocessed/clean_books.csv"

df.to_csv(PROCESSED_PATH, index=False)

print("\n✅ Preprocessing completed successfully")
print("Final dataset shape:", df.shape)
print("Saved to:", PROCESSED_PATH)


print("\nSample rows:")
print(df[['title_clean', 'authors_clean', 'combined_text']].head())