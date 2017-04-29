#!/usr/bin/python3
import socket
from struct import pack
import logging
import time
import subprocess
import sys
import os
import signal


# Mock the remote procedure call library.
# https://www.npmjs.com/package/qrpc


classmates = [
        b"MaliciousSpoofing",
        b"BrutalCipher",
        b"NefariousSniffing",
        b"SQLizedShell",
        b"PolymorphicWEEP",
        b"HashedBackEnd",
        b"VirtualMemory",
        b"StatisticalBreakdown",
        b"TwoFactorDecryption",
        b"LockedPort",
        b"TrustedProbing",
        b"PromisedKey",
        b"ArmoredAegis",
        b"ForcefulFirewall",
        b"TopSecretExposure",
        b"ForensicDestruction",
        b"ImmuneEngineering",
        b"CautiousGuard",
        b"FabianMadeMeDoIt"
        ]
bots = [
        b"Jason Bourne",
        b"Roxanne",
        b"River"
        ]


class Player():

    def __init__(self, name, loc, direction, health, peer_id=0):
        self.name = name
        self.loc = loc
        self.direction = direction
        self.peer_id = peer_id
        self.health = health

    def __str__(self):
        return """
        Name:       {name}
        loc:        {loc}
        direction:  {direction}
        health:     {health}""".format(
            name=self.name,
            loc=str(self.loc),
            direction=self.direction,
            health=self.health
        )


