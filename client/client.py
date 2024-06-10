import asyncio
import curses
import websockets

class TerminalEditor:
    logged_in = False

    def __init__(self):
        self.uri = "ws://localhost:8765"
        self.websocket = None

    async def run(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        try:
            await self.main(stdscr)
        finally:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

    async def main(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.menu()
        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()
            if self.logged_in:
                if key == ord('1'):
                    await self.save_file()
                elif key == ord('2'):
                    await self.open_file()
                elif key == ord('q'):
                    break
            else:
                if key == ord('1'):
                    await self.register()
                elif key == ord('2'):
                    await self.login()
                elif key == ord('q'):
                    break

    def menu(self):
        self.stdscr.clear()
        if self.logged_in:
            self.stdscr.addstr(0, 0, "1. Save")
            self.stdscr.addstr(1, 0, "2. Open")
        else:
            self.stdscr.addstr(0, 0, "1. Register")
            self.stdscr.addstr(1, 0, "2. Login")
        self.stdscr.addstr(2, 0, "q. Quit")
        self.stdscr.refresh()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def register(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Register")
        self.stdscr.addstr(1, 0, "Username: ")
        curses.echo()
        username = self.stdscr.getstr(1, 10, 20).decode('utf-8')
        self.stdscr.addstr(2, 0, "Password: ")
        password = self.stdscr.getstr(2, 10, 20).decode('utf-8')
        curses.noecho()

        await self.connect()
        await self.websocket.send(f"register {username} {password}")
        response = await self.websocket.recv()
        self.display_message(response)

    async def login(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Login")
        self.stdscr.addstr(1, 0, "Username: ")
        curses.echo()
        username = self.stdscr.getstr(1, 10, 20).decode('utf-8')
        self.stdscr.addstr(2, 0, "Password: ")
        password = self.stdscr.getstr(2, 10, 20).decode('utf-8')
        curses.noecho()

        await self.connect()
        await self.websocket.send(f"login {username} {password}")
        response = await self.websocket.recv()
        if response.startswith("Authenticated"):
            self.logged_in = True
        self.display_message(response)

    async def save_file(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Save")
        self.stdscr.addstr(1, 0, "Enter file name: ")
        curses.echo()
        filename = self.stdscr.getstr(1, 18, 20).decode('utf-8')
        self.stdscr.addstr(2, 0, "Enter file content: ")
        content = self.stdscr.getstr(2, 21, 60).decode('utf-8')
        curses.noecho()

        await self.connect()
        await self.websocket.send(f"write {filename} {content}")
        response = await self.websocket.recv()
        self.display_message(response)

    async def open_file(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Open")
        self.stdscr.addstr(1, 0, "Enter file name: ")
        curses.echo()
        filename = self.stdscr.getstr(1, 18, 20).decode('utf-8')
        curses.noecho()

        await self.connect()
        await self.websocket.send(f"read {filename}")
        response = await self.websocket.recv()
        self.display_message(response)

    async def commit(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(f"commit {message}")
            response = await websocket.recv()
            self.display_message(response)

    async def push(self):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send("push")
            response = await websocket.recv()
            self.display_message(response)

    async def pull(self):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send("pull")
            response = await websocket.recv()
            self.display_message(response)

    def display_message(self, message):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, message)
        self.stdscr.addstr(1, 0, "Press any key to return to menu...")
        self.stdscr.refresh()
        self.stdscr.getch()
        self.menu()

async def main():
    editor = TerminalEditor()
    await editor.run()

if __name__ == "__main__":
    asyncio.run(main())
