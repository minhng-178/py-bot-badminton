import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
import asyncio
from typing import Optional
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


# Load environment variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("Lỗi: Không tìm thấy DISCORD_TOKEN. Tạo file .env với DISCORD_TOKEN=token_của_bạn và khởi động lại bot.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('HDBadminton')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Emoji mapping for polls (supports up to 10 options)
POLL_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

# Admin check decorator
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_messages
    return commands.check(predicate)

# Error handler
async def handle_error(ctx, error, command_name):
    """Xử lý lỗi tập trung"""
    logger.error(f"Lỗi trong lệnh {command_name}: {error}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bạn không có quyền sử dụng lệnh này.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Tham số không hợp lệ. Vui lòng kiểm tra cú pháp lệnh.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Thiếu tham số bắt buộc cho lệnh `{command_name}`.")
    else:
        await ctx.send(f"❌ Đã xảy ra lỗi khi thực hiện lệnh: {str(error)}")

# Bot events
@bot.event
async def on_ready():
    logger.info(f'Bot HDBadminton đã đăng nhập với tên {bot.user.name} (ID: {bot.user.id})') # type: ignore
    print(f'✅ Bot HDBadminton đã sẵn sàng! Đăng nhập với tên {bot.user.name}') # type: ignore
    
    # Đặt trạng thái bot
    activity = discord.Activity(type=discord.ActivityType.watching, name="các trận cầu lông 🏸")
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore command not found errors
    
    await handle_error(ctx, error, ctx.command.name if ctx.command else "unknown")

@bot.event
async def on_message(message):
    """Ghi log tin nhắn và xử lý lệnh"""
    if message.author == bot.user:
        return
    
    # Ghi log hoạt động tin nhắn
    logger.info(f"Tin nhắn từ {message.author} trong #{message.channel}: {message.content[:100]}...")
    
    await bot.process_commands(message)

