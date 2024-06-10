import asyncio
import websockets
from file_manager import FileManager
from git_manager import GitManager
from auth import AuthManager
from logger import Logger

async def handler(websocket, path):
    file_manager = FileManager()
    git_manager = GitManager()
    auth_manager = AuthManager()
    logger = Logger("server_logger")

    authenticated = False
    username = None
    try:
        async for message in websocket:
            logger.log_info(f"Received message: {message}")
            command, *args = message.split()
            if command == "register":
                try:
                    username, password = args
                    auth_manager.add_user(username, password)
                    await websocket.send("Registration successful")
                    logger.log_info(f"User {username} registered successfully")
                except Exception as e:
                    await websocket.send(f"Registration failed: {e}")
                    logger.log_error(f"User registration failed: {e}")
            elif command == "login":
                try:
                    username, password = args
                    token = auth_manager.authenticate(username, password)
                    await websocket.send(f"Authenticated {token}")
                    logger.log_info(f"User {username} authenticated successfully")
                except Exception as e:
                    await websocket.send(f"Authentication failed: {e}")
                    logger.log_error(f"User authentication failed: {e}")
            elif command == "verify":
                try:
                    token = args[0]
                    username = auth_manager.verify_token(token)
                    authenticated = True
                    await websocket.send(f"Token valid for {username}")
                    logger.log_info(f"Token verified for {username}")
                except Exception as e:
                    await websocket.send(f"Token verification failed: {e}")
                    logger.log_error(f"Token verification failed: {e}")
            elif authenticated:
                if command == "read":
                    content = file_manager.read_file(args[0])
                    await websocket.send(content)
                    logger.log_info(f"File {args[0]} read by user {username}")
                elif command == "write":
                    filename, content = args[0], " ".join(args[1:])
                    file_manager.write_file(filename, content)
                    await websocket.send("File written")
                    logger.log_info(f"File {filename} written by user {username}")
                elif command == "commit":
                    git_manager.commit(args[0])
                    await websocket.send("Commit done")
                    logger.log_info(f"Commit with message '{args[0]}' by user {username}")
                elif command == "push":
                    git_manager.push()
                    await websocket.send("Push done")
                    logger.log_info(f"Push executed by user {username}")
                elif command == "pull":
                    git_manager.pull()
                    await websocket.send("Pull done")
                    logger.log_info(f"Pull executed by user {username}")
            else:
                await websocket.send("Authentication required")
    except websockets.ConnectionClosed:
        logger.log_info("Connection closed")
    except Exception as e:
        logger.log_error(f"Error: {e}")
        await websocket.send(f"Error: {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
