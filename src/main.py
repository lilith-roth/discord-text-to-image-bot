import os
import uuid
import discord

from PIL import Image, ImageFont, ImageDraw, ImageColor
from . import settings

proc_dir_name = os.path.split(os.path.abspath(__file__))[0]
font_filepath = os.path.join(proc_dir_name, "fonts/Tuffy.ttf")

def text_to_image(
        text: str,
        font_filepath: str,
        font_size: int,
        color: (int, int, int),
        font_align="center"
    ):
    font: ImageFont.FreeTypeFont = ImageFont.truetype(font_filepath, size=font_size)
    box = font.getsize_multiline(text)
    img = Image.new("RGBA", (box[0], box[1]))
    draw = ImageDraw.Draw(img)
    draw_point = (0, 0)
    draw.multiline_text(draw_point, text, font=font, fill=color, align=font_align)
    return img


class BotClient(discord.Client):
    async def on_ready(self):
        print(f'Running from {proc_dir_name}')
        print(f'Using font {font_filepath}')
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if not message.content.startswith('$imagetext'):
            return
        print(f'Message from {message.author}: {message.content}')
        output_image = text_to_image(
                message.content[10:],
                font_filepath,
                8,
                (255, 255, 255),
        )
        file_name = f'cache/{uuid.uuid4().hex}.png'
        save_path = os.path.join(proc_dir_name, file_name)
        output_image.save(save_path)
        await message.channel.send(file=discord.File(save_path))



def main():
    cache_dir = os.path.join(proc_dir_name, 'cache')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    intents = discord.Intents.default()
    intents.message_content = True
    client = BotClient(intents=intents)
    client.run(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    main()
