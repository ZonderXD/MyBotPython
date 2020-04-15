import discord
import asyncio
import datetime
import random as r
import random
import io
import os
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.utils import get

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'          [NebluxBot]')
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('Command help: .help'))
    print(f"[NebluxBot] Bot successfully launched!;")
    print(f"[NebluxBot] Name: [{bot.user}];")
    print(f'[NebluxBot] ID: [{bot.user.id}]')
    print('[------------------------------]')
    print(f'          [Other]')

@bot.event
async def is_owner(ctx):
    return ctx.author.id == 668325441224048641 # Айди создателя бота


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    ctx = message.content
    author = message.author
    channel = message.channel.name
    guild = message.guild.name
    print(" [Message]: {0}\n [Author]: {1}\n [Channel]: {2}\n [Guild]: {3}".format(ctx,author,channel,guild))
    print("[------------------------------]")
    print(f'          [Next]')

@bot.command()
async def updates(ctx):
	update_role = discord.utils.get(ctx.guild.roles, id = 695295305595224075)
	await ctx.author.add_roles( update_role )
	await ctx.send(embed = discord.Embed(description = f'**Вы успешно подписались на обновления!**', color=0x0c0c0c))

@bot.command()
async def un_updates(ctx):
	update_role = discord.utils.get(ctx.guild.roles, id = 695295305595224075)
	await ctx.author.remove_roles( update_role )
	await ctx.send(embed = discord.Embed(description = f'**Вы успешно отписались от обновлений!**', color=0x0c0c0c))
@bot.event
async def on_member_join(member):
	await member.create_dm()

	await member.send(embed = discord.Embed(description = f'**<@{member.id}> Приветствую тебя на сервере `{member.guild.name}` ! Желаю тебе хорошо повеселится. И обязательно прочитай правила сервера!**', color=0xec33))

@bot.command()
@commands.check(is_owner)
async def members(ctx, role: discord.Role):
    data = "\n".join([i.mention for i in role.members])
    
    await ctx.send(embed = discord.Embed(description = f'{data}', color=0x0c0c0c))

@bot.command(aliases = ['level', 'profile', 'я', 'lvl', 'уровень', 'ранг', 'rank', 'card'])
async def __lvl_card(ctx):
	async with ctx.typing():

		url = str(ctx.author.avatar_url)[:-10]

		r = requests.get(url, stream = True)
		r = Image.open(io.BytesIO(r.content))
		r = r.convert('RGBA')
		r = r.resize((227, 227), Image.ANTIALIAS)

		image = Image.new("RGBA", (917, 374), (0, 0, 0, 0))
		image.paste(r, (29, 22, 256, 249))

		banner = Image.open('main_banner.png') #место куда мы сохранили баннер
		banner = banner.convert('RGBA')

		image.paste(banner, (0, 0, 917, 374), banner)

		idraw = ImageDraw.Draw(image)
		name = ctx.author.name
		tag = ctx.author.discriminator
 		
		font_50 = ImageFont.truetype("bahnschrift.ttf", size = 50)
		font_25 = ImageFont.truetype("bahnschrift.ttf", size = 25)

		idraw.text((294, 72), f'{name}#{tag}', font = font_50)
		idraw.text((294, 137), f'надпись "О себе"', font = font_25)
		idraw.text((120, 263), f'левел', font = font_25)
		idraw.text((104, 293), f'сколько хр осталось до следующего лвл', font = font_25)
		idraw.text((183, 322), f'баланс (в $)', font = font_25)
		idraw.text((639, 263), f'сколько годиков?', font = font_25)

		image.save('banners') #место, куда сохраняем картинку

		await ctx.send(file = discord.File(fp = 'main_banner.png')) #прикрепляем картинку

@bot.command()
@commands.check(is_owner)
async def spam(ctx, member: discord.Member = None, *, arg):
	if member is None: 
		await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите пользователя!**'))
	else:
		await member.create_dm()
		async def spam():
			while True:
				await member.send(embed = discord.Embed(description = f'**{arg}**', color=0x0c0c0c))

		await spam()

