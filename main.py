import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
import discord
from discord.ext import commands
import io

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

@bot.command()
async def 展開予想(ctx):
    if not ctx.message.attachments:
        await ctx.send("画像を添付してください。")
        return
    
    await ctx.send("画像を処理中です...")

    image_bytes = await ctx.message.attachments[0].read()
    image = Image.open(io.BytesIO(image_bytes))
    model = genai.GenerativeModel("models/gemini-2.5-flash-preview-04-17")

    try:
        response = model.generate_content([
            build_vision_prompt(),
            image
        ])
        await ctx.send("展開予想:\n" + response.text)
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {str(e)}")

def build_vision_prompt():
    return """
    この画像は競輪の出走表です。

    選手のライン構成・脚質・競走得点・コメントなどをもとに、
    レース展開を予想してください。1〜3パターンの可能性を挙げてください。
    また、買う目を考えてください。
    
    以下の点を考慮してください：
    - どのラインが主導権を握りそうか（先行）
    - 捲りを狙う選手が誰か
    - 単騎選手が不気味な動きを見せる可能性
    - 番手や三番手から抜け出す選手
    - 番手が取れない選手の不利な展開 など

    出力は【展開予想①】【展開予想②】…と分けて、自然な日本語で書いてください。
    """

bot.run(os.getenv("DISCORD_TOKEN"))
