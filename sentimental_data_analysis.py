# sentimental_data_analysis.py
from imports import *

def run_sentimental_data_analysis(trump_df, biden_df):
    # Load the dataset
    language_dataset = pd.read_csv('/Users/gulsah/Desktop/REDI/redi_fall2024_data_circle_twitter_project/csv/Language Detection.csv')

    # Data cleaning
    # 1. Lowercase conversion
    language_dataset['Text'] = language_dataset['Text'].str.lower()
    # 2. Remove emojis
    language_dataset['Text'] = language_dataset['Text'].apply(lambda x: re.sub(r'[^\w\s,]', '', x))
    # 3. Remove URLs
    language_dataset['Text'] = language_dataset['Text'].apply(lambda x: re.sub(r'http\S+|www\S+', '', x))
    # 4. Remove mentions & hashtags
    language_dataset['Text'] = language_dataset['Text'].apply(lambda x: re.sub(r'@\w+|#\w+', '', x))
    # 5. Remove punctuation, numbers, and special characters
    language_dataset['Text'] = language_dataset['Text'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

    # Feature extraction: convert text into numerical features (Bag of Words)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(language_dataset['Text'])  # Text data
    y = language_dataset['Language']  # Language labels

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model selection: Multinomial Naive Bayes
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Feature extraction: convert text into numerical features (Bag of Words)
    text_transformed = vectorizer.transform(trump_df['tweet'])
    trump_df['predicted_language'] = model.predict(text_transformed)
    # Display the DataFrame with the predictions
    # trump_df[['tweet', 'predicted_language']]
    st.dataframe(trump_df.groupby('predicted_language')['tweet'].count())