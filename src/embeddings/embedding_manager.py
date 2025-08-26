"""
Embedding Manager for GIKI Prospectus Q&A Chatbot
Handles text embedding generation using alternative approaches
"""
from typing import List, Dict, Any, Optional
import numpy as np
import logging
import hashlib
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleEmbeddingManager:
    """Simple embedding manager that uses hash-based embeddings for compatibility"""
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        self.model_name = "simple-hash-embedding"
        logger.info(f"SimpleEmbeddingManager initialized with dimension {embedding_dim}")
    
    def _text_to_hash_vector(self, text: str) -> np.ndarray:
        """Convert text to a hash-based vector"""
        # Create a hash of the text
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        # Convert hash to a fixed-size vector
        vector = np.zeros(self.embedding_dim)
        for i, char in enumerate(text_hash):
            if i < self.embedding_dim:
                vector[i] = ord(char) / 255.0
        
        # Fill remaining dimensions with hash-derived values
        for i in range(len(text_hash), self.embedding_dim):
            vector[i] = (ord(text_hash[i % len(text_hash)]) + i) % 255 / 255.0
        
        return vector
    
    def get_single_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        try:
            return self._text_to_hash_vector(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(self.embedding_dim)
    
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts"""
        try:
            return [self.get_single_embedding(text) for text in texts]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [np.zeros(self.embedding_dim) for _ in texts]
    
    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.embedding_dim
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings"""
        try:
            dot_product = np.dot(embedding1, embedding2)
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def batch_encode_with_metadata(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Encode chunks with metadata"""
        try:
            encoded_chunks = []
            for chunk in chunks:
                text = chunk.get('content', '')
                embedding = self.get_single_embedding(text)
                
                encoded_chunk = {
                    'content': text,
                    'embedding': embedding.tolist(),
                    'metadata': chunk.get('metadata', {})
                }
                encoded_chunks.append(encoded_chunk)
            
            logger.info(f"Encoded {len(encoded_chunks)} chunks")
            return encoded_chunks
            
        except Exception as e:
            logger.error(f"Error in batch encoding: {e}")
            return []

# For compatibility, use the simple embedding manager
EmbeddingManager = SimpleEmbeddingManager
