import json
from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

class ChatbotLogic:
    def __init__(self, dataset_path: str, unanswered_path: str):
        self.dataset_path = Path(dataset_path)
        self.unanswered_path = Path(unanswered_path)
        self._initialize_files()
        self._initialize_nltk()
        
    def _initialize_nltk(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
    def _initialize_files(self):
        """Ensure data files exist"""
        for file_path in [self.dataset_path, self.unanswered_path]:
            if not file_path.exists():
                file_path.write_text('[]')
                
    def _load_json(self, file_path: Path):
        """Load data from JSON file"""
        try:
            return json.loads(file_path.read_text())
        except Exception:
            return []
            
    def _save_json(self, data: list, file_path: Path):
        """Save data to JSON file"""
        file_path.write_text(json.dumps(data, indent=4))
        
    def preprocess_text(self, text: str):
        """Preprocess text for matching"""
        tokens = word_tokenize(text.lower())
        return [
            self.stemmer.stem(word)
            for word in tokens
            if word.isalnum() and word not in self.stop_words
        ]
        
    def find_best_response(self, query: str):
        """Find best matching response for query"""
        dataset = self._load_json(self.dataset_path)
        if not dataset:
            return None
            
        query_tokens = set(self.preprocess_text(query))
        best_match = None
        highest_score = 0
        
        for qa in dataset:
            qa_tokens = set(self.preprocess_text(qa['question']))
            intersection = len(query_tokens & qa_tokens)
            union = len(query_tokens | qa_tokens)
            score = intersection / union if union > 0 else 0
            
            if score > highest_score:
                highest_score = score
                best_match = qa['response']
        
        return best_match if highest_score > 0.3 else None
        
    def add_unanswered(self, question: str):
        """Add question to unanswered list"""
        unanswered = self._load_json(self.unanswered_path)
        if not any(qa['question'] == question for qa in unanswered):
            unanswered.append({'question': question, 'response': ''})
            self._save_json(unanswered, self.unanswered_path)
    def save_answer(self, question: str, response: str) -> bool:
        try:
            # Load dataset
            dataset = self._load_json(self.dataset_path)
            dataset.append({'question': question, 'response': response})
            self._save_json(dataset, self.dataset_path)

            # Remove from unanswered
            unanswered = self._load_json(self.unanswered_path)
            unanswered = [qa for qa in unanswered if qa['question'] != question]
            self._save_json(unanswered, self.unanswered_path)
            return True
        except Exception as e:
            print(f"Error saving answer: {str(e)}")
            return False