class CounterstrikeWrapper():

    # PREFIX
    PREFIX = 0x94

    # Often used bytes
    c0 = 0xc0
    zero = 0x00

    MAP_WIDTH = 94
    MAP_HEIGHT = 34

    MAP_TOKENS = set([
        0x63,  # EMPTY
        0x13,  # ?
        0x14,  # ?
        0x15,  # white *
        0x18,  # ?
        0x19   # ?
    ])


    def __init__(self, server="localhost", port=8181, name=None, enemy_name=None,
                 against_bots=False, launch=False, local=False, dm=False, phase=1, bot=2):

        if launch:
            self.client = self.launch_client(local, dm, bots, phase, bot)
            time.sleep(0.5)
        else:
            self.client = None

        # open a socket...
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))

        self.peer_id = 0x00
        self.name = name
        self.enemy_name = enemy_name
        self.against_bots = against_bots
        self.counter = 1
        self.players = {}
        self.dm = dm

    def _receive_packet(self, size=1024):
        data = self.sock.recv(size)
        # print(data)
        return data

    def _send(self, packet):
        """
        :param packet: the raw data to send.
        :return:
        """
        self.sock.send(packet)
        logging.debug(packet)
        self.counter += 1

    def _string_prefix_byte(self, string):
        """
        only works for strings of 15 or less
        :return: 0xaN where n is the string length
        """
        length = len(string)
        return bytes([10 << 4 | length])

    def _strip_reply_prefix(self, data):
        """
        :param the raw reply:
        :return: tuple (counter, data)
        """
        prefix_index = len(self._get_packet_prefix())

        return data[2:prefix_index], data[prefix_index:]

    def _mask_upper_3(self, data):
        """
        :param data: takes a single byte
        :return: 00011111 AND data convert to decimal
        """
        return 0x1f & data

    def _get_packet_prefix(self):
        """
        This method sticks the 3+ byte prefix at the start
        it handles figuring out how many bytes to allocate for the message counter.

        this damn prefix updates in a most absurd way.
        00 - 7f      jumps to
        cc80 - ccff  jumps to
        cd0100 +

        this means we must have been using the top 1 bit for something else.

        :return: the message prefix
        """
        prefix = pack('>BB', self.PREFIX, self.peer_id)

        counter_bytes = 0
        if self.counter <= 127:
            counter_bytes = self.counter.to_bytes(1, byteorder='big')
        elif self.counter <= 255:
            counter_bytes = b'\xcc' + self.counter.to_bytes(1, byteorder='big')
        else:
            counter_bytes = (self.counter + 13434880).to_bytes(3, byteorder='big')
        return prefix + counter_bytes

    def _send_with_prefix(self, data):
        """
        :param data: starting with the commad prefix byte.
        :return:
        """
        self._send(self._get_packet_prefix() + data)

    def launch_client(self, local, dm, bots, phase=1, bot=3):
        if local:
            iface = subprocess.Popen(['./client', 'input'], stdin=subprocess.PIPE, shell=True)
        else:
            iface = subprocess.Popen(['./client', 'input-live'], stdin=subprocess.PIPE)
        l1 = 1
        if dm:
            l1 += 1
        if not bots:
            l1 += 2
            iface.stdin.write(str(l1).encode('utf-8'))
        else:
            iface.stdin.write(''.join([str(l1), ' ', str(phase), ' ', str(bot)]).encode('utf-8'))
        # iface.communicate()[0]
        iface.stdin.close()
        return iface

    def connect_player(self, name, pin):
        """
                            c  o  n  n  e  c  t  _  p  l  a  y
        0000   94 00 01 ae 63 6f 6e 6e 65 63 74 5f 70 6c 61 79  ....connect_play
        0010   65 72|93|a4 61 73 64 66|a4 30 30 30 30|b0 37 38  er..asdf.0000.78
        0020   64 61 62 66 33 32 61 34 33 33 63 65 33 66        dabf32a433ce3f

        :param name:
        :param pin:
        :param arg3: Hash of client

        :return:
        """
        command = b'connect_player'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x93])  # 3 args
        name_len = self._string_prefix_byte(name)
        pin_len = self._string_prefix_byte(pin)
        arg3 = b'alurbassrblng2us'  # b'alurbassrblng2us' # 78dabf32a433ce3f
        arg3_len = bytes([0xb0])
        self._send_with_prefix(command_len + command + args + name_len +
                               name + pin_len + pin + arg3_len + arg3)
        self.name = name
        self.players[name] = Player(name, (0, 0), 0, 100)
        return self._receive_packet()

    def get_t_id(self, name):
        """
        Example:
                            g  e  t  _  t  _  i  d  ?  ?  a  s
        0000   94 00 02 a8 67 65 74 5f 74 5f 69 64|91|a4 61 73  ....get_t_id..as
        0010   64 66                                            df

        :param name: the name of the player to get the ID for.
        :returns: the id
        """
        command = b'get_t_id'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x91])  # 1 arg
        name_len = self._string_prefix_byte(name)
        self._send_with_prefix(command_len + command + args + name_len + name)
        packet = self._receive_packet()

        # in case we are not the first connected self.
        if len(packet) != 0:
            t_id = packet[4]  # unpack('>B', packet[4])[0]
        else:
            t_id = 00
            print("user not found", file=sys.stderr, flush=True)
        self.peer_id = t_id
        return t_id

    def get_time_remaining(self):
        """
        Example:
        0000   94 00 03 b2 67 65 74 5f 74 69 6d 65 5f 72 65 6d  ....get_time_rem
        0010   61 69 6e 69 6e 67 90                             aining.

        :returns: the time left until a server restart
        """
        command = b'get_time_remaining'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x90])  # 0 args
        self._send_with_prefix(command_len + command + args)
        packet = self._receive_packet()
        counter, messsage = self._strip_reply_prefix(packet)
        time_left = int.from_bytes(messsage[1:], byteorder='big')
        return time_left  # convert to hours

    def query_leader(self):
        """
        Example:
                            q  u  e  r  y  _  l  e  a  d  e  r
        0000   94 00 04 ac 71 75 65 72 79 5f 6c 65 61 64 65 72  ....query_leader
        0010   90                                               .
        """
        pass

    def spawn(self, arg1, name, arg3):
        """
        Example:
                            s  p  a  w  n
        0000   94 00 05 a5 73 70 61 77 6e 93 9e a0 a0 00 00 00  ....spawn.......
        0010   00 00 00 00 00 a0 a5 1b 5b 34 30 6d a0 00 a4 61  ........[40m...a
        0020   73 64 66 03                                      sdf.
                s  d  f

        :param arg1: This is a struct of some kind, with 14 children or elements....
        :param name: the name of the player to spawn
        :param arg3: usually 0x03.  Idk what it means.
        :returns: none
        """
        if arg1 is None:
            arg1 = b'\x9e\xa0\xa0\x00\x00\x00\x00\x00\x00\x00\x00\xa0\xa5\x1b\x5b\x34\x30\x6d\xa0\x00'
        if arg3 is None:
            arg3 = 0x01

        command = b'spawn'
        command_len = self._string_prefix_byte(command)
        name_len = self._string_prefix_byte(name)
        args = bytes([0x93])  # 3 args
        arg3 = bytes([arg3])
        self._send_with_prefix(command_len + command + args + arg1 + name_len + name + arg3)
        return self._receive_packet()

    def move_to_arena(self, arena):
        """
                        14  m  o  v  e  _  t  o  _  a  r  e  n
        0000   94 00 06 ad 6d 6f 76 65 5f 74 6f 5f 61 72 65 6e  ....move_to_aren
        0010   61|94 a4 61 73 64 66 00 00 c3                    a..asdf...

        :param arena: an arena to move to.  There are 3 other unknown params, which I'll hardcode
        :returns: none
        """
        command = b'move_to_arena'
        command_len = self._string_prefix_byte(command)
        arena_len = self._string_prefix_byte(arena)
        args = bytes([0x94])  # 4 args
        arg2 = bytes([0x00])
        arg3 = bytes([0x00])
        arg4 = bytes([0xc3])
        self._send_with_prefix(command_len + command + args + arena_len + arena + arg2 + arg3 + arg4)
        self._receive_packet()

    def move_to_deathmatch(self, name):
        """
        0000   94 00 08 b2 6d 6f 76 65 5f 74 6f 5f 64 65 61 74  ....move_to_deat
        0010   68 6d 61 74 63 68 94 ad 52 69 73 6b 79 48 6f 6e  hmatch..RiskyHon
        0020   65 79 70 6f 74 00 00 c2

        may not need this methond, since we will be playing with this and a normal self.
        """
        pass

    def generate_bot(self, name):
        """
                                       94 00 09 ac 67 65 6e 65  eypot.......gene
        0030   72 61 74 65 5f 62 6f 74 95 ad 52 69 73 6b 79 48  rate_bot..RiskyH
        0040   6f 6e 65 79 70 6f 74 00 00 c3 00                 oneypot....

        may not need this method, since we will be playing with this and a normal self.
        """
        command = b'generate_bot'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x95])  # 3 args
        name_len = self._string_prefix_byte(name)
        arg2 = bytes([0x00])
        arg3 = bytes([0x00])
        arg4 = bytes([0xc3])
        arg5 = bytes([0x00])
        self._send_with_prefix(command_len + command + args + name_len + name + arg2 + arg3 + arg4 + arg5)
        reply = self._receive_packet()
        counter, message = self._strip_reply_prefix(reply)

    def check_winner(self, name):
        """
        0000   94 00 07 ac 63 68 65 63 6b 5f 77 69 6e 6e 65 72  ....check_winner
        0010   93 a4 61 73 64 66 00 00                          ..asdf..

        :param name: the name of the player to check for winner status
                     there are 2 other unknown params, hardcoded
        :returns: T/F
        """
        command = b'check_winner'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x93])  # 3 args
        name_len = self._string_prefix_byte(name)
        arg2 = bytes([0x00])
        arg3 = bytes([0x00]) if not self.against_bots else bytes([0x06])
        self._send_with_prefix(command_len + command + args + name_len + name + arg2 + arg3)
        reply = self._receive_packet()
        counter, message = self._strip_reply_prefix(reply)
        # print(counter, message)
        return message[1] > 0

    def get_ppl(self, name):
        """
        Updates the self.players dictionary

        EXAMPLE command
        0000   94 00 09 a7 67 65 74 5f 70 70 6c 93 a4 61 73 64  ....get_ppl..asd
        0010   66 00 00                                         f..

        EXAMPLE response
        0000   94 01 cd 16 a3 c0 92 9e
               a4 61 73 64 66   <NAME>
               a0               <Empty String>
               fb               <Health>
               01               <LIVES>
        0010   00               <SCORE>
               04               <Direction>
               57               <X>
               05               <Y>
               00 00 a5 1b 5b 33 30 6d a5 1b 5b 34
        0020   30 6d a4 61 73 64 66 00 9e a4 31 32 33 34 a0 64
        0030   03 02 04 57 07 00 00 a5 1b 5b 33 36 6d a5 1b 5b
        0040   34 30 6d a4 31 32 33 34 00

        :param name: you should be able to give it any name,
                     and the response will be the same
        :returns: none
        """
        command = b'get_ppl'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x93])  # 3 args
        name_len = self._string_prefix_byte(name)
        arg2 = bytes([0x00])  # What does this do?
        arg3 = bytes([0x00]) if not self.against_bots else bytes([0x06])  # What does this do?
        self._send_with_prefix(command_len + command + args + name_len + name + arg2 + arg3)
        reply = self._receive_packet()
        counter, message = self._strip_reply_prefix(reply)
        assert(len(message) > 0)
        assert(message[0] == 0xc0)
        # print(message)
        player_chunks = message.split(b'\x9e')  # 9e only appears at the start of each struct.

        for i in range(1, len(player_chunks)):
            player_data = player_chunks[i]

            cursor = 0
            player_name_length = self._mask_upper_3(player_data[cursor])
            player_name = player_data[1:player_name_length + 1]  # +1 for index not length
            cursor += player_name_length + 1  # +1 for the length byte

            if player_name in self.players:
                this_player = self.players[player_name]
            else:
                this_player = Player(player_name, (0, 0), 0, 100)
                self.players[player_name] = this_player

            # Ignore the typestring for now...
            player_type_length = self._mask_upper_3(player_data[cursor+0])
            cursor += player_type_length + 1  # +1 for length byte

            this_player.health = player_data[cursor+0]
            this_player.lives = player_data[cursor+1]
            this_player.score = player_data[cursor+2]
            this_player.direction = player_data[cursor+3]
            this_player.loc = (
                player_data[cursor+4],  # X
                player_data[cursor+5]   # Y
            )

    def update(self, name):
        """
        Ask for the server's updated version of the map.

        0000   94 00 08 a6 75 70 64 61 74 65 93 a4 61 73 64 66  ....update..asdf
        0010   00 00

        :return: a 2D array of map data.
        """
        command = b'update'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x93])  # 3 args
        name_len = self._string_prefix_byte(name)
        arg2 = bytes([0x00])
        arg3 = bytes([0x00]) if not self.against_bots else bytes([0x06])
        self._send_with_prefix(command_len + command + args + name_len + name + arg2 + arg3)

        bytes_to_get = len(self._get_packet_prefix()) + 6
        reply = self._receive_packet(size=bytes_to_get)
        counter, message = self._strip_reply_prefix(reply)

        # verify the message begins with c0
        assert(len(message) > 0)
        assert(message[0] == 0xc0)
        # the second and fourth byte are uninstersting.
        array_length = message[3]
        row_length = message[5]
        assert(row_length is not None)
        cols = []
        for i in range(array_length):
            row = []
            if i > 0:
                self._receive_packet(size=2)
            for j in range(row_length):
                # put the thing into the array...
                row.append(self._receive_packet(size=1))
            cols.append(row)
        self.map = cols
        if client.MAP_WIDTH == 0:
            client.MAP_WIDTH = len(cols[0])
            client.MAP_HEIGHT = len(cols)
        return cols

    def move(self, name, a1, a2):
        """
        0000   94 00 cd 01 29 a4 6d 6f 76 65 95 a4 61 73 64 66  ....).move..asdf
        0010   00 00 01 00                                      ....

        :param name:
        :params:
            up a2 ff,
            left a1 ff,
            down a2 01,
            right a1 01,
        :return: none
        """
        command = b'move'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x95])  # 5 args
        name_len = self._string_prefix_byte(name)
        self._send_with_prefix(command_len + command + args + name_len + name +
                               bytes([0x00]) +
                               (bytes([0x00]) if not self.against_bots else bytes([0x06])) +
                               bytes([a1]) +
                               bytes([a2])
                               )
        self._receive_packet()
        # Finally, update the internal position of the client.
        # Can't do this yet because 2's compliment goddamnit.

    def fire_projectile(self, name, x, y, a1, a2, p_type):
        """
        0000   94 00 cd 4f b4 af 66 69 72 65 5f 70 72 6f 6a 65  ...O..fire_proje
        0010   63 74 69 6c 65 98 a4 61 73 66 64 20 05 01 00 00  ctile..asfd ....
        0020   00 01                             ^     ^----------------------
                                                these 2 indicate position    |
                                                     the next 2 are direction, same as move

                                                `

        0000   94 00 cd 01 4d af 66 69 72 65 5f 70 72 6f 6a 65  ....M.fire_proje
        0010   63 74 69 6c 65 98 a4 61 73 64 66 29 05 00 01 00  ctile..asdf)....
        0020   00 01
                                             ..
        takes 8 arguments...

        projectiles:

        0: normal, 7 damage
        1: normal, 7 damage
        2: red, 20 damage
        6: fire through walls, 5 damage
        7: fire thgough walls, 12 damage
        8: 1 damage, invisible
        """
        command = b'fire_projectile'
        command_len = self._string_prefix_byte(command)
        args = bytes([0x98])  # 8 args
        name_len = self._string_prefix_byte(name)
        self._send_with_prefix(command_len + command + args + name_len + name +
                               bytes([x]) +
                               bytes([y]) +
                               bytes([a1]) +
                               bytes([a2]) +
                               bytes([0x00]) +  # no idea what this does
                               (bytes([0x00]) if not self.against_bots else bytes([0x06])) +  # or this
                               bytes([p_type])
                               )
        self._receive_packet()

    def lay_mine(self, name, x, y, p_type):
        self.fire_projectile(name, x, y, 0, 0, p_type)

    def blast_enemy(self, name):
        if not self.enemy_loc:
            print("Enemy location unknown", file=sys.stderr, flush=True)
        print("Blasting enemy at " + str(self.enemy_loc), file=sys.stderr, flush=True)
        x = self.enemy_loc[0]
        y = self.enemy_loc[1]

        startx = x - 4 if x - 4 > 0 else 0
        stopx = x + 4 if x + 4 < self.MAP_WIDTH else self.MAP_WIDTH
        starty = y - 2 if y - 2 > 0 else 0
        stopy = y + 2 if y + 2 < self.MAP_HEIGHT else self.MAP_HEIGHT

        for i in range(startx, stopx+1):
            for j in range(starty, stopy+1):
                self.fire_projectile(name, i, j, 1, 0, 1)

        time.sleep(.1)

    def add_friend(self, name, map_id, loc, peer_id):
        self.friends.append(Player(self, name, map_id, peer_id))

    def add_enemy(self, name, map_id, loc, peer_id):
        self.friends.append(Player(self, name, map_id, peer_id))

    @property
    def my_loc(self):
        if self.name in self.players:
            return self.players[self.name].loc
        return None

    @property
    def enemy_loc(self):
        if self.enemy_name in self.players:
            return self.players[self.enemy_name].loc
        return None


