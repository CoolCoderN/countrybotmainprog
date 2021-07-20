from discord.ext import commands
from mongomethods import count, reading, update, update_prestige, update_war, writing, delete_task, search_name, update_coins, get_prefix

import discord, random
import asyncio


@commands.command()
async def dice(ctx, amount):
  try: 
    amount = int(amount) 
  except:
    await ctx.send(":x: That isn't a valid amount") 
    return
 
  if amount <= 0:
    await ctx.send(":x: That isnt a valid amount")
    return
  try:
    a = await reading(ctx.author.id)
  except:
    prefix = await get_prefix(id)
    embed = discord.Embed(title='Hey!', description=f":x: You don't have a country. Start a country with `{db[str(ctx.guild.id)]}start`")
    await ctx.channel.send(embed=embed)
    return
  if amount >= a[0][1]:
    await ctx.send(':x: You do not have that much population to bet')
    return
  else:
    user_dice1 = random.randint(1, 6)
    user_dice2 = random.randint(1, 6)
    await ctx.send(f'You rolled {user_dice1} and {user_dice2} :game_die:')
    await asyncio.sleep(1)
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    await ctx.send(f"I rolled {dice1} and {dice2} :game_die:")
    if (dice1 + dice2) < (user_dice1 + user_dice2):
      await ctx.send(':( I lost again! I WILL NEVER WIN! GG, ugh.')
      await ctx.send('<:angrycbot:863148860616212501> <:angrycbot:863148860616212501> <:angrycbot:863148860616212501>')
      await update((ctx.author.id, a[0][0], a[0][1] + amount, a[0][2], a[0][3], a[0][4], a[0][10]))
    elif (dice1 + dice2) == (user_dice1 + user_dice2):
      await ctx.send('<:Thinkingcbot:863151583294521344> Its a draw. so no one won')
      await ctx.send('<:sadcbot:863150212989845514> <:sadcbot:863150212989845514> <:sadcbot:863150212989845514>')
      
    else:
      await ctx.send('YES. I WON!!!! WOHOOOOOO :partying_face:')
      await ctx.send('<:laughcbot:863151389042933800> <:laughcbot:863151389042933800> <:laughcbot:863151389042933800>')
      await update((ctx.author.id, a[0][0], a[0][1] - amount, a[0][2], a[0][3], a[0][4], a[0][10]))


@dice.error
async def dice_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    prefix = await get_prefix(ctx.guild.id)
    embed = discord.Embed(title='Incorrect Usage', description=f'```Usage: {prefix}dice <amount>```')
    await ctx.channel.send(embed=embed)

@commands.command()
async def coinflip(ctx, *amount1):
  h_t = random.choice(['h', 't'])
  try:
    a = await reading(ctx.author.id)
  except:
    prefix = await get_prefix(id)
    embed = discord.Embed(title='Hey!', description=f":x: You don't have a country. Start a country with `{prefix}start`")
    await ctx.channel.send(embed=embed)
    return

  amount = []
  for i in amount1:
    amount.append(i)


  try:
    
    if amount[0].lower() not in ['heads', 'tails']:
      embed = discord.Embed(title='huh', description=':x: That is not a valid option. Specify either `heads` or `tails`')
      await ctx.channel.send(embed=embed)
      return

    else:
      pass

  except:
    embed = discord.Embed(title='Error', description=':x: You need to specify heads or tails!')
    await ctx.channel.send(embed=embed)
    return

  
  if len(amount) == 1:
    if a[0][1] <= 0:
      embed = discord.Embed(title='Hey!', description=":x: You don't have enough people to do this command")
      await ctx.channel.send(embed=embed)
      return
    
    if h_t == 'h':
      confirmed = 'heads'

    else:
      confirmed = 'tails'

    if confirmed == amount[0]:
      embed = discord.Embed(title='Woohooooo!!!', description=':tada: Your guess was correct!! You won `1` population!!!')

      await update((ctx.author.id, a[0][0], a[0][1] + 1, a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

    else:
      embed = discord.Embed(title=':(', description=':slight_frown: Your guess was incorrect. You lost `1` population')

      await update((ctx.author.id, a[0][0], a[0][1] - 1, a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

  else:
    
    try:
      amount[1] = int(amount[1])
    except:
      embed = discord.Embed(title='Error', description=':x: You have entered an invalid amount!')
      await ctx.send(embed=embed)
      return
    
    if amount[1] < 1:
      await ctx.send(":x: You can't bet with this amount smh")
      return


    if a[0][1] <= int(amount[1]):
      embed = discord.Embed(title='Hey!', description=":x: You don't have that much population to bet")
      await ctx.send(embed=embed)
      return
    
    if h_t == 'h':
      confirmed = 'heads'

    else:
      confirmed = 'tails'

    if confirmed == amount[0]:
      embed = discord.Embed(title='Woohooooo!!!', description=f':tada: Your guess was correct!! You won `{amount[1]}` population!!!')

      await update((ctx.author.id, a[0][0], a[0][1] + int(amount[1]), a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return

    else:
      embed = discord.Embed(title=':(', description=f':slight_frown: Your guess was incorrect. You lost `{amount[1]}` population')

      await update((ctx.author.id, a[0][0], a[0][1] - amount[1], a[0][2], a[0][3], a[0][4], a[0][10]))

      await ctx.channel.send(embed=embed)
      return


def setup(bot):
  bot.add_command(coinflip)
  bot.add_command(dice)