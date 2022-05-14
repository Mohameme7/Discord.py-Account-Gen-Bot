import datetime
import json
import discord
from discord.ext import commands
import random
import os.path
from os import path
import requests



config = json.load(open('config.json'))
token = config.get('Discord Token')
prefix = config.get('Command Prefix')

bot = commands.Bot(command_prefix=prefix ,    case_insensitive=True,  help_command=None)
bot.remove_command("help")
@bot.command()
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
        embed.set_footer(text="Made by Mohameme7#0023")
        await ctx.message.reply(embed=embed)



@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help Command", description= "List of commands you can use with the bot, type !help [command] for more info about the command")
    em.add_field(name= "User Commands", value= "`!gen` `!stock` `!ping`")
    em.add_field(name= "Admin Commands", value= "`!setnotifchannel` `!clearstock` `!newcategory` `!removecategory` `!restock`")
    await ctx.send(embed = em)

@help.command()
async def gen(ctx):
    em = discord.Embed(title= f"{prefix}gen", description=f"Usage: `{prefix}gen (AccountType)`, Sends a account to the user DMS, has a cooldown of 120 seconds")
    await ctx.send(embed=em)

@help.command()
async def stock(ctx):
    em = discord.Embed(title= f"{prefix}stock", description=f"Usage:`{prefix}stock`, Shows the current stock.")
    await ctx.send(embed=em)

@help.command()
async def ping(ctx):
    em = discord.Embed(title= f"{prefix}ping", description=f"Usage: `{prefix}ping`, Shows the Bot Latency.")
    await ctx.send(embed=em)


@help.command()
async def setnotifchannel(ctx):
    em = discord.Embed(title=f"`{prefix}setnotifchannel`", description=f"Usage: `{prefix}setnotifchannel (#channel)`, Sets a channel for bot launch notifications, if used like this `{prefix}setnotifchannel` it sets it to none")
    await ctx.send(embed=em)

@help.command()
async def clearstock(ctx):
    em = discord.Embed(title= f"{prefix}clearstock", description=f"Usage: `{prefix}clearstock (type)`, Clears all the stock in a account type")
    await ctx.send(embed=em)

@help.command()
async def newcategory(ctx):
    em = discord.Embed(title= f"{prefix}newcategory", description=f"Usage: `{prefix}newcategory (typename)`, Makes a new account Category")
    await ctx.send(embed=em)

@help.command()
async def removecategory(ctx):
    em = discord.Embed(title= f"{prefix}removecategory", description=f"Usage: `{prefix}removecategory (typename)`, Removes a account Category")
    await ctx.send(embed=em)
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





@bot.command()
@commands.has_permissions(administrator= True)
async def newcategory(ctx, categoryname):
    if path.exists(categoryname + ".txt"):
        embed1 = discord.Embed(title = "Error!", description= f"Error, {categoryname} Already exists!", colour = 0xe74c3c)
        await ctx.send(embed = embed1)
    else:
     with open(categoryname + ".txt" , 'w+') as f:
         embed = discord.Embed(title="Successfully Added!", description=f"New category created successfully!",  colour=0x2ecc71)
         await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator= True)
async def restock(ctx, category):
    attachment_url = ctx.message.attachments[0].url
    swallo = requests.get(attachment_url)
    poggywoggy = swallo.content
    poggywoggy.decode('utf-8')
    poggywoggy_2 = poggywoggy
    with open(f'{category}.txt', 'ab') as f:
        f.write(poggywoggy_2)
        await ctx.send(f"Added the {category} accounts to the stock successfully!")

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def gen(ctx, type):
      with open(type + ".txt", "r") as f:
          accs = f.readlines()
          accountsend = random.choice(accs)
          await ctx.author.send(accountsend)
      with open(type + ".txt", "w+") as f:
          accs.remove(accountsend)
          f.write(''.join(accs))
          await ctx.message.reply(f"Sent the {type} Account Successfully", delete_after=10)



@bot.command()
@commands.has_permissions(administrator= True)
async def removecategory(ctx, type):
    if os.path.exists(f'{type}.txt'):
        os.remove(f'{type}.txt')
        embed = discord.Embed(title = "Deleted Category", description= f"Successfully Deleted {type} Category!", colour = 0x2ecc71)
        embed.set_footer(text = "Made by Mohameme7#0023")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Critical Error!", description=f"Category {type} does not exist!!", colour= 0xe74c3c)
        embed.set_footer(text="Made by Mohameme7#0023")
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator= True)
async def clearstock(ctx, type):
    with open(f'{type}.txt', 'w+') as f:
        if type != -124432432:
         f.truncate(0)
         embed = discord.Embed(title = "Cleared Accounts!", description= f"Removed all the accounts in {type}!", colour = 0x2ecc71)
         embed.set_footer(text = "Made by Mohameme7#0023")
         await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Error!", description=f"{type }Category Does not exist!",
                                  colour= 0xe74c3c)
            embed.set_footer(text="Made by Mohameme7#0023")
            await ctx.send(embed=embed)



@bot.command()
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
     embed.set_footer(text="Made by Mohameme7#0023")
     await ctx.send(embed=embed)
    except:
        embid = discord.Embed(title="Gen Stock", description="Shows The stock for the current account types in the gen.")
        embid.add_field(name= "Stock", value= "No Account Types in the bot, type !help to start setting up the bot if you are a admin")
        await ctx.send(embed=embid)

@gen.error
async def on_cooldown(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{ctx} Command On Cooldown!",description=f"You can use this command again in {error.retry_after:.2f}s.", color= 0xe74c3c)
            embed.set_footer(text="Made by Mohameme7#0023")
            await ctx.send(embed=embed)
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid Commands, Use !help for a list of commands that you can use!")
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have perms to use this command!")
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Make sure to fill all required arguments!")

bot.run(token)
