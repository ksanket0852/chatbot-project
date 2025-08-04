import gradio as gr
import time
from chatbot import chat_with_groq
from config import UI  # Reuse values loaded in config.py

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def respond(history):
    # Construct prompt from history
    prompt = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in history if isinstance(msg, dict)
    )

    # Get assistant response
    bot_reply = chat_with_groq(prompt)

    # Stream response
    history.append({"role": "assistant", "content": ""})
    for character in bot_reply:
        history[-1]["content"] += character
        time.sleep(UI.get("streaming_delay_seconds", 0.02))
        yield history

def add_message(history, message):
    if message.strip():
        history.append({"role": "user", "content": message})
    return history, ""

def clear_chat():
    return [], ""

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown(UI["title"])
    gr.Markdown(UI["description"])

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        type="messages",
        height=UI.get("height", 500)
    )

    with gr.Row():
        chat_input = gr.Textbox(
            placeholder=UI["placeholder"],
            show_label=False,
            container=False,
            scale=8
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)
        clear_btn = gr.Button("Clear", variant="secondary", scale=1)

    chat_input.submit(
        add_message, [chatbot, chat_input], [chatbot, chat_input], queue=False
    ).then(
        respond, chatbot, chatbot, api_name="bot_response"
    )

    submit_btn.click(
        add_message, [chatbot, chat_input], [chatbot, chat_input], queue=False
    ).then(
        respond, chatbot, chatbot
    )

    clear_btn.click(clear_chat, inputs=None, outputs=[chatbot, chat_input])

    chatbot.like(print_like_dislike, None, None)

if __name__ == "__main__":
    demo.launch()