@bot.command()
async def password(ctx, lenght: int = None, number: int = None):

    if not lenght or not number:
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите длину пароля и количество символов в нем.', color=0x0c0c0c)) 

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for x in range(number):
        password = ''

        for i in range( lenght ):
            password += random.choice(chars)

        await ctx.author.send(embed = discord.Embed(description = f'**Сгенерированный пароль:\n{password}**', color=0x0c0c0c)) 
        await ctx.send(embed = discord.Embed(description = f'**Пароль успешно отправлен!**', color=0x0c0c0c))
        return

@bot.command()
async def help(ctx):
	emb = discord.Embed( title = 'Команды:', color=0x6fdb9e )

	emb.add_field(name='Информационные:', value='``.user`` - Узнать информацию о пользователе\n ``.role`` - Информация о роли\n ``.server`` - Узнать информацию о сервере', inline = False)
	emb.add_field(name='Администрация:', value='`.ban` - Бан пользователя\n `.kick` - Кикнуть пользователя\n `.mute` - Замутить пользователя\n `.unmute` - Размутить пользователя\n `.tempban` - Временный бан\n `tempmute` - Временный мут\n `.clear` - Очистить сообщения\n `.rename` - Поменять ник',inline = False)
	emb.add_field(name='Экономия:', value='``.work`` - Пойти на работу\n ``.bank`` - Проверить баланс',inline = False)
	emb.add_field(name='Разное:', value=' ``.avatar`` - Аватар пользоватлея\n ``.ping`` - Пинг бота\n ``.time`` - Узнать время\n ``.roles`` - Узнать сколько пользователей с ролью\n `.updates` - Подписаться на обновления\n `.un_updates` - Отписаться от обновлений',inline = False)
	emb.add_field(name='Весёлости:', value='``.ran_color`` - Рандомный цвет в формате HEX\n ``.coin`` - Бросить монетку\n ``.math`` - Решить пример\n `.8ball` - Волшебный шар\n `.password` - Рандомный',inline = False)
	emb.set_thumbnail(url=ctx.guild.icon_url)
	emb.set_footer(text='𝕯𝖆𝖗𝖐 𝕬𝖓𝖌𝖊𝖑#8992 © | Все права защищены', icon_url='https://cdn.discordapp.com/avatars/668325441224048641/8431275535fe40a8234d810db5646643.png?size=512')

	await ctx.send( embed = emb )

@bot.command()
@commands.check(is_owner)
async def send(ctx, member: discord.Member = None, *, arg): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: сообщение!**'))

    else:
        
        await member.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

@bot.command()
async def user(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

@bot.command()
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    emb = discord.Embed(
        title= 'Текущий пинг',
        description= f'{bot.ws.latency * 1000:.0f} ms'
    )
    await ctx.send(embed=emb)

@bot.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= bot.user.name, icon_url=bot.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb )

@bot.command()
async def ran_color(ctx):
    clr = (random.randint(0,16777215))
    emb = discord.Embed(
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``',
        colour= clr
    )

    await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions( administrator = True) 
async def tempban(ctx, member : discord.Member, time:int, arg:str, *, reason=None):
    if member == ctx.message.author:
        return await ctx.send("Ты не можешь забанить сам себя.")
    msgg =  f'Пользователь <@{member.id}> , забанен по причине {reason}.'
    msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине {reason}.'
    if reason == None:
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}.'
    if reason == None:
        msgg =  f'Пользователь <@{member.id}>, забанен.'
    await ctx.send(msgg)  
    await member.send(msgdm)
    await ctx.guild.ban(member, reason=reason)
    if arg == "s":
        await asyncio.sleep(time)          
    elif arg == "m":
        await asyncio.sleep(time * 60)
    elif arg == "h":
        await asyncio.sleep(time * 60 * 60)
    elif arg == "d":
        await asyncio.sleep(time * 60 * 60 * 24)
    await member.unban()
    await ctx.send(f'Пользователь <@{member.id}> , разбанен.')
    await member.send(f'Вы были разбанены на сервере {ctx.guild.name}')

@bot.command(name = "8ball")
async def ball(ctx, *, arg):

    message = ['Нет','Да','Возможно','Опредленно нет'] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
    return

# Работа с ошибками шара

@ball.error 
async def ball_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите вопрос.', color=0x0c0c0c)) 