# Commands
@bot.command(name='announce', aliases=['thongbao'], help='Đăng thông báo (Chỉ Admin)')
@is_admin()
async def announce(ctx, *, message: str):
    """
    Tạo thông báo với định dạng đặc biệt
    Cách dùng: !announce Nội dung thông báo của bạn ở đây
    """
    try:
        # Xóa tin nhắn lệnh
        await ctx.message.delete()
        
        # Tạo embed thông báo
        embed = discord.Embed(
            title="📢 Thông Báo HDBadminton",
            description=message,
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Thông báo bởi {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        # Gửi thông báo
        announcement_msg = await ctx.send("@everyone", embed=embed)
        
        # Thêm phản ứng xác nhận
        await announcement_msg.add_reaction('✅')
        
        logger.info(f"Thông báo được đăng bởi {ctx.author} trong #{ctx.channel}")
        
    except Exception as e:
        await handle_error(ctx, e, "announce")

@bot.command(name='vote', aliases=['poll', 'binhchon'], help='Tạo cuộc bình chọn với nhiều lựa chọn')
async def vote(ctx, title: str, description: Optional[str] = None, *options):
    """
    Tạo cuộc bình chọn với phản ứng emoji (Phiên bản nâng cao cho HDBadminton)
    Cách dùng: !vote "Tiêu đề" "Mô tả (tùy chọn)" "Lựa chọn 1" "Lựa chọn 2" "Lựa chọn 3"
    """
    try:
        # Nếu chỉ có 2 tham số, coi tham số thứ 2 là lựa chọn đầu tiên
        if description and len(options) == 0:
            options = (description,)
            description = None
        elif description and len(options) >= 1:
            options = (description,) + options
            description = None
        
        if len(options) < 2:
            await ctx.send("❌ Bạn cần ít nhất 2 lựa chọn cho cuộc bình chọn!")
            return
        
        if len(options) > 10:
            await ctx.send("❌ Tối đa 10 lựa chọn được phép!")
            return
        
        # Xóa tin nhắn lệnh
        await ctx.message.delete()
        
        # Tạo embed bình chọn với phong cách tiếng Việt
        embed = discord.Embed(
            title=f"🗳️ {title}",
            color=0x3498db,
            timestamp=datetime.utcnow()
        )
        
        # Thêm mô tả nếu có
        if description:
            embed.add_field(name="📋 Thông tin:", value=description, inline=False)
        
        # Thêm các lựa chọn vào embed
        option_text = ""
        for i, option in enumerate(options):
            option_text += f"{POLL_EMOJIS[i]} {option}\n"
        
        embed.add_field(name="🏸 Các lựa chọn:", value=option_text, inline=False)
        embed.add_field(name="ℹ️ Hướng dẫn:", value="Nhấn vào emoji tương ứng để bình chọn!", inline=False)
        
        embed.set_footer(
            text=f"Cuộc bình chọn được tạo bởi {ctx.author.display_name} • #HDBadminton", 
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        # Gửi tin nhắn bình chọn
        poll_msg = await ctx.send(embed=embed)
        
        # Thêm emoji phản ứng
        for i in range(len(options)):
            await poll_msg.add_reaction(POLL_EMOJIS[i])
        
        logger.info(f"Cuộc bình chọn được tạo bởi {ctx.author} trong #{ctx.channel}: {title}")
        
    except Exception as e:
        await handle_error(ctx, e, "vote")

@bot.command(name='votetime', aliases=['votegio', 'binhchongio'], help='Tạo bình chọn khung giờ tập (Chỉ Admin)')
@is_admin()
async def vote_time(ctx, month: str, *time_options):
    """
    Tạo cuộc bình chọn khung giờ tập cầu lông
    Cách dùng: !votetime "Tháng 9" "8h00-10h00" "15h00-17h00"
    """
    try:
        if len(time_options) < 2:
            await ctx.send("❌ Cần ít nhất 2 khung giờ để bình chọn!")
            return
        
        if len(time_options) > 10:
            await ctx.send("❌ Tối đa 10 khung giờ được phép!")
            return
        
        # Xóa tin nhắn lệnh
        await ctx.message.delete()
        
        # Tạo embed bình chọn chi tiết
        embed = discord.Embed(
            title=f"🏸 BẦU CHỌN KHUNG GIỜ TẬP - {month.upper()}",
            description="Vì thuê sân trong tháng này luôn nên sân sẽ hạn chế hơn. C các thành viên vui lòng bình chọn khung giờ phù hợp nhất.",
            color=0xe74c3c,
            timestamp=datetime.utcnow()
        )
        
        # Thêm các khung giờ
        option_text = ""
        for i, time_slot in enumerate(time_options):
            option_text += f"{POLL_EMOJIS[i]} **Thứ 7 - {time_slot}**\n"
        
        embed.add_field(name="⏰ Các khung giờ:", value=option_text, inline=False)
        embed.add_field(name="📍 Địa điểm:", value="Sân Hoàng Hoa Thám", inline=True)
        embed.add_field(name="📅 Thời gian:", value="Thứ 7 hàng tuần", inline=True)
        
        embed.add_field(
            name="📝 Ghi chú:", 
            value="Tháng sau sẽ cố gắng mở rộng khung giờ cho các thành viên có thể cân đối thời gian cá nhân để vote ạ.\n\nCảm ơn mọi người đã tham gia bình chọn và đồng hành cùng CLB!", 
            inline=False
        )
        
        embed.set_footer(text="#HDBadminton #VoteLịchTập")
        
        # Gửi cuộc bình chọn
        poll_msg = await ctx.send("@everyone", embed=embed)
        
        # Thêm phản ứng
        for i in range(len(time_options)):
            await poll_msg.add_reaction(POLL_EMOJIS[i])
        
        logger.info(f"Bình chọn khung giờ được tạo bởi {ctx.author} cho {month}")
        
    except Exception as e:
        await handle_error(ctx, e, "votetime")

@bot.command(name='delete', aliases=['del', 'xoa'], help='Xóa tin nhắn theo ID (Chỉ Admin)')
@is_admin()
async def delete_message(ctx, message_id: int):
    """
    Xóa tin nhắn theo ID
    Cách dùng: !delete 123456789012345678
    """
    try:
        # Thử lấy và xóa tin nhắn
        message = await ctx.channel.fetch_message(message_id)
        await message.delete()
        
        # Gửi xác nhận và tự động xóa
        confirmation = await ctx.send(f"✅ Tin nhắn đã được xóa thành công!")
        await asyncio.sleep(3)
        await confirmation.delete()
        
        # Xóa tin nhắn lệnh
        await ctx.message.delete()
        
        logger.info(f"Tin nhắn {message_id} đã được xóa bởi {ctx.author} trong #{ctx.channel}")
        
    except discord.NotFound:
        await ctx.send("❌ Không tìm thấy tin nhắn! Hãy đảm bảo ID tin nhắn đúng và trong kênh này.")
    except discord.Forbidden:
        await ctx.send("❌ Bot không có quyền xóa tin nhắn đó!")
    except Exception as e:
        await handle_error(ctx, e, "delete")

@bot.command(name='help', aliases=['trogiup', 'huongdan'], help='Hiển thị các lệnh có sẵn')
async def help_command(ctx):
    """
    Hiển thị thông tin trợ giúp cho các lệnh có sẵn
    """
    try:
        embed = discord.Embed(
            title="🏸 Lệnh Bot HDBadminton",
            description="Đây là các lệnh có sẵn:",
            color=0xe74c3c
        )
        
        # Lệnh công khai
        embed.add_field(
            name="📋 Lệnh Chung",
            value="• `!help` hoặc `!trogiup` - Hiển thị tin nhắn trợ giúp này\n• `!vote \"câu hỏi\" \"lựa chọn 1\" \"lựa chọn 2\"` - Tạo cuộc bình chọn\n• `!status` - Kiểm tra trạng thái bot",
            inline=False
        )
        
        # Lệnh admin (chỉ hiển thị nếu người dùng là admin)
        if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_messages:
            embed.add_field(
                name="🔒 Lệnh Admin",
                value="• `!announce <tin nhắn>` hoặc `!thongbao` - Đăng thông báo\n• `!votetime \"tháng\" \"giờ 1\" \"giờ 2\"` - Tạo bình chọn khung giờ\n• `!delete <id tin nhắn>` hoặc `!xoa` - Xóa tin nhắn theo ID",
                inline=False
            )
        
        embed.add_field(
            name="ℹ️ Mẹo",
            value="• Sử dụng dấu ngoặc kép cho các từ nhiều từ\n• ID tin nhắn có thể được sao chép bằng cách nhấp chuột phải (cần bật Developer Mode)\n• Sử dụng `!votetime` để tạo bình chọn khung giờ tập chuyên biệt",
            inline=False
        )
        
        embed.set_footer(text="HDBadminton Bot | Quản lý hoạt động câu lạc bộ cầu lông của bạn")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await handle_error(ctx, e, "help")

@bot.command(name='status', aliases=['trangthai'], help='Kiểm tra trạng thái bot và thống kê')
async def status(ctx):
    """
    Hiển thị trạng thái bot và thống kê cơ bản
    """
    try:
        embed = discord.Embed(
            title="🤖 Trạng Thái Bot",
            color=0x2ecc71,
            timestamp=datetime.utcnow()
        )
        
        # Thông tin bot
        embed.add_field(name="Tên Bot", value=bot.user.name, inline=True) # type: ignore
        embed.add_field(name="Máy chủ", value=len(bot.guilds), inline=True)
        embed.add_field(name="Người dùng", value=len(set(bot.get_all_members())), inline=True)
        embed.add_field(name="Tiền tố lệnh", value=bot.command_prefix, inline=True)
        embed.add_field(name="Độ trễ", value=f"{round(bot.latency * 1000)}ms", inline=True)
        
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None) # type: ignore
        embed.set_footer(text="Trạng thái đã được kiểm tra")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await handle_error(ctx, e, "status")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'HDBadminton Bot is running!')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        return  # Suppress HTTP logs

def run_web_server():
    """Run a simple web server to keep Render service alive"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Web server đang chạy trên cổng {port}")
    server.serve_forever()

# Run the bot
if __name__ == "__main__":
    try:
        # Start web server in background thread for Render
        if os.environ.get('RENDER'):
            logger.info("Khởi động web server cho Render...")
            web_thread = threading.Thread(target=run_web_server, daemon=True)
            web_thread.start()
        
        logger.info("🏸 Đang khởi động HDBadminton Bot...")
        bot.run(token, log_handler=None, log_level=logging.INFO)
    except KeyboardInterrupt:
        logger.info("Người dùng yêu cầu tắt bot")
    except Exception as e:
        logger.error(f"Bot bị lỗi: {e}")
        sys.exit(1)