#
# Begin writing a set of methods to define our offensive logic.
# That way we don't have to comment out code and can swap between new attack patterns
#

def cornerblast(client, name):
    """
    Causes bot to return repeatedly to the corner, while we blast them...
    """
    # need to check if we are two from end first
    client.name = name
    client.get_ppl(name)
    pos = client.players[name].loc
    print(pos, file=sys.stderr, flush=True)
    print(client.enemy_loc, file=sys.stderr, flush=True)

    # start at bottom right
    client.move(name, client.MAP_WIDTH - pos[0] - 1, client.MAP_HEIGHT - pos[1] - 1)

    # Place mines once, they will persist.
    for i in range(1, 10):
        for j in range(1, 10):
            client.lay_mine(name, j, i, 1)

    while not client.check_winner(name):
        time.sleep(.2)
        client.move(name, 0, 0xfc)
        time.sleep(.2)
        client.move(name, 0, 4)

        time.sleep(.2)
        client.move(name, 0xfc, 0)
        time.sleep(.2)
        client.move(name, 4, 0)

    print("You win!")


def move_enemy(client, enemy_name, x, y):
    if x >= client.MAP_WIDTH and y >= client.MAP_HEIGHT:
        return False
    time.sleep(0.1)
    client.get_ppl(name)
    # print(client.enemy_loc)
    if client.enemy_loc is None:
        raise Exception("Couldn't find enemy")
    if client.enemy_loc != (x, y):
        if (client.enemy_loc[0] <= x and client.enemy_loc[1] <= y) or \
                (x - client.enemy_loc[0] >= -32 and y - client.enemy_loc[1] >= -32):
            client.move(enemy_name, twos_comp(x - client.enemy_loc[0], 8),
                        twos_comp(y - client.enemy_loc[1], 8))
        else:
            client.move(enemy_name, twos_comp(max(-32, x - client.my_loc[0]), 8),
                        twos_comp(max(-32, y - client.my_loc[1]), 8))
    return True