@bot.command()
@commands.has_permissions( administrator = True) 
async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 666994837790261278) #Айди роли
    channel_log = bot.get_channel(670260939249156096) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( mute_role ) 

@bot.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = bot.get_channel(670260939249156096) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками бана

@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = bot.get_channel(670260939249156096) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Работа с ошибками кика

@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 694191903972917319) #Айди роли

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))   

# Работа с ошибками мута

@mute.error 
async def mute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 694191903972917319) #Айди роли

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0x0c0c0c))     

# Работа с ошибками размута

@unmute.error 
async def unmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@bot.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))

# Работа с ошибками очистки чата

@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c))

@bot.command()
async def role(ctx, Role: discord.Role ):
    guild = ctx.guild
    emb = discord.Embed(title='Информация о роли .'.format(Role.name), description=f"Роль создали {Role.created_at.strftime('%b %#d, %Y')}\n\n"
                                                                                   f"Название роли: {Role.name}\n\nЦвет: {Role.colour}\n\n"
                                                                                   f"Позиция: {Role.position}\n\n",colour= Role.colour, timestamp=ctx.message.created_at)

    emb.set_footer(text=f"ID Пользователя: {ctx.author.id}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command(name = "changename", aliases = ["rename", "change"])
@commands.has_permissions(kick_members = True)
async def changing_name(ctx, member: discord.Member = None, nickname: str = None):
    try:
        if member is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите **пользователя**!"))
        elif nickname is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите ник!"))
        else:
            await member.edit(nick = nickname)
            await ctx.send(embed = discord.Embed(description = f"У пользователя **{member.name}** был изменен ник на **{nickname}**"))
    except:
        await ctx.send(embed = discord.Embed(description = f"Я не могу изменить ник пользователя **{member.name}**!"))

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(694873549743063111)
    if before.author == bot.user:
        return
    if before.content is None:
        return;
    elif after.content is None:
        return;
    message_edit = discord.Embed(colour=0xff0000,
                                 description=f"**{before.author} Изменил сообщение в канале {before.channel}** "
                                             f"\nСтарое сообщение:{before.content}"
                                             f"\n\nНовое сообщение: {after.content}",timestamp=before.created_at)

    message_edit.set_author(name=f"{before.author}",icon_url=f"{before.author.avatar_url}")
    message_edit.set_footer(text=f"ID Пользователя: {before.author.id} | ID Сообщения: {before.id}")
    await channel.send(embed=message_edit)
    return

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(694873549743063111)
    if message.content is None:
        return;
    embed = discord.Embed(colour=0xff0000, description=f"**{message.author} Удалил сообщение в канале {message.channel}** \n{message.content}",timestamp=message.created_at)

    embed.set_author(name=f"{message.author}", icon_url=f'{message.author.avatar_url}')
    embed.set_footer(text=f'ID Пользователя: {message.author.id} | ID Сообщения: {message.id}')
    await channel.send(embed=embed)
    return

@bot.command()
async def roles(ctx, role: discord.Role):
    await ctx.send(f'**Участников с этой ролью:** {len(role.members)}')

@bot.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Пожалуйста, укажите выражение для оценки.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Результат примера: `{args}`: \n`{result}`', color = 0x39d0d6))

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def work(ctx):

        await ctx.send(embed = discord.Embed(title="**:moneybag:Вы пошли на свою работу.:moneybag:**", colour=ctx.message.author.color))

        num = random.randint(1, 500)

        userid = ctx.message.author.id # id пользователя
        serverid = ctx.guild.id # id сервера
        color = ctx.message.author.color # цвет роли пользователя 

        ocount = f'{userid}{serverid}' # будет примерно так: 349790345204334594649246512328605700

        

        listdir = os.listdir(path="bank") # читаем папку bank 

        if f'{ocount}.cfg' in str(listdir):

                await asyncio.sleep(1)
                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close() 

                new = int(money) + int(num)
                
                see = open(f'bank\\{ocount}.cfg','w')
                see.write(str(new))
                see.close()

                await ctx.send(embed = discord.Embed(title=f"**:moneybag:Вы заработали {num}.:moneybag:**", colour=color).set_thumbnail(url=ctx.message.author.avatar_url))
        else: 
                await ctx.send(embed = discord.Embed(title=f"**:moneybag:Вы ничего не заработали, сначала зарегестрируйте счет в банке.:moneybag:**", colour=color).set_thumbnail(url=ctx.message.author.avatar_url))

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def bank(ctx):
        
        user = ctx.message.author 
        userid = ctx.message.author.id 
        serverid = ctx.guild.id
        servername = ctx.guild.name 
        color = ctx.message.author.color 

        ocount = f'{userid}{serverid}'

        

        listdir = os.listdir(path="bank") 

        if f'{ocount}.cfg' in str(listdir):
                
                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close() 

                emb = discord.Embed(title="**:bank:Банк:bank:**", colour=color)
                emb.add_field(name="**Баланс:**", value=f"**:moneybag:{money}:moneybag:**", inline=False)
                emb.add_field(name="**Сервер:**", value=f"**:computer:{servername}:computer:**", inline=False)  
                emb.add_field(name="**Имя:**", value=f"**{str(user)[:-5]}**", inline=False) 
                emb.add_field(name="**Тег:**", value=f"**{str(user)[-4:]}**", inline=False) 

                await ctx.send(embed = emb)
        else:
                
                print('The member was registered.')
                print("[------------------------------]")
                print(f'          [Next]')

                reg= open(f'bank\\{ocount}.cfg','w')
                reg.write('50') # Начальная сумма
                reg.close()

                see = open(f'bank\\{ocount}.cfg','r')
                money = see.read()
                see.close()

                emb = discord.Embed(title="**:bank:Банк:bank:**", colour=color)
                emb.add_field(name="**Баланс:**", value=f"**:moneybag:{money}:moneybag:**", inline=False)
                emb.add_field(name="**Сервер:**", value=f"**:computer:{servername}:computer:**", inline=False)  
                emb.add_field(name="**Имя:**", value=f"**{str(user)[:-5]}**", inline=False) 
                emb.add_field(name="**Тег:**", value=f"**{str(user)[-4:]}**", inline=False) 

                await ctx.send(embed = emb)

@bot.command()
@commands.check(is_owner)
async def servers(ctx):
    description = ' '
    counter = 0
    for guild in bot.guilds:
        counter += 1
        description += f'{counter}) **`{guild.name}`** - **`{len(guild.members)}`** участников. ID: **`{guild.id}`** \n'

    await ctx.send(embed = discord.Embed(title = 'Сервера, на которых я нахожусь', description = description, color = 0x00ffff))

@bot.command()
@commands.check(is_owner)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))

