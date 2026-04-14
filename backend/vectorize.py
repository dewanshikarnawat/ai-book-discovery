import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

DATA_PATH = "C:/Users/hp/AIBookDiscoveryProject/data/books/preprocessed/clean_books.csv"
MODEL_DIR = "C:/Users/hp/AIBookDiscoveryProject/backend/model"

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df['combined_text'] = df['combined_text'].fillna("")

tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=5000,
    ngram_range=(1, 2)
)

tfidf_matrix = tfidf.fit_transform(df['combined_text'])

similarity_matrix = cosine_similarity(tfidf_matrix)

with open(os.path.join(MODEL_DIR, "tfidf_vector.pkl"), "wb") as f:
    pickle.dump(tfidf, f)

with open(os.path.join(MODEL_DIR, "similarity_matrix.pkl"), "wb") as f:
    pickle.dump(similarity_matrix, f)

print("✅ Vectorization completed")
print("✅ TF-IDF model saved")
print("✅ Similarity matrix saved")