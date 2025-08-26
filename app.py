"""
GIKI Prospectus Q&A Chatbot - Main Application
Streamlit web interface for the RAG-based chatbot
"""
import streamlit as st
import os
import tempfile
from pathlib import Path
import logging
from datetime import datetime
import json

# Import our RAG components
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag.rag_engine import RAGEngine
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Detect system theme preference
def detect_system_theme():
    """Detect system dark/light mode preference"""
    try:
        import platform
        if platform.system() == "Windows":
            import subprocess
            result = subprocess.run(['reg', 'query', 'HKCU', '/v', 'AppsUseLightTheme'], 
                                  capture_output=True, text=True)
            if '0x00000000' in result.stdout:
                return "dark"
            else:
                return "light"
        elif platform.system() == "Darwin":  # macOS
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            if 'Dark' in result.stdout:
                return "dark"
            else:
                return "light"
        else:  # Linux and others
            return "light"  # Default to light
    except:
        return "light"  # Default to light if detection fails

# Get system theme
system_theme = detect_system_theme()

# Page configuration with theme
st.set_page_config(
    page_title="GIKI Prospectus Q&A Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with dark mode support
dark_mode_css = """
<style>
    /* Dark mode styles */
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background-color: #1e3a5f;
        border-left: 4px solid #2196f3;
        color: #ffffff;
    }
    
    .bot-message {
        background-color: #2d1b3d;
        border-left: 4px solid #9c27b0;
        color: #ffffff;
    }
    
    .source-info {
        background-color: #2d1b1b;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.8rem;
        color: #ffffff;
    }
    
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    
    .model-info {
        background-color: #1a1a2e;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #ffffff;
    }
    
    .gemini-highlight {
        background-color: #1a2e1a;
        border-left: 4px solid #4caf50;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #ffffff;
    }
    
    /* Dark mode specific adjustments */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border-color: #4a4a4a;
    }
    
    .stSelectbox > div > div > div {
        background-color: #262730;
        color: #ffffff;
    }
    
    .stButton > button {
        background-color: #4a4a4a;
        color: #ffffff;
        border-color: #666666;
    }
    
    .stButton > button:hover {
        background-color: #666666;
        border-color: #888888;
    }
    
    /* Additional dark mode improvements */
    .stMarkdown {
        color: #ffffff;
    }
    
    .stText {
        color: #ffffff;
    }
    
    .stAlert {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    
    .stSuccess {
        background-color: #1a2e1a;
        color: #ffffff;
    }
    
    .stError {
        background-color: #2e1a1a;
        color: #ffffff;
    }
    
    .stInfo {
        background-color: #1a1a2e;
        color: #ffffff;
    }
</style>
"""

light_mode_css = """
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .source-info {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.8rem;
    }
    
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    
    .model-info {
        background-color: #f0f8ff;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .gemini-highlight {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
"""

# Apply theme-appropriate CSS
if system_theme == "dark":
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    if 'system_status' not in st.session_state:
        st.session_state.system_status = None

def initialize_rag_engine():
    """Initialize the RAG engine"""
    try:
        if st.session_state.rag_engine is None:
            with st.spinner("Initializing RAG Engine..."):
                st.session_state.rag_engine = RAGEngine()
                st.session_state.system_status = st.session_state.rag_engine.get_system_status()
            st.success("RAG Engine initialized successfully!")
        return True
    except Exception as e:
        st.error(f"Failed to initialize RAG Engine: {str(e)}")
        return False

def get_data_folder_files():
    """Get all supported files from the data folder"""
    data_folder = Path("data")
    if not data_folder.exists():
        return []
    
    supported_extensions = ['.pdf', '.docx', '.txt', '.doc']
    files = []
    
    for file_path in data_folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files.append(str(file_path))
    
    return files

def process_documents_from_data_folder():
    """Process documents from the data folder"""
    if not initialize_rag_engine():
        return False
    
    data_files = get_data_folder_files()
    if not data_files:
        return False
    
    try:
        with st.spinner(f"Processing {len(data_files)} documents from data folder..."):
            # Process documents
            result = st.session_state.rag_engine.process_documents(data_files)
            
            if result['success']:
                st.session_state.documents_processed = True
                st.session_state.system_status = st.session_state.rag_engine.get_system_status()
                
                # Display results
                st.success(f"✅ Successfully processed {result['files_processed']} files from data folder!")
                st.info(f"📄 Pages extracted: {result['pages_extracted']}")
                st.info(f"🔢 Chunks created: {result['chunks_created']}")
                st.info(f"💾 Chunks stored: {result['chunks_stored']}")
                
                return True
            else:
                st.error(f"❌ Failed to process documents: {result.get('error', 'Unknown error')}")
                return False
                
    except Exception as e:
        st.error(f"❌ Error processing files from data folder: {str(e)}")
        return False

def process_uploaded_files(uploaded_files):
    """Process uploaded files"""
    if not uploaded_files:
        return False
    
    if not initialize_rag_engine():
        return False
    
    try:
        # Save uploaded files to temporary directory
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        
        with st.spinner("Processing uploaded files..."):
            for uploaded_file in uploaded_files:
                # Save file
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(file_path)
            
            # Process documents
            result = st.session_state.rag_engine.process_documents(file_paths)
            
            if result['success']:
                st.session_state.documents_processed = True
                st.session_state.system_status = st.session_state.rag_engine.get_system_status()
                
                # Display results
                st.success(f"✅ Successfully processed {result['files_processed']} uploaded files!")
                st.info(f"📄 Pages extracted: {result['pages_extracted']}")
                st.info(f"🔢 Chunks created: {result['chunks_created']}")
                st.info(f"💾 Chunks stored: {result['chunks_stored']}")
                
                return True
            else:
                st.error(f"❌ Failed to process documents: {result.get('error', 'Unknown error')}")
                return False
                
    except Exception as e:
        st.error(f"❌ Error processing files: {str(e)}")
        return False

def display_chat_message(message, is_user=True):
    """Display a chat message"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>GIKI Assistant:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Initialize theme variables
    theme_options = ["System", "Light", "Dark"]
    selected_theme = "System"  # Default value
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Theme toggle
        st.subheader("🎨 Theme")
        selected_theme = st.selectbox(
            "Theme Mode",
            theme_options,
            index=0 if system_theme == "light" else 1 if system_theme == "dark" else 0
        )
        
        # Apply theme based on selection
        if selected_theme == "System":
            current_theme = system_theme
        else:
            current_theme = selected_theme.lower()
        
        # Re-apply CSS based on selected theme
        if current_theme == "dark":
            st.markdown(dark_mode_css, unsafe_allow_html=True)
        else:
            st.markdown(light_mode_css, unsafe_allow_html=True)
    
    # Header with theme indicator (after sidebar theme selection)
    theme_icon = "🌙" if current_theme == "dark" else "☀️"
    st.markdown(f"""
    <div class="main-header">
        <h1>🎓 GIKI Prospectus Q&A Chatbot {theme_icon}</h1>
        <p>Ask questions about GIKI documents using AI-powered retrieval</p>
        <small>Theme: {current_theme.title()} Mode</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for documents in data folder
    data_files = get_data_folder_files()
    
    # Language selection (moved outside sidebar)
    language = st.selectbox(
        "Language",
        ["en", "ur"],
        format_func=lambda x: "English" if x == "en" else "اردو (Urdu)"
    )
    
    # LLM Provider Selection
    st.header("🤖 AI Model Settings")
    if st.session_state.rag_engine:
        available_providers = st.session_state.rag_engine.llm_manager.get_available_providers()
        
        if available_providers:
            selected_provider = st.selectbox(
                "AI Provider",
                available_providers,
                format_func=lambda x: x.title()
            )
            
            # Show model information
            if selected_provider == "openrouter":
                st.markdown("""
                <div class="gemini-highlight">
                    <strong>🆓 GPT-3.5 Turbo (FREE)</strong><br>
                    ⭐ Fast, accurate, and completely free!
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="model-info">
                    <strong>🆓 OpenRouter Free Models:</strong><br>
                    • GPT-3.5 Turbo (Recommended)<br>
                    • GPT-3.5 Turbo 16K<br>
                    • Llama 2 (7B & 13B)<br>
                    • Claude Instant<br>
                    • PaLM 2 Chat<br>
                    • DialoGPT
                </div>
                """, unsafe_allow_html=True)
            
            # Model selection for OpenRouter
            openrouter_models = st.session_state.rag_engine.llm_manager.get_openrouter_models()
            if openrouter_models:
                # Find GPT-3.5-turbo model index (default)
                default_index = 0
                for i, model in enumerate(openrouter_models):
                    if "gpt-3.5-turbo" in model.lower():
                        default_index = i
                        break
                
                selected_model = st.selectbox(
                    "OpenRouter Model",
                    openrouter_models,
                    index=default_index,
                    format_func=lambda x: f"🌟 {x}" if "gpt-3.5-turbo" in x.lower() else x
                )
                if st.button("🔄 Switch Model"):
                    try:
                        # Update the model in the OpenRouter LLM
                        st.session_state.rag_engine.llm_manager.openrouter_llm.model = selected_model
                        st.success(f"Switched to {selected_model}")
                    except Exception as e:
                        st.error(f"Failed to switch model: {str(e)}")
            
            elif selected_provider == "openai":
                st.markdown("""
                <div class="model-info">
                    <strong>🔑 OpenAI Models:</strong><br>
                    • GPT-3.5 Turbo<br>
                    • GPT-4 (if available)
                </div>
                """, unsafe_allow_html=True)
            
            elif selected_provider == "anthropic":
                st.markdown("""
                <div class="model-info">
                    <strong>🔑 Anthropic Models:</strong><br>
                    • Claude 3 Sonnet<br>
                    • Claude Instant
                </div>
                """, unsafe_allow_html=True)
            
            # Switch provider button
            if st.button("🔄 Switch Provider"):
                try:
                    st.session_state.rag_engine.llm_manager.switch_provider(selected_provider)
                    st.success(f"Switched to {selected_provider.title()}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to switch provider: {str(e)}")
        else:
            st.warning("⚠️ No AI providers available. Please check your API keys.")
    
    # System status
    st.header("📊 System Status")
    if st.session_state.system_status:
        status = st.session_state.system_status
        if 'error' not in status:
            st.markdown(f"**Vector Store:** {status['vector_store']['status']}")
            st.markdown(f"**Documents:** {status['vector_store']['total_documents']}")
            st.markdown(f"**Files:** {status['vector_store']['unique_files']}")
            st.markdown(f"**LLM:** {status['llm']['current_provider']}")
        else:
            st.error("System status unavailable")
    
    # Reset button
    if st.button("🔄 Reset System"):
        if st.session_state.rag_engine:
            if st.session_state.rag_engine.reset_system():
                st.session_state.documents_processed = False
                st.session_state.chat_history = []
                st.session_state.system_status = st.session_state.rag_engine.get_system_status()
                st.success("System reset successfully!")
            else:
                st.error("Failed to reset system")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Document Management")
        
        # Check for documents in data folder
        data_files = get_data_folder_files()
        
        if data_files:
            st.success(f"📂 Found {len(data_files)} documents in data folder:")
            for file_path in data_files:
                file_name = Path(file_path).name
                st.markdown(f"📄 {file_name}")
            
            # Auto-process data folder documents if not already processed
            if not st.session_state.documents_processed:
                if st.button("🚀 Load Documents from Data Folder"):
                    process_documents_from_data_folder()
        else:
            st.info("📂 No documents found in data folder. You can:")
            st.markdown("1. **Place documents** in the `data/` folder")
            st.markdown("2. **Upload documents** using the form below")
        
        # Additional upload section
        st.header("📤 Upload Additional Documents")
        st.info("Upload more documents to add to the existing knowledge base")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload additional GIKI documents (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt', 'doc'],
            accept_multiple_files=True,
            help="Upload additional documents to enhance the knowledge base"
        )
        
        if uploaded_files:
            if len(uploaded_files) > Config.MAX_DOCUMENTS:
                st.warning(f"⚠️ Maximum {Config.MAX_DOCUMENTS} documents allowed. Only the first {Config.MAX_DOCUMENTS} will be processed.")
                uploaded_files = uploaded_files[:Config.MAX_DOCUMENTS]
            
            # Process button
            if st.button("🚀 Process Uploaded Documents"):
                process_uploaded_files(uploaded_files)
        
        # Document information
        if st.session_state.documents_processed and st.session_state.system_status:
            st.header("📋 Loaded Documents")
            status = st.session_state.system_status
            if 'vector_store' in status:
                for file_name in status['vector_store']['file_names']:
                    st.markdown(f"📄 {file_name}")
    
    with col2:
        st.header("💬 Chat Interface")
        
        # Initialize RAG engine if not done
        if not st.session_state.rag_engine:
            if st.button("🔧 Initialize System"):
                initialize_rag_engine()
        
        # Auto-initialize and load documents if available
        if st.session_state.rag_engine and not st.session_state.documents_processed and data_files:
            if st.button("🚀 Auto-Load Documents"):
                process_documents_from_data_folder()
        
        # Chat interface
        if st.session_state.rag_engine and st.session_state.documents_processed:
            # Display chat history
            for message in st.session_state.chat_history:
                display_chat_message(message['content'], message['is_user'])
                if not message['is_user'] and 'sources' in message:
                    with st.expander("📚 View Sources"):
                        for source in message['sources']:
                            st.markdown(f"**{source['file_name']}** (Page {source['page_number']}) - Confidence: {source['similarity_score']:.2f}")
            
            # Question input
            question = st.text_input("Ask a question about GIKI:", key="question_input")
            
            if st.button("🤖 Ask Question") and question:
                # Add user message to history
                st.session_state.chat_history.append({
                    'content': question,
                    'is_user': True,
                    'timestamp': datetime.now()
                })
                
                # Get answer
                with st.spinner("🤔 Thinking..."):
                    result = st.session_state.rag_engine.ask_question(question, language)
                
                if result['success']:
                    # Add bot response to history
                    st.session_state.chat_history.append({
                        'content': result['answer'],
                        'is_user': False,
                        'sources': result['sources'],
                        'confidence': result['confidence'],
                        'timestamp': datetime.now()
                    })
                    
                    # Display the new messages
                    display_chat_message(question, True)
                    display_chat_message(result['answer'], False)
                    
                    # Show sources
                    if result['sources']:
                        with st.expander("📚 View Sources"):
                            for source in result['sources']:
                                st.markdown(f"**{source['file_name']}** (Page {source['page_number']}) - Confidence: {source['similarity_score']:.2f}")
                    
                    # Show confidence
                    st.info(f"Confidence: {result['confidence']:.2f}")
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
                
                # Clear input - use rerun instead of direct assignment
                st.rerun()
        
        elif not st.session_state.documents_processed:
            if data_files:
                st.info("📝 Documents found in data folder. Click '🚀 Load Documents from Data Folder' to start chatting.")
            else:
                st.info("📝 No documents available. Please add documents to the data folder or upload files to start chatting.")
        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🎓 GIKI Prospectus Q&A Chatbot | Powered by RAG (Retrieval-Augmented Generation)</p>
        <p>Upload GIKI documents and ask questions to get AI-powered answers!</p>
        <p>🆓 Powered by Google Gemini 2.0 Flash Experimental (FREE) via OpenRouter</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
