from enum import Enum

CommandState = Enum('NEW_COMMAND', 'IN_COMMAND')


class MsgByte:
    def __init__(self, csv_line):
        parsed_data = csv_line.split(',')
        self.timestamp = parsed_data[0]
        self.tx = parsed_data[1] == 'TX'
        self.value = int(parsed_data[2], 0)

class GenericCommand:
    HEADER_BYTE_SIZE = 4
    def __init__(self):
        self.__byte_idx = 0
        # 4-elements bytearray for command's header (always 4 bytes)
        self.__header = bytearray('\x00' * HEADER_BYTE_SIZE)

        self.command_id = 0
        self.checksum  = 0
        self.payload_len = 0
        self.payload = bytearray()

    def feed(self, byte):
        # Acquire command's header
        if self.__byte_idx < HEADER_BYTE_SIZE:
            self.__header[self.__byte_idx] = byte
        # Extract key information from header
        elif self.__byte_idx == HEADER_BYTE_SIZE:
            self.command_id = int.from_bytes(self.__header[0], 'little')
            self.checksum = int.from_bytes(self.__header[1], 'little')
            self.payload_len = int.from_bytes(self.__header[2:3], 'little')
            # Command doesn't have any payload so parsing is done
            if self.payload_len == 0:
                return False
        # Acquire command's header
        else:
            self.payload.extend(byte)
            # All allowed data has been acuired so parsing is done
            if self.__byte_idx == self.payload_len + HEADER_BYTE_SIZE:
                return False

        self.__byte_idx = self_byte_idx + 1
        # Command packet is currently being assembled so more data is required
        return True


class CommandParser:
    def __init__(self):
        self.byte_counter = 0
        self.cmd_id = {
            'handshake' : b'\x55',
            'get_boot_info' : b'\x10',
            'load_boot_header' : b'\x11',
            'load_segment_header' : b'\x17',
            'load_segment_data' : b'\x18',
            'check_image' : b'\x19',
            'mem_write' : b'\x50',
            'read_jedecid' : b'\x36',
            'flash_erase' : b'\x30',
            'flash_write' : b'\x31',
            'flash_write_check' : b'\x3A',
            'xip_read_start' : b'\x60',
            'flash_xip_readsha' : b'\x3E',
            'xip_read_finish' : b'\x61',
        }

    def parse(self, byte, state):
        if state == CommandState.NEW_COMMAND:
            self.cmd_id = byte
            self.byte_counter = 1

def main():
    csv_path = '/home/jatsekku/Desktop/boot.csv'

    handshake_detected = False
    handshake_probability_cnt = 0
    last_msg = None

    with open(csv_path, 'r') as csv_file:
        for csv_line in csv_file:
            current_msg = MsgByte(csv_line)

            # Handle handshake
            if current_msg.value == 0x55:
                handshake_probability_cnt = handshake_probability_cnt + 1
                if handshake_probability_cnt > 30:
                    handshake_detected = True

            else:
                if handshake_detected is True:
                    print('handshake', handshake_probability_cnt)
                    handshake_detected = False
                else:

                    #handle other
                    pass
                handshake_probability_cnt = 0

            # if last_msg == 0x55 and current_msg.value != 0x55 and handshake_cmd:
            #     print("handshake")
            #     handshake_cmd = False
            #
            # last_msg = current_msg.value





main()
