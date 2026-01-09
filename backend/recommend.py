import pandas as pd
import pickle
import numpy as np
import re

DATA_PATH = "C:/Users/hp/AIBookDiscoveryProject/data/books/preprocessed/clean_books.csv"
MODEL_DIR = "C:/Users/hp/AIBookDiscoveryProject/backend/model"

df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded {len(df)} books")

with open(f"{MODEL_DIR}/similarity_matrix.pkl", "rb") as f:
    similarity_matrix = pickle.load(f)
print(f"✅ Model loaded: {similarity_matrix.shape}")

def normalize(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def recommend_books(book_title, top_n=5):
    query = normalize(book_title)
    print(f"🔍 Searching for: '{query}'")
    
    matches = df[df['title_clean'].apply(normalize).str.contains(query, na=False)]
    print(f"✅ Found {len(matches)} matches")
    
    if matches.empty:
        print("❌ No matches found!")
        return []
    
    idx = matches.index[0]
    print(f"✅ Using book index: {idx}")
    
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_books = similarity_scores[1:top_n + 1]
    
    recommendations = []
    for i, score in top_books:
        recommendations.append({
            "title": df.iloc[i]['title'],
            "author": df.iloc[i]['authors'],
            "rating": float(df.iloc[i]['average_rating']),
            "similarity_score": float(score)
        })
    
    return recommendations

if __name__ == "__main__":
    print("🚀 Testing...")
    results = recommend_books("harry potter")
    print("\n📚 RECOMMENDATIONS:")
    for book in results:
        print(f"• {book['title']} by {book['author']} ({book['rating']}⭐ | {book['similarity_score']:.2f})")