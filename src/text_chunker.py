"""
Text chunking module for GIKI Prospectus Q&A Chatbot
Handles splitting documents into chunks for vector embedding
"""
from typing import List, Dict, Any
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextChunker:
    """Handles text chunking for RAG system"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self._count_tokens,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        try:
            encoding = tiktoken.get_encoding("cl100k_base")  # OpenAI's encoding
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Error counting tokens, using character count: {e}")
            return len(text)
    
    def chunk_document_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk document pages into smaller pieces"""
        chunks = []
        
        for page in pages:
            try:
                # Split page text into chunks
                page_chunks = self.text_splitter.split_text(page['text'])
                
                # Create chunk objects with metadata
                for i, chunk_text in enumerate(page_chunks):
                    if chunk_text.strip():  # Only add non-empty chunks
                        chunk = {
                            'content': chunk_text.strip(),
                            'metadata': {
                                'file_name': page['file_name'],
                                'page_number': page['page_number'],
                                'chunk_index': i,
                                'total_chunks': len(page_chunks),
                                'chunk_size': len(chunk_text),
                                'token_count': self._count_tokens(chunk_text)
                            }
                        }
                        chunks.append(chunk)
                
                logger.info(f"Created {len(page_chunks)} chunks from page {page['page_number']} of {page['file_name']}")
                
            except Exception as e:
                logger.error(f"Error chunking page {page.get('page_number', 'unknown')} from {page.get('file_name', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Total chunks created: {len(chunks)}")
        return chunks
    
    def chunk_text_with_metadata(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk a single text with metadata"""
        try:
            chunks = self.text_splitter.split_text(text)
            chunk_objects = []
            
            for i, chunk_text in enumerate(chunks):
                if chunk_text.strip():
                    chunk = {
                        'content': chunk_text.strip(),
                        'metadata': {
                            **metadata,
                            'chunk_index': i,
                            'total_chunks': len(chunks),
                            'chunk_size': len(chunk_text),
                            'token_count': self._count_tokens(chunk_text)
                        }
                    }
                    chunk_objects.append(chunk)
            
            return chunk_objects
            
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            raise
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about the chunks"""
        if not chunks:
            return {
                'total_chunks': 0,
                'total_tokens': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0
            }
        
        total_tokens = sum(chunk['metadata']['token_count'] for chunk in chunks)
        chunk_sizes = [chunk['metadata']['chunk_size'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'total_tokens': total_tokens,
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes)
        }
    
    def filter_chunks_by_size(self, chunks: List[Dict[str, Any]], min_size: int = 10, max_size: int = None) -> List[Dict[str, Any]]:
        """Filter chunks based on size constraints"""
        filtered_chunks = []
        
        for chunk in chunks:
            chunk_size = chunk['metadata']['chunk_size']
            
            # Check minimum size
            if chunk_size < min_size:
                continue
            
            # Check maximum size
            if max_size and chunk_size > max_size:
                continue
            
            filtered_chunks.append(chunk)
        
        logger.info(f"Filtered {len(chunks)} chunks to {len(filtered_chunks)} chunks")
        return filtered_chunks
