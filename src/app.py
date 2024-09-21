import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from src.chatbot_engine import get_chatgpt_response

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)

# 環境変数からトークンを取得
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# アプリの初期化
app = App(token=SLACK_BOT_TOKEN)

# メンションイベントのハンドリング
@app.event("app_mention")
def handle_app_mention_events(event, say, context):
    user_message = event.get('text', '')
    logging.info(f"Received message: {user_message}")

    # ボットのユーザーIDを取得
    bot_user_id = context['bot_user_id']

    # ボットへのメンションを除去してメッセージを取得
    cleaned_message = user_message.replace(f"<@{bot_user_id}>", "").strip()

    # ChatGPTからの応答を取得
    try:
        response = get_chatgpt_response(cleaned_message)
        logging.info(f"ChatGPT response: {response}")
        say(response)
    except Exception as e:
        logging.error(f"Error: {e}")
        say("申し訳ありませんが、現在応答できません。")

# アプリの起動
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
