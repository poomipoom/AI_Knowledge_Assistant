from sqlalchemy.orm import Session as DBSession
from groq import AsyncGroq
from app.core.config import get_settings
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import retrieve_documents, TOOLS_SCHEMA
from app.db.models import ChatMessage
import json

settings = get_settings()
groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def run_agent_loop(db: DBSession, session_id: str, user_query: str):
    """
    Simple ReAct-like reasoning loop.
    """
    
    # 1. Get Chat History (limit to last 10 messages)
    history = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.desc()).limit(10).all()
    history.reverse() # Oldest first
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        # Ignore the very last one if it matches the current user_query just to avoid duplication,
        # but since it's already saved by chat_svc, we just use the history as is.
        messages.append({"role": msg.role.value, "content": msg.content})
        
    # 2. Call LLM with Tools
    response = await groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    citations = []
    
    # 3. Handle Tool Calls
    if response_message.tool_calls:
        # Add assistant message with tool calls to history
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "retrieve_documents":
                args = json.loads(tool_call.function.arguments)
                tool_result = await retrieve_documents(db, session_id, args["query"])
                
                # Extract citations
                try:
                    results_list = json.loads(tool_result)
                    for r in results_list:
                        citations.append({
                            "document_name": r["document_name"],
                            "content": r["content"]
                        })
                except:
                    pass
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
                
        # 4. Call LLM again to get final answer
        final_response = await groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages
        )
        final_text = final_response.choices[0].message.content
        return {
            "content": final_text,
            "citations": citations
        }
        
    # If no tool calls
    return {
        "content": response_message.content,
        "citations": []
    }
