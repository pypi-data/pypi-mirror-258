# 封装功能

- 发送文本
- 发送图片/文件/音频/视频/其他

# 使用示例

```python
import worktool

with worktool.Worktool("your_robot_id") as bot:
        bot.send_file(
            ["群1", "好友1"],
            "文件名.jpg",
            "https://your_image_url.jpg",
            bot.FileType.IMAGE
        )
        bot.send_text(
            ["好友1"],
            "Hello world!"
        )
        bot.send_text(
            ["群1"],
            "Hello world!",
            ["@所有人"]
        )

```