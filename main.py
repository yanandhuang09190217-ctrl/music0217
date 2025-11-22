import os
import discord
from discord.ext import commands
import wavelink

TOKEN = os.getenv("DISCORD_TOKEN")
LAVALINK_URL = os.getenv("LAVALINK_URL", "http://localhost:2333")
LAVALINK_PASS = os.getenv("LAVALINK_PASS", "youshallnotpass")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # connect to Lavalink node
    await wavelink.NodePool.create_node(bot=bot, host=LAVALINK_URL, port=2333, password=LAVALINK_PASS)
    print("Lavalink connected.")

@bot.command()
async def play(ctx):
    author = ctx.author

    # 1. 檢查成員是否在語音頻道
    if not author.voice:
        await ctx.send("⚠️ 你需要先加入語音頻道才能使用這個功能！")
        return

    # 2. Bot 連接語音頻道
    channel = author.voice.channel
    vc: wavelink.Player = ctx.voice_client

    if not vc:
        vc = await channel.connect(cls=wavelink.Player)

    # 3. 在文字頻道詢問網址
    ask_msg = await ctx.send("🎵 要播放的音樂網址是什麼呢？請在 60 秒內輸入～")

    # 等待使用者回覆
    def check(m):
        return m.author == author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        query = msg.content.strip()
        # 刪除提問與使用者回覆
        try:
            await ask_msg.delete()
            await msg.delete()
        except:
            pass
    except:
        await ctx.send("⏳ 超過 60 秒未輸入，播放取消。")
        return

    # 搜尋並播放
    track = await wavelink.YouTubeTrack.search(query=query, return_first=True)
    if not track:
        await ctx.send("❌ 找不到此音樂，請確認網址或改用關鍵字搜尋。")
        return

    await vc.play(track)
    await ctx.send(f"▶ 正在播放：**{track.title}**")

    # 私訊通知成功播放
    try:
        await author.send(f"🎧 已成功開始播放音樂：**{track.title}**")
    except:
        await ctx.send("⚠️ 無法傳送私訊，但音樂已開始播放！")

bot.run(TOKEN)
