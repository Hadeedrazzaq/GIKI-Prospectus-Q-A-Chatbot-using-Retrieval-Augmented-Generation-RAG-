"""
Vector Store for GIKI Prospectus Q&A Chatbot
Simplified in-memory vector store for compatibility
"""
from typing import List, Dict, Any, Optional
import numpy as np
import json
import logging
from pathlib import Path
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVectorStore:
    """Simple in-memory vector store for compatibility"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        # In-memory storage
        self.documents = []
        self.embeddings = []
        self.metadata = []
        
        # Load existing data if available
        self._load_data()
        
        logger.info("SimpleVectorStore initialized")
    
    def _load_data(self):
        """Load data from disk if available"""
        try:
            data_file = self.persist_directory / "vector_store.pkl"
            if data_file.exists():
                with open(data_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get('documents', [])
                    self.embeddings = data.get('embeddings', [])
                    self.metadata = data.get('metadata', [])
                logger.info(f"Loaded {len(self.documents)} documents from disk")
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    
    def _save_data(self):
        """Save data to disk"""
        try:
            data = {
                'documents': self.documents,
                'embeddings': self.embeddings,
                'metadata': self.metadata
            }
            data_file = self.persist_directory / "vector_store.pkl"
            with open(data_file, 'wb') as f:
                pickle.dump(data, f)
            logger.info("Data saved to disk")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def add_documents(self, encoded_chunks: List[Dict[str, Any]]) -> bool:
        """Add documents to the vector store"""
        try:
            for chunk in encoded_chunks:
                self.documents.append(chunk['content'])
                self.embeddings.append(np.array(chunk['embedding']))
                self.metadata.append(chunk['metadata'])
            
            # Save to disk
            self._save_data()
            
            logger.info(f"Added {len(encoded_chunks)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def search_similar(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            if not self.embeddings:
                return []
            
            query_vector = np.array(query_embedding)
            
            # Compute similarities
            similarities = []
            for i, doc_embedding in enumerate(self.embeddings):
                similarity = self._cosine_similarity(query_vector, doc_embedding)
                similarities.append((similarity, i))
            
            # Sort by similarity (descending)
            similarities.sort(reverse=True)
            
            # Return top-k results
            results = []
            for similarity, idx in similarities[:top_k]:
                results.append({
                    'content': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'similarity_score': similarity
                })
            
            logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []
    
    def search_by_text(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search by text (simple keyword matching)"""
        try:
            if not self.documents:
                return []
            
            query_lower = query_text.lower()
            results = []
            
            for i, doc in enumerate(self.documents):
                doc_lower = doc.lower()
                if query_lower in doc_lower:
                    # Simple relevance score based on word overlap
                    query_words = set(query_lower.split())
                    doc_words = set(doc_lower.split())
                    overlap = len(query_words.intersection(doc_words))
                    relevance = overlap / max(len(query_words), 1)
                    
                    results.append({
                        'content': doc,
                        'metadata': self.metadata[i],
                        'similarity_score': relevance
                    })
            
            # Sort by relevance and return top-k
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching by text: {e}")
            return []
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        try:
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Error computing cosine similarity: {e}")
            return 0.0
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            unique_files = set()
            for meta in self.metadata:
                file_name = meta.get('file_name', 'Unknown')
                unique_files.add(file_name)
            
            return {
                'total_documents': len(self.documents),
                'unique_files': len(unique_files),
                'file_names': list(unique_files),
                'status': 'active' if self.documents else 'empty'
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {
                'total_documents': 0,
                'unique_files': 0,
                'file_names': [],
                'status': 'error'
            }
    
    def delete_collection(self) -> bool:
        """Delete the entire collection"""
        try:
            self.documents = []
            self.embeddings = []
            self.metadata = []
            self._save_data()
            logger.info("Collection deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False
    
    def reset_collection(self) -> bool:
        """Reset the collection (same as delete)"""
        return self.delete_collection()

# For compatibility, use the simple vector store
VectorStore = SimpleVectorStore
