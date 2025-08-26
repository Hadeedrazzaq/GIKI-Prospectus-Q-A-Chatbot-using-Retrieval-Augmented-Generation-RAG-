# 🆓 OpenRouter API Setup Guide

This guide will help you set up OpenRouter API to use free AI models for the GIKI Prospectus Q&A Chatbot.

## 🎯 What is OpenRouter?

OpenRouter is a platform that provides access to multiple AI models through a single API, including many **free models** that you can use without paying anything.

## 🆓 Available Free Models

### **GPT Models**
- `openai/gpt-3.5-turbo` - OpenAI's GPT-3.5 Turbo (recommended)
- `openai/gpt-3.5-turbo-16k` - GPT-3.5 with larger context

### **Meta Llama Models**
- `meta-llama/llama-2-7b-chat` - Llama 2 7B Chat model
- `meta-llama/llama-2-13b-chat` - Llama 2 13B Chat model

### **Google Models**
- `google/palm-2-chat-bison` - Google's PaLM 2 Chat model

### **Anthropic Models**
- `anthropic/claude-instant-v1` - Claude Instant (faster, cheaper)

### **Microsoft Models**
- `microsoft/dialo-gpt-medium` - Microsoft's DialoGPT Medium
- `microsoft/dialo-gpt-large` - Microsoft's DialoGPT Large

## 🚀 Setup Steps

### **Step 1: Create OpenRouter Account**

1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Click "Sign Up" or "Get Started"
3. Create an account (you can use GitHub, Google, or email)
4. Verify your email address

### **Step 2: Get Your API Key**

1. After logging in, go to your [API Keys page](https://openrouter.ai/keys)
2. Click "Create Key"
3. Give your key a name (e.g., "GIKI Chatbot")
4. Copy the generated API key (it starts with `sk-or-`)

### **Step 3: Configure Your Environment**

1. Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```

2. Edit the `.env` file and add your OpenRouter API key:
   ```bash
   # OpenRouter API Configuration (Free models available)
   OPENROUTER_API_KEY=sk-or-your-api-key-here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_MODEL=openai/gpt-3.5-turbo
   ```

### **Step 4: Test the Setup**

1. Run the test script:
   ```bash
   python test_system.py
   ```

2. You should see "✅ Available LLM providers: ['openrouter']" in the output

### **Step 5: Start the Application**

```bash
streamlit run app.py
```

## 🎮 Using OpenRouter in the App

### **Model Selection**
1. Start the application
2. In the sidebar, you'll see "🤖 AI Model Settings"
3. Select "Openrouter" as the AI Provider
4. Choose from the available free models
5. Click "🔄 Switch Model" to change models

### **Recommended Models for GIKI Chatbot**

| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `openai/gpt-3.5-turbo` | General use | Fast | High |
| `meta-llama/llama-2-13b-chat` | Detailed answers | Medium | Very High |
| `anthropic/claude-instant-v1` | Quick responses | Very Fast | Good |
| `google/palm-2-chat-bison` | Creative answers | Fast | High |

## 💰 Free Tier Limits

OpenRouter provides generous free credits:
- **$5 worth of free credits** when you sign up
- **$0.50 worth of free credits** every month
- **No credit card required** for free tier

### **Cost Comparison (per 1M tokens)**
- GPT-3.5 Turbo: ~$0.50
- Llama 2 7B: ~$0.20
- Claude Instant: ~$0.15
- PaLM 2: ~$0.10

## 🔧 Troubleshooting

### **"No LLM provider available"**
- Check that your OpenRouter API key is correct
- Make sure the key starts with `sk-or-`
- Verify the key is active in your OpenRouter dashboard

### **"API error" responses**
- Check your internet connection
- Verify the model name is correct
- Check if you have enough credits remaining

### **Slow responses**
- Try a faster model like `claude-instant-v1`
- Check your internet speed
- Some models are naturally slower than others

### **Model not working**
- Try switching to a different model
- Check the OpenRouter status page
- Some models may be temporarily unavailable

## 🎯 Example Questions to Test

Once you have OpenRouter set up, try these questions with your GIKI documents:

1. "What are the admission requirements for Computer Science?"
2. "How much is the tuition fee for undergraduate programs?"
3. "What are the academic rules for attendance?"
4. "Tell me about the student housing facilities"
5. "What are the graduation requirements?"

## 🔄 Switching Between Models

You can easily switch between different models:

1. **In the sidebar**, select "Openrouter" as the provider
2. **Choose a model** from the dropdown
3. **Click "🔄 Switch Model"**
4. **Ask a question** to test the new model

## 📊 Monitoring Usage

1. Go to your [OpenRouter dashboard](https://openrouter.ai/account)
2. Check your usage and remaining credits
3. View your API call history
4. Monitor costs and usage patterns

## 🆘 Getting Help

- **OpenRouter Documentation**: [docs.openrouter.ai](https://docs.openrouter.ai)
- **OpenRouter Discord**: [discord.gg/openrouter](https://discord.gg/openrouter)
- **OpenRouter Status**: [status.openrouter.ai](https://status.openrouter.ai)

## 🎉 You're Ready!

With OpenRouter set up, you now have access to multiple free AI models for your GIKI Prospectus Q&A Chatbot. The system will automatically use OpenRouter when configured, and you can switch between different models to find the one that works best for your needs.

**Happy chatting with your GIKI documents! 🎓**