def fire_top_corner(client, name):
    for i in range(1, 10):
        for j in range(1, 10):
            client.lay_mine(name, j, i, 1)


def move(client, name, x, y):
    if x >= client.MAP_WIDTH and y >= client.MAP_HEIGHT:
        return False
    time.sleep(0.1)
    client.get_ppl(name)
    if client.my_loc is None:
        raise Exception("Couldn't find player")
    if client.my_loc[0] not in [0, client.MAP_WIDTH - 1] and\
            client.my_loc[1] not in [0, client.MAP_HEIGHT - 1]:
        print("Moved out of wall " + str(client.my_loc), file=sys.stderr, flush=True)
    if client.my_loc != (x, y):
        if (client.my_loc[0] <= x and client.my_loc[1] <= y) or \
                (x - client.my_loc[0] >= -32 and y - client.my_loc[1] >= -32):
            client.move(name, twos_comp(x - client.my_loc[0], 8), twos_comp(y - client.my_loc[1], 8))
        else:
            client.move(name, twos_comp(max(-32, x - client.my_loc[0]), 8),
                        twos_comp(max(-32, y - client.my_loc[1]), 8))
            return move(client, name, x, y)
    return True


def print_map(client):
    for i in client.map:
        print('[', end='', file=sys.stderr, flush=True)
        for j in i:
            print(str(int.from_bytes(j, byteorder='big')) + ", ", end='', file=sys.stderr, flush=True)
        print('],', file=sys.stderr, flush=True)


