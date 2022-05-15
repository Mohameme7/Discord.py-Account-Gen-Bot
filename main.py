import datetime
import json
import discord
from discord.ext import commands
import random
import os.path
from os import path
import requests
import re


config = json.load(open('config.json'))
token = config.get('Discord Token')
prefix = config.get('Command Prefix')

bot = commands.Bot(command_prefix=prefix ,    case_insensitive=True,  help_command=None)
bot.remove_command("help")
@bot.command(description=f"Usage: `{prefix}setnotifchannel (#channel)`, Sets a channel for bot launch notifications, if used like this `{prefix}setnotifchannel` it sets it to none")
@commands.has_permissions(administrator=True)
async def setnotifchannel(ctx, channel: discord.TextChannel = None):
    if channel == None:
        try:
            with open("logchannel.json", 'r') as f:
                cfg = json.loads(f.read())
                cfg.pop(str(ctx.guild.id))
                json.dump(cfg, open("logchannel.json", 'w'))
                await ctx.message.reply(f"Successfully Reset the logchannel by {ctx.author}")
        except:
            await ctx.message.reply("There's no channel set already")

    else:

     with open("logchannel.json", "r") as f:
        cfg = json.load(f)

     cfg[str(ctx.guild.id)] = channel.id
     with open("logchannel.json", "w") as f:
        json.dump(cfg, f, indent=4)
        embed = discord.Embed(title="Success",
                              description=f"Successfully set the notification channel to {channel.mention}!",
                              colour=discord.Colour.random())
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.message.reply(embed=embed)



@bot.command(invoke_without_command=True)
async def help(ctx, commandname = None):
  if commandname is None:
    em = discord.Embed(title="Help Command", description= "List of commands you can use with the bot, type !help [command] for more info about the command", colour = discord.Colour.random())
    em.add_field(name= "User Commands", value= f"`{prefix}gen`\n `{prefix}stock`\n `{prefix}ping`\n `{prefix}embed`")
    em.add_field(name= "Admin Commands", value= f"`{prefix}setnotifchannel` \n `{prefix}clearstock`\n `{prefix}newcategory`\n `{prefix}removecategory`\n `{prefix}restock`")
    em.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
    await ctx.send(embed = em)
  elif commandname is not None:
      try:
          cmd = bot.get_command(commandname)
          embed = discord.Embed(title = f'{prefix}{commandname}', description = f'{cmd.description}', colour = discord.Colour.random())
          embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
          await ctx.send(embed=embed)
      except:
          await ctx.send("this command does not exist, type help for more commands")

@bot.event
async def on_ready():
  try:
    with open('logchannel.json', 'r') as f:
        cfg = json.load(f)
        for guild in cfg:
         logch = cfg[guild]
         onlnch = bot.get_channel(int(logch))
         today = datetime.datetime.now()
         date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
         await onlnch.send(f"Back online, {date_time}")
  except:
      print("No notification channel set")


@bot.command(description = "Sends a embedded message with the author name on it as well.")
async def embed(ctx, message):
    embed = discord.Embed(title= f'Message sent by {ctx.author}', description = message, colour= discord.Colour.random())
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
    await ctx.send(embed=embed)


@bot.command(description=f"Usage: `{prefix}newcategory (typename)`, Makes a new account Category")
@commands.has_permissions(administrator= True)
async def newcategory(ctx, categoryname):
    if path.exists(categoryname + ".txt"):
        embed1 = discord.Embed(title = "Error!", description= f"Error, {categoryname} Already exists!", colour = 0xe74c3c)
        embed1.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.send(embed = embed1)
    else:
     with open(categoryname + ".txt" , 'w+') as f:
         embed = discord.Embed(title="Successfully Added!", description=f"New category created successfully!",  colour=0x2ecc71)
         embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
         await ctx.send(embed=embed)

@bot.command(description = f"Usage: {prefix} `A TXT File with accounts in`, Restocks a existing category")
@commands.has_permissions(administrator= True)
async def restock(ctx, category):
   try:
    attachment_url = ctx.message.attachments[0].url
    swallo = requests.get(attachment_url)
    poggywoggy = swallo.content
    poggywoggy.decode('utf-8')
    poggywoggy_2 = poggywoggy
    with open(f'{category}.txt', 'ab') as f:
        f.write(poggywoggy_2)
        await ctx.send(f"Added the {category} accounts to the stock successfully!")
   except:
       await ctx.send(f"Please make sure to add accounts to a existing category!")

