# classifier/utils.py
import re
import nltk
import torch
import string
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from nltk.corpus import stopwords

# Download NLTK data if not already present
nltk.download('stopwords')

# Load the DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

# Load the saved model weights
model.load_state_dict(torch.load('../model/model_weights.pth', map_location=torch.device('cpu')))
model.eval()

# Preprocessing tools
stop_words = set(stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")


def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def preprocess_data(text):
    text = clean_text(text)
    text = ' '.join(word for word in text.split(' ') if word not in stop_words)
    text = ' '.join(stemmer.stem(word) for word in text.split(' '))
    return text


def classify_sms(sms):
    print("Cleaned SMS:", sms)
    inputs = tokenizer(sms, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits).item()
    probability = torch.softmax(logits, dim=1)[0][predicted_class].item()
    return 'spam' if predicted_class == 1 else 'ham', probability