def mine_fill_dumb(client, name):
    for i in range(1, max(client.MAP_WIDTH+1, client.MAP_HEIGHT+1)):
        for j in range(1, i+1):
            if i < client.MAP_WIDTH+1 and j < client.MAP_HEIGHT+1:
                client.lay_mine(name, client.MAP_WIDTH-i, client.MAP_HEIGHT-j, 1)
            if j < client.MAP_WIDTH+1 and i < client.MAP_HEIGHT+1:
                client.lay_mine(name, client.MAP_WIDTH-j, client.MAP_HEIGHT-i, 1)


def mine_fill(client, name):
    for i in range(1, max(client.MAP_WIDTH+1, client.MAP_HEIGHT+1)):
        for j in range(1, i+1):
            if i < client.MAP_WIDTH+1 and j < client.MAP_HEIGHT+1:
                if not client.dm and client.WALL_LOC[client.MAP_HEIGHT-j][client.MAP_WIDTH-i] == 0x63\
                        and not client.against_bots:
                    client.lay_mine(name, client.MAP_WIDTH-i, client.MAP_HEIGHT-j, 6)
                elif client.dm and (client.MAP_WIDTH-i in [0, client.MAP_WIDTH - 1] or
                                    client.MAP_HEIGHT-j in [0, client.MAP_HEIGHT - 1]):
                    client.lay_mine(name, client.MAP_WIDTH-i, client.MAP_HEIGHT-j, 6)
                else:
                    client.lay_mine(name, client.MAP_WIDTH-i, client.MAP_HEIGHT-j, 1)
            if j < client.MAP_WIDTH+1 and i < client.MAP_HEIGHT+1:
                if not client.dm and client.WALL_LOC[client.MAP_HEIGHT-i][client.MAP_WIDTH-j] == 0x63\
                        and not client.against_bots:
                    client.lay_mine(name, client.MAP_WIDTH-j, client.MAP_HEIGHT-i, 6)
                elif client.dm and (client.MAP_WIDTH-j in [0, client.MAP_WIDTH - 1] or
                                    client.MAP_HEIGHT-i in [0, client.MAP_HEIGHT - 1]):
                    client.lay_mine(name, client.MAP_WIDTH-j, client.MAP_HEIGHT-i, 6)
                else:
                    client.lay_mine(name, client.MAP_WIDTH-j, client.MAP_HEIGHT-i, 1)


