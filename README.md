# 🏸 HDBadminton Discord Bot

A Vietnamese Discord bot designed specifically for managing badminton club activities, including announcements, polls, and administrative tasks.

## ✨ Features

### 📋 General Commands

- **Vote System** - Create polls with reaction-based voting
- **Status Check** - View bot status and statistics
- **Help System** - Comprehensive command guide in Vietnamese

### 🔒 Admin Commands

- **Announcements** - Post formatted announcements with @everyone
- **Time Voting** - Specialized polls for practice time slots
- **Message Management** - Delete messages by ID
- **Enhanced Logging** - Track all bot activities

### 🇻🇳 Vietnamese Language Support

- Complete Vietnamese interface
- Localized error messages
- Vietnamese command aliases
- Badminton club specific terminology

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Discord Bot Token
- A Discord server with appropriate permissions

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/minhng-178/py-bot-badminton.git
cd py-bot-badminton
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup environment variables**

```bash
cp .env.example .env
# Edit .env and add your Discord bot token
```

4. **Run the bot**

```bash
python main.py
```

## 🎮 Commands

### General Commands

| Command                                | Aliases                 | Description             |
| -------------------------------------- | ----------------------- | ----------------------- |
| `!help`                                | `!trogiup`, `!huongdan` | Show available commands |
| `!vote "question" "option1" "option2"` | `!binhchon`             | Create a poll           |
| `!status`                              | `!trangthai`            | Check bot status        |

### Admin Commands (Requires Admin/Manage Messages permission)

| Command                             | Aliases                    | Description               |
| ----------------------------------- | -------------------------- | ------------------------- |
| `!announce <message>`               | `!thongbao`                | Post announcement         |
| `!votetime "month" "time1" "time2"` | `!votegio`, `!binhchongio` | Create practice time poll |
| `!delete <message_id>`              | `!xoa`, `!del`             | Delete message by ID      |

## 📝 Usage Examples

### Create a Practice Time Poll

```
!votetime "Tháng 10" "8h00 - 10h00" "15h00 - 17h00"
```

This creates a specialized poll for badminton practice times with:

- Professional formatting
- Location information (Hoàng Hoa Thám Court)
- Schedule details (Saturday weekly)
- Club hashtags (#HDBadminton #VoteLịchTập)

### Post an Announcement

```
!thongbao Tập luyện tuần này sẽ diễn ra vào thứ 7 từ 8h-10h tại sân Hoàng Hoa Thám!
```

### Create a General Poll

```
!binhchon "Chọn địa điểm tập tháng tới" "Sân Hoàng Hoa Thám" "Sân Cầu Giấy" "Sân Thanh Xuân"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### Bot Permissions

The bot requires the following Discord permissions:

- Send Messages
- Manage Messages
- Add Reactions
- Read Message History
- Use External Emojis
- Mention Everyone

## 📁 Project Structure

```
hd-badminton-bot/
├── main.py              # Main bot code
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── .env               # Your environment variables (create this)
├── discord.log        # Bot activity logs
└── README.md          # This file
```

## 🛡️ Features in Detail

### Enhanced Vote System

- Support for up to 10 options using emoji reactions
- Automatic emoji assignment (1️⃣ to 🔟)
- Rich embed formatting with Vietnamese labels
- Creator attribution and timestamps

### Admin-Only Commands

- Role-based permission system
- Administrator or "Manage Messages" permission required
- Automatic command cleanup for cleaner channels

### Comprehensive Logging

- All activities logged to `discord.log`
- Console and file output
- Error tracking and debugging support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the logs in `discord.log`
2. Ensure your bot token is correctly set in `.env`
3. Verify the bot has necessary permissions in your Discord server
4. Open an issue on GitHub

## 🏸 About HDBadminton

This bot was specifically designed for the HDBadminton club to streamline:

- Practice session scheduling
- Member communication
- Event coordination
- Administrative tasks

Built with ❤️ for the badminton community in Vietnam.
