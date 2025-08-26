"""
RAG Engine for GIKI Prospectus Q&A Chatbot
Main orchestrator for the RAG pipeline
"""
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from document_processor import DocumentProcessor
from text_chunker import TextChunker
from embeddings.embedding_manager import EmbeddingManager
from vectorstore.vector_store import VectorStore
from llm.llm_manager import LLMManager
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    """Main RAG engine that orchestrates the entire pipeline"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.text_chunker = TextChunker()
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        self.llm_manager = LLMManager()
        
        logger.info("RAG Engine initialized successfully")
    
    def process_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process documents through the entire pipeline"""
        try:
            logger.info(f"Processing {len(file_paths)} documents")
            
            # Step 1: Extract text from documents
            logger.info("Step 1: Extracting text from documents")
            pages = self.document_processor.process_multiple_documents(file_paths)
            
            # Step 2: Chunk the text
            logger.info("Step 2: Chunking text")
            chunks = self.text_chunker.chunk_document_pages(pages)
            
            # Step 3: Generate embeddings
            logger.info("Step 3: Generating embeddings")
            encoded_chunks = self.embedding_manager.batch_encode_with_metadata(chunks)
            
            # Step 4: Store in vector database
            logger.info("Step 4: Storing in vector database")
            success = self.vector_store.add_documents(encoded_chunks)
            
            if not success:
                raise Exception("Failed to add documents to vector store")
            
            # Get statistics
            stats = self.text_chunker.get_chunk_statistics(chunks)
            vector_stats = self.vector_store.get_collection_stats()
            
            result = {
                'success': True,
                'files_processed': len(file_paths),
                'pages_extracted': len(pages),
                'chunks_created': len(chunks),
                'chunks_stored': len(encoded_chunks),
                'chunk_statistics': stats,
                'vector_store_stats': vector_stats
            }
            
            logger.info(f"Document processing completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'files_processed': 0,
                'pages_extracted': 0,
                'chunks_created': 0,
                'chunks_stored': 0
            }
    
    def ask_question(self, question: str, language: str = "en") -> Dict[str, Any]:
        """Ask a question and get an answer using RAG"""
        try:
            logger.info(f"Processing question: {question}")
            
            # Step 1: Generate embedding for the question
            question_embedding = self.embedding_manager.get_single_embedding(question)
            
            if len(question_embedding) == 0:
                raise Exception("Failed to generate question embedding")
            
            # Step 2: Search for relevant documents
            logger.info("Searching for relevant documents")
            search_results = self.vector_store.search_similar(question_embedding.tolist())
            
            if not search_results:
                logger.warning("No relevant documents found")
                return {
                    'success': True,
                    'answer': "I don't have enough information from the uploaded documents to answer this question. Please make sure relevant GIKI documents are uploaded.",
                    'sources': [],
                    'confidence': 0.0
                }
            
            # Step 3: Prepare context from search results
            context_parts = []
            sources = []
            
            for result in search_results:
                context_parts.append(result['content'])
                sources.append({
                    'file_name': result['metadata'].get('file_name', 'Unknown'),
                    'page_number': result['metadata'].get('page_number', 'Unknown'),
                    'similarity_score': result['similarity_score']
                })
            
            context = "\n\n".join(context_parts)
            
            # Step 4: Generate answer using LLM
            logger.info("Generating answer using LLM")
            answer = self.llm_manager.generate_response(question, context, language)
            
            # Calculate average confidence
            avg_confidence = sum(result['similarity_score'] for result in search_results) / len(search_results)
            
            result = {
                'success': True,
                'answer': answer,
                'sources': sources,
                'confidence': avg_confidence,
                'context_length': len(context),
                'sources_count': len(sources)
            }
            
            logger.info(f"Question answered successfully with confidence: {avg_confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'answer': "Sorry, I encountered an error while processing your question. Please try again.",
                'sources': [],
                'confidence': 0.0
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the RAG system"""
        try:
            # Check vector store status
            vector_stats = self.vector_store.get_collection_stats()
            
            # Check available LLM providers
            available_providers = self.llm_manager.get_available_providers()
            
            # Check embedding model
            embedding_dim = self.embedding_manager.get_embedding_dimension()
            
            return {
                'vector_store': {
                    'status': 'active' if vector_stats['total_documents'] > 0 else 'empty',
                    'total_documents': vector_stats['total_documents'],
                    'unique_files': vector_stats['unique_files'],
                    'file_names': vector_stats['file_names']
                },
                'llm': {
                    'current_provider': self.llm_manager.provider,
                    'available_providers': available_providers
                },
                'embeddings': {
                    'model': self.embedding_manager.model_name,
                    'dimension': embedding_dim
                },
                'configuration': {
                    'chunk_size': self.text_chunker.chunk_size,
                    'chunk_overlap': self.text_chunker.chunk_overlap,
                    'top_k_retrieval': Config.TOP_K_RETRIEVAL
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def reset_system(self) -> bool:
        """Reset the entire system (clear vector store)"""
        try:
            logger.info("Resetting RAG system")
            success = self.vector_store.reset_collection()
            
            if success:
                logger.info("RAG system reset successfully")
            else:
                logger.error("Failed to reset RAG system")
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting system: {str(e)}")
            return False