def mine_enemy(client, name, count=1, update=True):
    if update:
        client.get_ppl(name)
    if client.enemy_loc is None:
        return
    # print('enemy loc: ' + str(client.enemy_loc), file=sys.stderr)
    for i in range(-3, 4):
        for j in range(-3, 4):
            if -1 < (client.enemy_loc[0] + j) < (client.MAP_WIDTH) and\
                    -1 < (client.enemy_loc[1] + i) < (client.MAP_HEIGHT):
                if not client.dm and client.WALL_LOC[client.enemy_loc[1] + i][client.enemy_loc[0] + j] == 0x63\
                        and not client.against_bots:
                    client.lay_mine(name, client.enemy_loc[0] + j, client.enemy_loc[1] + i, 6)
                elif client.dm and (client.enemy_loc[0] + j in [0, client.MAP_WIDTH - 1] or
                                    client.enemy_loc[1] + i in [0, client.MAP_HEIGHT - 1]):
                    client.lay_mine(name, client.enemy_loc[0] + j, client.enemy_loc[1] + i, 6)
                else:
                    client.lay_mine(name, client.enemy_loc[0] + j, client.enemy_loc[1] + i, 1)


def perimeter_walk(client, name, enemy_name):
    # add client position check after mining enemy
    # mine_fill(client, name)
    while not client.check_winner(name):
        # bottom right
        move_enemy(client, enemy_name, 89, 29)
        move(client, name, client.MAP_WIDTH - 1, client.MAP_HEIGHT - 1)
        mine_enemy(client, name, 10)
        # bottom left:
        move(client, name, 0, client.MAP_HEIGHT - 1)
        mine_enemy(client, name, 10)
        # top left
        move(client, name, 0, 0)
        mine_enemy(client, name, 10)
        # top right
        move(client, name, client.MAP_WIDTH - 1, 0)
        mine_enemy(client, name, 10)