@bot.command(description = f"Usage : {prefix}gen , Allows you to generate a account from a existing type")
@commands.cooldown(1, 120, commands.BucketType.user)
async def gen(ctx, type):
    try:
      with open(type + ".txt", "r") as f:
          accs = f.readlines()
          accountsend = random.choice(accs)
          PATTERN = "[:]"
          email,password = re.split(PATTERN, accountsend, maxsplit=1)
          embed = discord.Embed(title=f"{type.capitalize()} Account", description="", colour = discord.Colour.random())
          embed.add_field(name = "Email", value = email)
          embed.add_field(name=chr(173), value=chr(173))
          embed.add_field(name="password", value=password)
          embed.add_field(name="Combo", value=accountsend)
          embed.add_field(name=chr(173), value=chr(173))
          embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
          await ctx.author.send(embed=embed)
      with open(type + ".txt", "w+") as f:
          accs.remove(accountsend)
          f.write(''.join(accs))
          em = discord.Embed(title = f'Successfully Generated!', description= f"{ctx.author.mention} I have Sent the {type} Account to your DM", colour = discord.Colour.random())
          em.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
          await ctx.send(embed=em)
          await ctx.message.delete()
    except:
        embid = discord.Embed(title = f"Error! {type} is Out Of Stock!", description = "", colour = discord.Colour.random())
        embid.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.send(embed=embid)


@bot.command(description=f"Usage: `{prefix}removecategory (typename)`, Removes a account Category")
@commands.has_permissions(administrator= True)
async def removecategory(ctx, type):
    if os.path.exists(f'{type}.txt'):
        os.remove(f'{type}.txt')
        embed = discord.Embed(title = "Deleted Category", description= f"Successfully Deleted {type} Category!", colour = 0x2ecc71)
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Critical Error!", description=f"Category {type} does not exist!!", colour= 0xe74c3c)
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.send(embed=embed)

@bot.command(description=f"Usage: `{prefix}clearstock (type)`, Clears all the stock in a account type")
@commands.has_permissions(administrator= True)
async def clearstock(ctx, type):
    with open(f'{type}.txt', 'w+') as f:
        if type != -124432432:
         f.truncate(0)
         embed = discord.Embed(title = "Cleared Accounts!", description= f"Removed all the accounts in {type}!", colour = 0x2ecc71)
         embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
         await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Error!", description=f"{type }Category Does not exist!", colour= 0xe74c3c)
            embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
            await ctx.send(embed=embed)


@bot.command(description=f"Usage: `{prefix}ping`, Shows the Bot Latency.")
async def ping(ctx):
    await ctx.send(f'The bot ping is {round(bot.latency*1000)}ms')


@bot.command(description=f"Usage:`{prefix}stock`, Shows the current stock.")
async def stock(ctx):
    try:
     global service
     services = [""]
     stocklist = []

     for service in services:
        if os.path.exists(f"{service}.txt"):
            stocklist.append(f"{service} stock: {len(open(f'{service}.txt', 'r').readlines())} accounts")
        else:
            print("Error! a service that you added in services does not exist ! make sure to double check and remove non existing services")
     embed = discord.Embed(title="gen stock ", description="shows stock tf will it show", colour= discord.Colour.random())
     embed.add_field(name="Stock", value=  "\n".join(stocklist))
     embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
     await ctx.send(embed=embed)
    except:
        embid = discord.Embed(title="Gen Stock", description="Shows The stock for the current account types in the gen.", colour = discord.Colour.random())
        embid.add_field(name= "Stock", value= "No Account Types in the bot, type !help to start setting up the bot if you are a admin")
        embid.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.send(embed=embid)

@gen.error
async def on_cooldown(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"Command On Cooldown!",description=f"You can use this command again in {error.retry_after:.2f}s.", colour= 0xe74c3c)
            embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
            await ctx.send(embed=embed)
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Error!", description = f"Command not found! Type {prefix}help for a list of commands you can use!", colour = 0xe74c3c)
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.message.reply(embed=embed)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Error!", description = "You do not have permissions to use this command!", colour = 0xe74c3c)
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.message.reply(embed=embed)
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "Error!", description = "Please fill all required arguments for this command!", colour = 0xe74c3c)
        embed.set_footer(text="Made by Mohameme7#0023 https://discord.gg/eTTjQbzGTe")
        await ctx.message.reply(embed=embed)


bot.run(token)
