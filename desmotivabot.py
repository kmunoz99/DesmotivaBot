import os
import platform
import carteles
import discord
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import requests
from discord.ext.commands import Bot



bot = Bot(command_prefix='!') 


TOKEN = os.getenv('TOKEN')
IMGPath = os.getenv('IMG_FOLDER')

def generarImagen(imagen, toptext,bottomText,id):
    W, H = (650,555)
    toptext = toptext
    bottomText= bottomText

    fnt = ImageFont.truetype(IMGPath+'/font.ttf', 45)
    fnt2 = ImageFont.truetype(IMGPath+'/font.ttf', 25)

    im1 = Image.open("/root/bot/background.png")

    r = requests.get(imagen, allow_redirects=True)
    open(IMGPath+id+".png", 'wb').write(r.content)
    #urllib.request.urlretrieve(imagen,id+".png")
    im2 = Image.open(IMGPath+id+".png")
    im2 = im2.resize((588,415))
    overlay = Image.open(IMGPath+"/overlay.png") #La cajita que pone desmotivaciones.es 

    im1.paste(im2, (31, 31))
    im1.paste(overlay, (0,0),overlay)


    d = ImageDraw.Draw(im1)
    #Top text
    w, h = d.textsize(toptext,font=fnt)
    d.text(((W-w)/2,460), toptext,font=fnt, fill="white")
    #bottom text
    w, h = d.textsize(bottomText,font=fnt2)
    d.text(((W-w)/2,500), bottomText,font=fnt2, fill="white")

    im1.save(IMGPath+id+"final.png", quality=100)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

@bot.command()
async def cartel(ctx):

    msg = ctx.message.content
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    x = msg.split(' ', 1)[1]
    x = x.split(";;;")

    try:
        url = message.attachments[0].url
        print(url)
        carteles.generarImagen(url, x[0],x[1], str(ctx.message.reference.message_id))
        imagen = discord.File(IMGPath+str(ctx.message.reference.message_id)+"final.png")
        await ctx.reply(file=imagen)
        os.remove(IMGPath+str(ctx.message.reference.message_id)+".png") 
        os.remove(IMGPath+str(ctx.message.reference.message_id)+"final.png") 
    except:
        await ctx.reply("No encuentro ninguna imagen")
bot.run(TOKEN)