def bot_teleportation_glitch(client, name):
    move(client, name, client.MAP_WIDTH - 1, client.MAP_HEIGHT - 1)
    while not client.check_winner(name):
        client.move(name, 0, 0xfc)
        fire_top_corner(client, name)
        client.move(name, 0, 4)


def hide_and_fill(client, name):
    move(client, name, client.MAP_WIDTH - 1, client.MAP_HEIGHT - 1)
    while not client.check_winner(name):
        # mine_enemy(client, name)
        mine_fill(client, name)
        # mine_fill_trash_server(client, name)


def corner_enemy_and_mine(client, name, enemy):
    if client.againse_bots:
        return
    while not client.check_winner(name):
        move(client, name, 0, 0)
        move(client, enemy, client.MAP_WIDTH - 5, client.MAP_WIDTH - 5)
        mine_enemy(client, name, True)


def suicides_aint_shit(client, name):
    while not client.check_winner(name):
        client.move(name, 127, 127)
        mine_enemy(client, name, 10)


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val + (1 << bits)
    return val


if __name__ == "__main__":
    try:
        name = b'RiskyHoneypot'
        enemy_name = b'BrutalCipher'
        # opponent = b'Jason Bourne'
        client = CounterstrikeWrapper(server='colosseum.cs.unc.edu', against_bots=False, name=name,
                                      enemy_name=enemy_name, launch=False, local=True, dm=False)
        # client = CounterstrikeWrapper(server='localhost', against_bots=False, name=name,
        #                               enemy_name=b'Roxanne', launch=False, local=True, dm=False)

        print('connected', file=sys.stderr, flush=True)

        # client.connect_player(name, b"3086")

        # client.get_t_id(name)
        # time_left = client.get_time_remaining()
        # print("Time left: " + str(time_left))

        # client.query_leader()

        # print(client.spawn(None, name, i))

        # client.move_to_arena(name)

        # cornerblast(client, name)

        # hide_and_fill(client, name)

        perimeter_walk(client, name, enemy_name)
        # suicides_aint_shit(client, name)
        # mine_fill(client, name)

        print('won', file=sys.stderr, flush=True)

        if client.client is not None:
            client.client.kill()

        client.sock.close()

    except KeyboardInterrupt:
        if client.client is not None:
            os.killpg(os.getpgid(client.client.pid), signal.SIGTERM)
        sys.exit()

    # except Exception as e:
    #     print(e)
    #     if client.client is not None:
    #         os.killpg(os.getpgid(client.client.pid), signal.SIGTERM)
    #     sys.exit()