@bot.command()
@commands.check(is_owner)
async def leave(ctx, server_id: int = None):
    if server_id == None:
        await ctx.send(embed = discord.Embed(description = f'Укажите `ID` сервера!', color=0x00ffff))
    else:

        to_leave = bot.get_guild(server_id)

        await ctx.send(embed = discord.Embed(description = f'**Я успешно прекратил обслуживание данного сервера.**', color=0x0c0c0c))
        await to_leave.leave()

@bot.command()
async def server(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"〘{ctx.guild.name}〙", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f":flag_white: **Регион: `{ctx.guild.region}`**\n\n"
        f":cowboy:  **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f":tools: **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f":green_circle: **Онлайн: `{online}`**\n\n"
        f":black_circle: **Оффлайн: `{offline}`**\n\n"
        f":yellow_circle: **Отошли: `{idle}`**\n\n"
        f":red_circle: **Не трогать: `{dnd}`**\n\n"
        f":shield: **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f":musical_keyboard: **Всего каналов: `{allchannels}`**\n\n"
        f":loud_sound: **Голосовых каналов: `{allvoice}`**\n\n"
        f":keyboard: **Текстовых каналов: `{alltext}`**\n\n"
        f":briefcase: **Всего ролей: `{allroles}`**\n\n"
        f":slight_smile: **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: 〘{ctx.guild.name}〙")
    await ctx.send(embed=embed)


# Сonntent
token = os.environ.get("Njk0NjY3NjU2MjU4NjUwMjYy.XpdPKQ.jRrgTmCB5Kgdrark5pZxSKp2lnU")
bot.run(str(token))