import uuid, base64
import binascii

class UUID:
    @classmethod
    def id(cls):
        id = str(uuid.uuid4())
        print(id)
        # id = cls.hex_to_str(id)
        # id = binascii.a2b_base64(id.encode('utf-8'))
        # id = base64.b64encode(id)
        # id = base64.urlsafe_b64encode(id)
        # id = str(id, 'utf-8')
        # id = id.decode('utf-8')
        id = id.replace('+', '_')
        id = id.replace('/', '_')
        id = id.replace('=', '_')
        id = id.replace('-', '.')
        # print(id)
        # print(len(id))
        # exit()
        return str(id)

    def str_to_hex(s):
        return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

    def bin_to_str(s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split('')]])

    def hex_to_str(s):
        return ''.join([chr(i) for i in [int(b, 16) for b in s.split('')]])