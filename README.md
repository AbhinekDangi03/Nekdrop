# Nekdrop

The Zero-Trust File Relay. A secure, transient bridge between untrusted terminals and private nodes.

The TL;DR: Think of it as AirDrop for everyone else. Move a file from any computer to any phone just by scanning a QR. No login, no cloud, no trace left behind.


# The Philosophy

Nekdrop doesn't store any data. It simply manages 'Rooms'.
When a laptop joins Room A and a phone joins Room A, the server acts as a Pipe.

The file is sliced into binary chunks on the laptop, flows through this pipe, and is reassembled on the phone. This ensures that no data is ever leaked to the public computer's storage.


# Why am I doing this?

My motivation behind Nekdrop is to share files from a college computer to my mobile without opening any third-party software or web apps.

In my college, you have to make written lab files. To make those files, you need screenshots of the programs and codes done during lab periods. Usually, this sharing is done by signing into Gmail, WhatsApp, or Outlook—which is a big security risk. (What if I forget to log out? What if people see my data?).

Nekdrop aims to solve this problem by sharing files in a direct memory-to-memory manner.

# The Problems

Connectivity: Data transfer requires a Shared Medium. If devices are not on the same local network (Wi-Fi), there are only two options:

  1. Physical Bridge: Bluetooth or Wi-Fi Direct (P2P).

  2. Global Bridge: A 'Relay Server' on the public internet.

Since college computers are trapped behind a firewall and mobile phones have their own data, they are in two different dimensions.

The Solution:

  1. Create a Temporal Portal: Running a tiny webserver on my old mobile phone using Termux.

  2. Generate a One-Time URL: Since the server (phone) is on the internet, it generates a QR code.

  3. Close the Portal: The PC sees the portal, drops the file, and the portal wipes from existence.

# How It Works

  1. The Handshake: The webpage connects to the home server running a FastAPI service to give the phone a temporary public "Global Address."

  2. The Discovery: The webpage displays a QR code containing a session ID (UUID) and WebSocket URL.

  3. The Transmission: The transfer happens over WebSockets, showing real-time data streams.

  4. Finishing: When completed, the session is wiped. The file was never "saved" on the internet.

# The Blueprint

  1. The Server (FastAPI): A Python script in Termux that creates "Rooms" (like those in Among Us). If two people join Room 123, the server relays data between them.

  2. The Tunnel (Cloudflared): A tool that gives Termux a public URL, bypassing CGNAT (Carrier Grade NAT) that usually prevents phones from being servers.

  3.The Handshake (QR): A simple HTML page. Scanning the code joins your phone to the specific room.
  
# Technical Stack

  1. FastAPI: A high-performance web framework. It fetches index.html and manages the Phone -> FastAPI -> PC flow.

  2. WebSockets: Provides the full-duplex communication protocol.

  3. Cloudflare Tunnel: Handles NAT Traversal (The Portal).

# Security

To keep the transfer secure, we utilize:

 1. Room ID (UUID): A long, non-guessable random string.

 2. Token Handshake: Your phone sends a "secret word" to the server.

 3. In-Memory Only: Files are streamed; they are never saved to the phone's disk.
  
 4. Cloudflare WAF: Protected by a Web Application Firewall.

# Server Architecture

I am using Termux with OpenSSH, which is a Daemon (background process) listening for encrypted connections.

Since it is a Remote Shell, it doesn't just serve files like a web server (which gives OUTPUT); it serves CONTROL (which gives you INPUT). This allows me to treat the mobile node as a Headless Server.

Nekdrop operates on two layers:

  1. Layer 1 (SSH Server): Allows the developer to control the phone, navigate folders, and start the engine.

  2. Layer 2 (FastAPI Server): Allows the users to move files. They don't have 'Control' over your phone; they can't run commands; they can only use the Bridge created for them.
