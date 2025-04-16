# dndnetwork.py
"""
This module contains the DungeonMasterServer class, which is a server that
manages a turn-based game for multiple connected clients. The server will
accept connections from clients, broadcast messages to all clients, and
manage the turn-based game loop. Each client is expected to send a message
to the server every turn to participate in the game. They are allowed to send
empty messages.

Players can also send '/quit' to gracefully exit the game. The server will
remove them from the game and close their connection. But it will continue
running the game loop until all players have left.
"""

import socket
import threading
import time
import datetime
import chromadb
import uuid # helps create unique identifier for chromadb documents

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from lab08.lab08 import OllamaEmbeddingFunction

from pathlib import Path


class DungeonMasterServer:
    def __init__(self, game_log, dm_hook=lambda : '', host="127.0.0.1", port=5555, countdown=10):
        self.host = host
        self.port = port
        self.countdown = countdown
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # Track connected clients in a dict: {client_socket: addr}
        self.clients = {}
        self.current_client = ''
        self.game_started = False
        self.running = True

        # Concurrency helpers for turn-based logic
        self.turn_number = 1

        self.dm_hook = dm_hook
        self.update_log = lambda msg: game_log.append(msg+'\n')

        # Saving game information
        self.collection = self.set_up_chromadb()
        self.character_info_log = []
        self.game_events_log = []
        self.joined_players = ''

    def start_server(self):
        print(f"[LOG] Listening on {self.host}:{self.port}")

        # Accept clients on a background thread
        threading.Thread(target=self.accept_clients, daemon=True).start()
        # Do the countdown here in the main thread to block until done
        self.start_countdown()
        # Once countdown finishes, start the turn-based game
        game_thread = threading.Thread(target=self.game_loop, daemon=True)
        game_thread.start()
        game_thread.join()

    def accept_clients(self):
        # List to store usernames of players
        players = []
        while True:
            client_sock, addr = self.server_socket.accept()
            name = client_sock.recv(1024).decode()
            self.clients[client_sock] = addr, name
            self.broadcast(f"[LOG] New connection from {addr}. Welcome {name}!".encode())
            # add player to list
            players.append(name)
            # Notify them if the game started or not
            if self.game_started:
                client_sock.sendall(b"[LOG] You are ready to join the game!\n")
            else:
                client_sock.sendall(b"[LOG] You joined before the countdown ended!\n")

            # Save currently joined player usernames 
            joined_players = " ".join(players)

            # Each connected client is handled in its own thread

    def handle_client(self, client_sock):
        while True:
            try:
                data = client_sock.recv(1024)
                if not data:
                    continue
                msg = data.decode().strip()

                if msg.lower() == "/quit":
                    self.remove_client(client_sock, reason="Player quit.")
                else:
                    # The player is submitting their turn action
                    self.broadcast_action(client_sock, msg)
                    # save the player's whos turn it currently is to use as a parameter so the DM can address players by name
                    addr, name = self.clients[client_sock]
                    self.current_client = name

                break
            except ConnectionResetError:
                self.remove_client(client_sock, reason="Connection reset.")
                break


    def remove_client(self, client_sock, reason=""):
        if client_sock in self.clients:
            addr, name = self.clients[client_sock]
            print(f"[LOG] Removing client {addr}: {reason}")
            # make sure client is removed from client list
            del self.clients[client_sock]
        client_sock.close()


    def start_countdown(self):
        for i in range(self.countdown, 0, -1):
            msg = f"[LOG] Countdown: {i} seconds left...\n".encode()
            self.broadcast(msg)
            time.sleep(1)
        print("[LOG] Countdown ended.")
        self.game_started = True

    def game_loop(self):
        print("[LOG] Game loop started! Each player must respond every turn.")
        self.broadcast(b"Game has started!\n")

        while self.running:
            if not self.clients:
                # if there are no more clients in the game, save the game 
                self.save_data()
                print("[LOG] No players left. Stopping game.")
                self.running = False
                break

            # Broadcast that a new turn has started
            turn_msg = f"\n[LOG] --- TURN {self.turn_number} STARTED ---\n".encode()
            self.broadcast(turn_msg)
            self.broadcast('[LOG] DM is making decisions...\n'.encode())

            dm_message = self.dm_hook()
            self.broadcast(f'[DM] {dm_message}'.encode())

            # Save the DM's response
            CHARACTER_KEYWORDS = ['character information', 'character', 'class', 'race', 'abilities']

            if any(keyword in dm_message.lower() for keyword in CHARACTER_KEYWORDS):
                # If the response conatins character information, save to the corresponding list
                self.character_info_log.append(dm_message)
            else:
                # else just save to game events
                self.game_events_log.append(dm_message)
            

            self.broadcast(b"\n\nPlease enter your action (or '/quit' to leave)\n")

            # Wait for all players to respond
            client_threads = []
            for client_sock, _ in self.clients.items():
                thread = threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True)
                thread.start()
                client_threads.append(thread)
            
            for thread in client_threads:
                thread.join()   

            # Announce that the turn is complete
            self.broadcast(f"--- TURN {self.turn_number} COMPLETE ---\n".encode())
            self.turn_number += 1
            time.sleep(1)  # Just a short pause before next turn

        self.server_socket.close()
        print("[LOG] Game loop ended. Server closed.")

    def broadcast_action(self, client_sock, msg):
        """Record the player's action, broadcast it, and signal that they've responded."""
        if client_sock not in self.clients:
            return
        addr, name  = self.clients[client_sock]

        out_msg = f"[{name}] -> {msg}\n".encode()

        # Add the players action to game events list
        self.game_events_log.append(out_msg.decode())

        self.broadcast(out_msg)

    def broadcast(self, message: bytes):
        """Send a message to all connected players."""
        message_decode = message.decode().strip()
        print(f"[LOG] Broadcasting: {message_decode}")
        self.update_log(message_decode)
        for client_sock in list(self.clients.keys()):
            try:
                client_sock.sendall(message)
            except OSError:
                self.remove_client(client_sock, reason="Send failed.")
    
    def save_data(self):
        character_info = "\n".join(self.character_info_log)
        game_events = "\n".join(self.game_events_log)

        game_time = datetime.datetime.now()
        game_time_epoch = int(game_time.timestamp())

        document = f"""
        Game Session Log
        Date: {game_time.isoformat()}
        Players: {self.joined_players}

        Character Information:
        {character_info}

        Game Events:
        {game_events}

        ----------END GAME----------
        """

        self.collection.add(
            ids=[str(uuid.uuid4())], # generate a unique ID for each document
            documents=[document],
            metadatas=[{"date": game_time_epoch}]
        )


    def set_up_chromadb(self):
        collection_name = "dnd_knowledge"

        client = chromadb.PersistentClient(path = "./chroma")
        embedding_function = OllamaEmbeddingFunction(model_name = "nomic-embed-text")

        try:
            collection = client.get_collection(collection_name)
        except:
            collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function
            )

        return collection
        

# player.py

import socket
import threading

class PlayerClient:
    def __init__(self, name, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self._name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def name(self):
        return self._name

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.sock.sendall(f'{self.name}'.encode())
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(data.decode().strip())
            except ConnectionResetError:
                print(f"[LOG] Connection closed by server.")
                break

    def send_message(self, msg: str):
        """Send a message to the DM (e.g. the player's action)."""
        self.sock.sendall(msg.encode())

    def unjoin(self):
        """Send '/quit' to gracefully exit."""
        self.send_message("/quit")
        self.sock.close()