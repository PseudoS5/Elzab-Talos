import serial


class Talos:
    def __init__(self, serial_port: str, baud: int) -> None: # default 9600,8,E,1
        self.serial_port = serial_port
        self.baud = baud

    def open(self) -> bool:
        self.serial = serial.Serial(self.serial_port, self.baud, 8, 'E', 1)
        self.serial.timeout = 3
        return self.serial.is_open
    
    def send_esc(self) -> None:
        self.serial.write([0x1B])

    def send_command(self, data: list[int]) -> None:
        self.serial.write(bytes([0x1B, *data])) # 0x1B is ESC
        self.serial.write(b'\r\n')
        self.serial.flush()


    # PRINT

    def print(self, value: str) -> None:
        self.serial.write(value.encode('latin2'))

    def println(self, value: str) -> None:
        self.serial.write(value.encode('latin2'))
        self.serial.write(b'\r\n')
        self.serial.flush()

    # CONTROL SEQUENCES

    def set_char_height(self, height: int) -> None:
        # space is (N+1)*0,125mm where N is height
        self.send_command([0x58, height + 32])

    def set_line_height(self, height: int) -> None:
        # space is (N+1)*0,125mm where N is height
        self.send_command([0x59, height + 32])

    def cut_paper(self, partial: bool = False) -> None:
        self.send_command([0x5B if partial else 0x5A])

    def print_barcode(self, height: int, numeric_mode: bool, data: str) -> None:
        # height is height*0,125mm
        if numeric_mode and len(data) % 2 != 0:
            raise ValueError('Numeric mode requires an even number')
        self.send_command([0x5C, height, 2 if numeric_mode else 1, *data.encode('ascii')])

    def feed_paper(self, lines: int) -> None:
        self.send_command([0x83, lines + 32])