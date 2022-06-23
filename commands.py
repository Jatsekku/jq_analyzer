from scapy.all import *

# ------------------------------- GetBootInfo ----------------------------------
class GetBootInfo(Packet):
    fields_desc = [XByteField('id', 0x10),
                   XByteField('rsvd', 0x00),
                   LEShortField('len', 0)]

# ------------------------------ LoadBootHeader --------------------------------
class LoadBootHeader(Packet):
    fields_desc = [XByteField('id', 0x11),
                   XByteField('rsvd', 0x00),
                   LEShortField('len', 176),
                   XStrFixedLenField('boot_header', b'', 176)]

# ------------------------------ LoadPublicKey ---------------------------------
class LoadPublicKey(Packet):
    fields_desc = [XByteField('id', 0x12),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 68),
                   XStrFixedLenField('public_key', b'', 68)]

# ------------------------------ LoadSignature ---------------------------------
#TODO
class LoadSignature(Packet):
    fields_desc = [XByteField('id', 0x14),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0),
                   XStrLenField('signature', b'',
                                length_from = lambda pkt: int(pkt.len))]

# -------------------------------- LoadAesIV -----------------------------------
class LoadAesIV(Packet):
    fields_desc = [XByteField('id', 0x16),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 20),
                   XStrFixedLenField('aes_iv', b'', 20)]

# ---------------------------- LoadSegmentHeader -------------------------------
class LoadSegmentHeader(Packet):
    fields_desc = [XByteField('id', 0x17),
                   XByteField('rsvd', 0x00),
                   LEShortField('len', 16),
                   XStrFixedLenField('seg_header', b'', 16)]

# ----------------------------- LoadSegmentData --------------------------------
#TODO
class LoadSegmentData(Packet):
    fields_desc = [XByteField('id', 0x18),
                   XByteField('rsvd', 0x00),
                   LEShortField('len', 0),
                   XStrLenField('seg_data', b'',
                                length_from = lambda pkt: int(pkt.len))]]

# -------------------------------- CheckImage ----------------------------------
class CheckImage(Packet):
    fields_desc = [XByteField('id', 0x19),
                   XByteField('rsvd', 0x00),
                   LEShortField('len', 0)]

# --------------------------------- RunImage -----------------------------------
# TODO !!!
class RunImage(Packet):
    fields_desc = [XByteField('id', 0x1A),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]


# -------------------------------- FlashErase ----------------------------------
# TODO !!!
class FlashErase(Packet):
    fields_desc = [XByteField('id', 0x30),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ------------------------------- FlashProgram ---------------------------------
# TODO !!!
class FlashProgram(Packet):
    fields_desc = [XByteField('id', 0x31),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# --------------------------------- FlashRead ----------------------------------
# TODO !!!
class FlashRead(Packet):
    fields_desc = [XByteField('id', 0x32),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ----------------------------- FlashProgramCheck ------------------------------
# TODO !!!
class FlashProgramCheck(Packet):
    fields_desc = [XByteField('id', 0x3A),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ------------------------------- FlashSetPara ---------------------------------
# TODO !!!
class FlashSetPara(Packet):
    fields_desc = [XByteField('id', 0x3B),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ------------------------------ FlashChipErase --------------------------------
# TODO !!!
class FlashChipErase(Packet):
    fields_desc = [XByteField('id', 0x3C),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ------------------------------- FlashReadSHA ---------------------------------
# TODO !!!
class FlashReadSHA(Packet):
    fields_desc = [XByteField('id', 0x3D),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ----------------------------- FlashXIPReadSHA --------------------------------
# TODO !!!
class FlashXIPReadSHA(Packet):
    fields_desc = [XByteField('id', 0x3E),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ---------------------------- FlashXIPReadStart -------------------------------
class FlashXIPReadStart(Packet):
    fields_desc = [XByteField('id', 0x60),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ---------------------------- FlashXIPReadFinish ------------------------------
class FlashXIPReadFinish(Packet):
    fields_desc = [XByteField('id', 0x3E),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

# ----------------------------- FlashReadJedecID -------------------------------
class FlashReadJedecID(Packet):
    fields_desc = [XByteField('id', 0x36),
                   XByteField('rsvd', 0x00),
                   ShortField('len', 0)]

p = LoadSignature(len = 3, signature = b'\x01\x02\x03')
print(raw(p))
p.show2()
