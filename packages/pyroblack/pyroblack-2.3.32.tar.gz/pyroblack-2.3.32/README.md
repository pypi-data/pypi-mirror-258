<p align="center">
    <a href="https://github.com/eyMarv/pyrofork">
        <img src="static/img/pyrofork.png" alt="Pyrofork" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://eyMarv.github.io/pyrofork-docs">
        Documentation
    </a>
    •
    <a href="https://github.com/eyMarv/pyrofork/issues">
        Issues
    </a>
    •
    <a href="https://t.me/MayuriChan_Chat">
        Support Chat
    </a>
</p>

## Pyrofork

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrofork!")


app.run()
```

**Pyrofork** is a modern, elegant and asynchronous [MTProto API](https://eyMarv.github.io/pyrofork-docs/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.

### Support

If you'd like to support Pyrofork, you can consider:

- [Become a GitHub sponsor](https://github.com/sponsors/Mayuri-Chan).

### Key Features

- **Ready**: Install Pyrofork with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [TgCrypto](https://github.com/pyrogram/tgcrypto), a high-performance cryptography library written in C.  
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip3 install git+https://github.com/eyMarv/pyrofork.git
```

### Resources

- Check out the docs at https://eyMarv.github.io/pyrofork-docs to learn more about Pyrofork, get started right
away and discover more in-depth material for building your client applications.
- Join the official group at https://t.me/OpenFileZ and stay tuned for news, updates and announcements.
