
import os
from dotenv import load_dotenv
 
config_list = [
        # Azure OpenAI deployments
        {
            "model": os.getenv("GPT4o_DEPLOYMENT_NAME"), 
            "tags": ["gpt-4o", "azure", "OpenAI", "big"], # autogen tags for filtering if multiple models are specified
            "api_key": os.getenv("AZURE_API_KEY"), 
            "base_url": os.getenv("AZURE_DEPLOYMENT_ENDPOINT"), 
            "api_type": "azure", 
            "api_version": "2023-03-15-preview", # API VERSION != MODEL VERSION!!!!! Get from deployment targt in Azure AI Studio
            "temperature": 0.2,
        },        
        {
            "model": os.getenv("GPT4omini_DEPLOYMENT_NAME"), 
            "tags": ["gpt-4o-mini", "azure", "OpenAI", "medium"], # autogen tags for filtering if multiple models are specified
            "api_key": os.getenv("AZURE_API_KEY"), 
            "base_url": os.getenv("AZURE_DEPLOYMENT_ENDPOINT"), 
            "api_type": "azure", 
            "api_version": "2023-03-15-preview", # API VERSION != MODEL VERSION!!!!! Get from deployment targt in Azure AI Studio
            "temperature": 0.2,
        },
        # Groq deployments
        {   
            "model": "llama-3.1-70b-versatile",
            "tags": ["Llama-3.1-70b", "groq", "Meta", "medium"],
            "api_key": os.getenv("GROQ_API_KEY"),
            "api_type": "groq",
            #"frequency_penalty": 0.5,
            #"max_tokens": 2048,
            #"presence_penalty": 0.2,
            #"seed": 42,
            "temperature": 0.2,
            #"top_p": 0.2
        },
        {   
            "model": "llama-3.1-8b-instant",
            "tags": ["Llama-3.1-8b", "groq", "Meta", "small"],
            "api_key": os.getenv("GROQ_API_KEY"),
            "api_type": "groq",
            #"frequency_penalty": 0.5,
            #"max_tokens": 2048,
            #"presence_penalty": 0.2,
            #"seed": 42,
            "temperature": 0.2,
            #"top_p": 0.2
        },
        # Anthropic deployments
        {
            "model": "claude-3-5-sonnet-latest",
            "tags": ["Claude-3.5-Sonnet", "Sonnet", "Anthropic", "medium"],
            "api_key": os.getenv("ANTHROPIC_API_KEY"), 
            "api_type": "anthropic",
            "temperature": 0.2,
            #"top_p": 0.2, # Note: It is recommended to set temperature or top_p but not both.
            #"max_tokens": 2048,
        },
        {
            "model": "claude-3-haiku-20240307",
            "tags": ["Claude-3.0-Haiku", "Haiku", "Anthropic", "small"],
            "api_key": os.getenv("ANTHROPIC_API_KEY"), 
            "api_type": "anthropic",
            "temperature": 0.2,
            #"top_p": 0.2, # Note: It is recommended to set temperature or top_p but not both.
            #"max_tokens": 2048,
        },
        {
            "model": "claude-3-5-haiku-latest",
            "tags": ["Claude-3.5-Haiku", "Haiku", "Anthropic", "small"],
            "api_key": os.getenv("ANTHROPIC_API_KEY"), 
            "api_type": "anthropic",
            "temperature": 0.2,
            #"top_p": 0.2, # Note: It is recommended to set temperature or top_p but not both.
            #"max_tokens": 2048,
        },        



    ]