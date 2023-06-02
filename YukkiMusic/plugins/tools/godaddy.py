from pyrogram import filters
from YukkiMusic import app


import requests as req
def godaddy_lookup(domain:str):
 try:
    u = f"https://api.godaddy.com/v1/domains/available?domain={domain}&checkType=FAST"
    headers = {
        'Authorization': f'sso-key gHf76cHJZSLN_TvUw6AfMfME4Ksa3qjPWBX:CNRnvSjVRjcJkE9hyZDnjZ',
        'Content-Type': 'application/json',
    }
    r = req.get(u, headers=headers)
    if r.status_code != 200:
        return None 
    data =  r.json()
    price = data.get("price", None)
    getPrice =  '${:,.2f}'.format(price / 1000000) if price else None
    isTaken =  data['available']
    return {
        "domain": domain,
        "price":getPrice,
        "available": isTaken,
        "success":True
    }
 except:
    return {
       "success":False
    }

@app.on_message(filters.command(['gd'], ['!', ".", "/"]))
async def godady(client, message):
    msg = await message.reply("wait....")
    user_id = None
    if message and message.from_user and message.from_user.id:
        user_id = message.from_user.id
    if not user_id:
        await msg.edit("There is an error hitted. Retry pls...")
        return
    if len(message.command) <= 1:
        await msg.edit("Provide a name /domain example.com")
        return
    domains = [ domain for domain in message.command[1:] if "." in domain ]
    if not domains:
       await msg.edit("Double check your domain name. Must have a extension...")
       return
    d = "**[GODADDY LOOKUP ]**\n\n"
    status = "❌ Taken"
    for domain in domains:
       r =  godaddy_lookup(domain)
       if not r:
          await msg.edit("Unable to check.")
          return
          
       if not r['success']:
          status = "❌ Failed"
          d += f"**{status} | {domain} | Invalid Domain/ Not Supported**\n"
       if r['available']:
          status = "✅ Available"
          d +=  f"**{status} | {domain} | {r['price']}**\n"
       else:
          status = "❌ Taken"
          d +=  f"**{status} | {domain} | Domain Taken**\n"
    await msg.edit(d)


