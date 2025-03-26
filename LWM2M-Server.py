# -*- coding: utf-8 -*-
"""
Created on Tue March  26 08:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("LWM2M Server")
print(Fore.GREEN+font)

import asyncio
from aiocoap import Context, Message, PUT
from aiocoap.resource import Resource, Site

class LWM2MResource(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.value = "100"  # default value for this example

    async def render_put(self, request):
        # Handle PUT request (simulating resource update)
        print(f"Received PUT request for resource {self.name}, value: {request.payload.decode()}")
        self.value = request.payload.decode()
        response = Message(code=PUT, payload=f"Updated {self.name} value to {self.value}".encode())
        return response

    async def render_get(self, request):
        # Handle GET request (simulating resource retrieval)
        print(f"Received GET request for resource {self.name}")
        response = Message(code=PUT, payload=f"{self.value}".encode())
        return response

class LWM2MServer:
    def __init__(self, host='localhost', port=5683):
        self.host = host
        self.port = port
        self.site = Site()

    def add_resource(self, resource_name):
        resource = LWM2MResource(resource_name)
        self.site.add_resource(f"/{resource_name}", resource)

    async def start(self):
        context = await Context.create_server_context(self.site, bind=(self.host, self.port))
        print(f"LWM2M Server started at {self.host}:{self.port}")
        await asyncio.get_event_loop().create_future()  # Run forever

if __name__ == "__main__":
    host = input("Enter server IP address (default: 'localhost'): ") or 'localhost'
    port = int(input("Enter server port (default: 5683):") or 5683)

    server = LWM2MServer(host, port)
    server.add_resource('temperature')  # Add resources like temperature, humidity, etc.

    asyncio.run(server.start())
