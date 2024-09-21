import os
import openai
import logging

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(user_input):
    try:
        logging.info(f"Sending request to OpenAI API: {user_input}")
        # OpenAI API v1.0.0以降の新しいエンドポイントを使用
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは有能なアシスタントです。"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        # 応答を取得
        answer = response.choices[0].message.content.strip()
        logging.info(f"Received response from OpenAI API: {answer}")
        return answer
    except Exception as e:
        logging.error(f"Error while communicating with OpenAI API: {e}", exc_info=True)
        raise e
