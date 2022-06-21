from enum import Enum
import time

CommandState = Enum('NEW_COMMAND', 'IN_COMMAND')


class MsgByte:
    def __init__(self, csv_line):
        parsed_data = csv_line.split(',')
        self.timestamp = parsed_data[0]
        self.tx = parsed_data[1] == 'TX'
        self.byte = int(parsed_data[2], 0)

class GenericCommand:
    HEADER_SIZE = 4
    def __init__(self):
        self.__byte_idx = 0
        self.__header = bytearray(b'\x00' * self.HEADER_SIZE)

        self.command_id = 0
        self.checksum  = 0
        self.payload_len = 0
        self.payload = bytearray()

    def feed(self, byte):
        # Acquire command's header
        if self.__byte_idx < self.HEADER_SIZE:
            self.__header[self.__byte_idx] = byte

            # Full header has been acuired so extract information from it
            if self.__byte_idx == (self.HEADER_SIZE - 1):
                self.command_id = self.__header[0]
                self.checksum = self.__header[1]
                self.payload_len = int.from_bytes(self.__header[2:4], 'little')
                # Command doesn't have any payload so parsing is done
                if self.payload_len == 0:
                    return False

        # Acquire command's payload
        if self.__byte_idx >= self.HEADER_SIZE:
            self.payload.append(byte)
            
            # All allowed data has been acuired so parsing is done
            if self.__byte_idx == self.payload_len + (self.HEADER_SIZE - 1):
                return False

        self.__byte_idx = self.__byte_idx + 1
        # Command packet is currently being assembled so more data is required
        return True

    def __repr__(self):
        return f"GenericHostCommand [id: {hex(self.command_id)}, checksum: {self.checksum}, len: {self.payload_len}]"

def main():
    csv_path = '/home/jatsekku/Desktop/boot.csv'

    handshake_detected = False
    handshake_probability_cnt = 0
    last_msg = None
    new_command = True
    command = GenericCommand()
    data_request = True

    with open(csv_path, 'r') as csv_file:
        for csv_line in csv_file:
            current_msg = MsgByte(csv_line)

            # Handle handshake
            if current_msg.byte == 0x55:
                handshake_probability_cnt = handshake_probability_cnt + 1
                if handshake_probability_cnt > 30:
                    handshake_detected = True

            else:
                if handshake_detected is True:
                    print('handshake', handshake_probability_cnt)
                    handshake_detected = False

                if handshake_detected is False:
                    if data_request is True:
                        data_request = command.feed(current_msg.byte)
                    if data_request is False:
                        print(command)
                        command = GenericCommand()
                        data_request = True

                handshake_probability_cnt = 0

def test():
    cmd = GenericCommand()
    for i in bytearray(b'\x10\x05\x00\x00'):
        print(cmd.feed(i))
    print(cmd)

main()
