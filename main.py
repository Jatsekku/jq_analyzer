from enum import Enum
import time

CommandState = Enum('NEW_COMMAND', 'IN_COMMAND')


class MsgByte:
    def __init__(self, csv_line):
        parsed_data = csv_line.split(',')
        self.timestamp = parsed_data[0]
        self.tx = parsed_data[1] == 'TX'
        self.byte = int(parsed_data[2], 0)

class HandshakeCommand:
    HANDSHAKE_CNT_TRIGGER = 20
    def __init__(self):
        self.__handshake_cnt = 0
        self.hand = 0

    def feed(self, byte):
        if byte == 0x55:
            self.__handshake_cnt = self.__handshake_cnt + 1

            if self.__handshake_cnt > self.HANDSHAKE_CNT_TRIGGER:
                return True
        else:
            self.hand = self.__handshake_cnt
            self.__handshake_cnt = 0

        return False

class GenericCommand:
    HEADER_SIZE = 4
    def __init__(self):
        self.__byte_idx = 0
        self.__header = bytearray(b'\x00' * self.HEADER_SIZE)

        self.id = 0
        self.checksum  = 0
        self.payload_len = 0
        self.payload = bytearray()

    def __repr__(self):
        return f"GenericHostCommand [id: {hex(self.id)}, checksum: {self.checksum}, len: {self.payload_len}]"

    def feed(self, byte):
        # Acquire command's header
        if self.__byte_idx < self.HEADER_SIZE:
            self.__header[self.__byte_idx] = byte

            # Full header has been acuired so extract information from it
            if self.__byte_idx == (self.HEADER_SIZE - 1):
                self.id = self.__header[0]
                self.checksum = self.__header[1]
                self.payload_len = int.from_bytes(self.__header[2:4], 'little')
                # Command doesn't have any payload so parsing is done
                if self.payload_len == 0:
                    return True

        # Acquire command's payload
        if self.__byte_idx >= self.HEADER_SIZE:
            self.payload.append(byte)

            # All allowed data has been acuired so parsing is done
            if self.__byte_idx == self.payload_len + (self.HEADER_SIZE - 1):
                return True

        self.__byte_idx = self.__byte_idx + 1
        # Command packet is currently being assembled so more data is required
        return False

class BLCommand:
    def __init__(self, name, id, fields):
        self.command_name = name
        self.id = id
        self.fields = fields

class CommandTranslator:
    def __init__(self, commands_list):
        self.commands_list = commands_list

    def translate(self, generic_command):
        passed_id = generic_command.id


def main():
    csv_path = '/home/jatsekku/Desktop/boot.csv'

    generic_command = GenericCommand()
    handshake_command = HandshakeCommand()
    last_handshake_detection = False
    cnt = 0

    with open(csv_path, 'r') as csv_file:
        for csv_line in csv_file:
            msg = MsgByte(csv_line)

            # Always look for handshake
            handshake_detected = handshake_command.feed(msg.byte)

            if handshake_detected is False:
                # If there was handshake - print it out and reset object
                if last_handshake_detection is True:
                   print('handshake', msg.byte, handshake_command.hand)
                   handshake_command = HandshakeCommand()
                   # Reset generic command object at the end of handshae block
                   generic_command = GenericCommand()

                # If there is no handshake - try to assembly generic command
                command_detected = generic_command.feed(msg.byte)
                 # Generic command has been assembled
                if command_detected is True:
                    print(generic_command)
                     # Reset generic command object
                    generic_command = GenericCommand()

            last_handshake_detection = handshake_detected

main()
