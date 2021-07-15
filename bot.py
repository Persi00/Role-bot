import discord, json
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.', intents=discord.Intents.all())

database_file = open("database.json", 'a+')
if database_file.read() == "":
    database_file.write('{"user": []}')
database = json.load(database_file)
database_file.close()

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_member_join(member : discord.Member):
    for user in database["users"]:
        if user['member'] == member.id:
            for role_id in user["roles"]:
                role = get(member.guild.roles, id=role_id)
                if role != None:
                    await member.add_roles(role)

@client.command()
async def myRoles(ctx):
    found = False
    for user in database["users"]:
        print(f"{user['member']}  {ctx.author}")
        if str(await client.fetch_user(user['member'])) == str(ctx.author):
            send = ""
            if len(user['roles']) != 0:
                found = True
            else:
                break
            for role_id in user['roles']:
                role = get(ctx.guild.roles, id=role_id)
                if role != None:
                    send += f"<@&{role.id}>, "

            send = send[:-2]
            send = "Your Roles: " + send
            if len(send) > 2000:
                await ctx.send("You have to many roles to send them in message!")
                break
            await ctx.send(send)
    if not found:
        await ctx.send("You haven't roles!")

@client.command()
async def showRoles(ctx, member : discord.Member):
    found = False
    for user in database["users"]:
        print(f"{user['member']}  {ctx.author}")
        if str(await client.fetch_user(user['member'])) == str(member):
            send = ""
            if len(user['roles']) != 0:
                found = True
            else:
                break
            for role_id in user['roles']:
                role = get(ctx.guild.roles, id=role_id)
                if role != None:
                    send += f"<@&{role.id}>, "

            send = send[:-2]
            send = f"<@!{member.id}>'s Roles: " + send
            if len(send) > 2000:
                await ctx.send(f"<@!{member.id}> has to many roles to send them in message!")  
                break
            await ctx.send(send)
    if not found:
        await ctx.send(f"<@!{member.id}> haven't roles!")

@client.command()
async def addRole(ctx, member : discord.Member, role : discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        found = False
        exist = False
        for user in database["users"]:
            if str(await client.fetch_user(user['member'])) == str(member):
                found = True
                if len(user['roles']) == 0:
                    exist = False
                if len(user['roles']) > 0:
                    for role_id in user['roles']:
                        if role_id == role.id:
                            exist = True
                            break
                if not exist:
                    user['roles'].append(role.id)
                    await member.add_roles(role)
                    await ctx.send(f'Now <@!{member.id}> has <@&{role.id}>!')
                else:
                    await ctx.send(f"<@!{member.id}> already has <@&{role.id}>!")
                    break
        if not found:
            database['users'].append({"member": member.id, "roles": [role.id]})
            await member.add_roles(role)
            await ctx.send(f'Now <@!{member.id}> has <@&{role.id}>!')

        with open('database.json', 'w') as database_file:
            json.dump(database, database_file)
    else:
        await ctx.send("You haven't permission to give someone role!")


@client.command()
async def removeRole(ctx, member : discord.Member, role : discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        found = False
        exist = False
        for user in database["users"]:
            if str(await client.fetch_user(user['member'])) == str(member):
                found = True
                if len(user['roles']) == 0:
                    exist = False
                if len(user['roles']) > 0:
                    for role_id in user['roles']:
                        if role_id == role.id:
                            exist = True
                            break
                if not exist:
                    await ctx.send(f"<@!{member.id}> hasn't <@&{role.id}>!")
                else:
                    await member.remove_roles(role)
                    await ctx.send(f"<@!{member.id}> already hasn't <@&{role.id}>!")
                    break
        if not found:
            database['users'].append({"member": member.id})
            await ctx.send(f"<@!{member.id}> hasn't <@&{role.id}>!")

        with open('database.json', 'w') as database_file:
            json.dump(database, database_file)
    else:
        await ctx.send("You haven't permission to give someone role!")

        
client.run('ODA2OTAwMjUyMTkxODgzMzA0.YBwKaw._pyOAW8bM-SpUJDmBJHiY5iJBkM')