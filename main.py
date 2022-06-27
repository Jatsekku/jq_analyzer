import time
import sys
import inspect

import commands

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

    def raw(self):
        return self.__header + self.payload

class CommandTranslator:
    def __init__(self, cmds_module = commands):
        cmds_classes = self.extract_classes(cmds_module)
        self._cmds_dict = self.generate_dict(cmds_classes)

    @staticmethod
    def extract_classes(module):
        pred = lambda m: inspect.isclass(m) and m.__module__ == module.__name__
        name_and_cls_tuples = inspect.getmembers(module, pred)
        return [tuple[1] for tuple in name_and_cls_tuples]

    @staticmethod
    def generate_dict(cmds_classes):
        dict = {}
        for cmd_cls in cmds_classes:
            cmd_id = cmd_cls.id.default
            if isinstance(cmd_id, int):
                dict[cmd_id] = cmd_cls
        return dict

    def translate(self, generic_cmd):
        cmd_id = generic_cmd.id
        try:
            cmd_cls = self._cmds_dict[cmd_id]
            return cmd_cls(generic_cmd.raw())
        except KeyError:
            return commands.UnknownCommand(id = cmd_id)


def main():
    csv_path = '/home/jatsekku/Desktop/boot.csv'

    generic_cmd = GenericCommand()
    handshake_cmd = HandshakeCommand()
    cmds_translator = CommandTranslator()

    last_handshake_detection = False
    cnt = 0

    with open(csv_path, 'r') as csv_file:
        for csv_line in csv_file:
            msg = MsgByte(csv_line)

            # Always look for handshake
            handshake_detected = handshake_cmd.feed(msg.byte)

            if handshake_detected is False:
                # If there was handshake - print it out and reset object
                if last_handshake_detection is True:
                   print('handshake', msg.byte, handshake_cmd.hand)
                   handshake_cmd = HandshakeCommand()
                   # Reset generic command object at the end of handshae block
                   generic_cmd = GenericCommand()

                # If there is no handshake - try to assembly generic command
                command_detected = generic_cmd.feed(msg.byte)
                 # Generic command has been assembled
                if command_detected is True:
                    packet = cmds_translator.translate(generic_cmd)
                    packet.remove_payload()
                    packet.show()
                     # Reset generic command object
                    generic_cmd = GenericCommand()

            last_handshake_detection = handshake_detected

main()
