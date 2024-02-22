""" powermon / ports / serialport.py """
import logging
import time

import serial
import asyncio

from powermon.commands.command import Command, CommandType
from powermon.commands.result import Result
from powermon.dto.portDTO import PortDTO
from powermon.ports.abstractport import AbstractPort
from powermon.ports.porttype import PortType
from powermon.protocols import get_protocol_definition

log = logging.getLogger("SerialPort")


class SerialPort(AbstractPort):
    """ serial port object - normally a usb to serial adapter """

    def __str__(self):
        return f"SerialPort: {self.path=}, {self.baud=}, protocol:{self.protocol}, {self.serial_port=}, {self.error_message=}"

    @classmethod
    def from_config(cls, config=None):
        log.debug("building serial port. config:%s", config)
        path = config.get("path", "/dev/ttyUSB0")
        baud = config.get("baud", 2400)
        # get protocol handler, default to PI30 if not supplied
        protocol = get_protocol_definition(protocol=config.get("protocol", "PI30"))
        return cls(path=path, baud=baud, protocol=protocol)

    def __init__(self, path, baud, protocol) -> None:
        super().__init__(protocol=protocol)
        self.port_type = PortType.SERIAL
        self.path = path
        self.baud = baud
        self.serial_port = None
        self.is_protocol_supported()
        # self.error_message = None

    def to_dto(self) -> PortDTO:
        dto = PortDTO(type="serial", path=self.path, baud=self.baud, protocol=self.protocol.to_dto())
        return dto

    def is_connected(self):
        return self.serial_port is not None and self.serial_port.is_open

    async def connect(self) -> int:
        log.debug("usbserial port connecting. path:%s, baud:%s", self.path, self.baud)
        try:
            self.serial_port = serial.Serial(port=self.path, baudrate=self.baud, timeout=1, write_timeout=1)
            log.debug(self.serial_port)
        except ValueError as e:
            log.error("Incorrect configuration for serial port: %s", e)
            self.error_message = str(e)
            self.serial_port = None
        except serial.SerialException as e:
            log.error("Error opening serial port: %s", e)
            self.error_message = str(e)
            self.serial_port = None
        return self.is_connected()

    async def disconnect(self) -> None:
        log.debug("usbserial port disconnecting")
        if self.serial_port is not None:
            self.serial_port.close()
        self.serial_port = None

    async def send_and_receive(self, command: Command) -> Result:
        full_command = command.full_command
        response_line = None
        log.info("port: %s, full_command: %s", self.serial_port, full_command)
        if not self.is_connected():
            raise RuntimeError("Serial port not open")
        try:
            log.debug("Executing command via usbserial...")
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            # Process i/o differently depending on command type
            command_defn = command.command_definition
            match command_defn.command_type:
                case CommandType.VICTRON_LISTEN:
                    # this command type doesnt need to send a command, it just listens on the serial port
                    _lines = 30
                    log.debug("case: CommandType.VICTRON_LISTEN, listening for %i lines", _lines)
                    response_line = b""
                    for _ in range(_lines):
                        _response = self.serial_port.read_until(b"\n")
                        response_line += _response
                case CommandType.SERIAL_READONLY:
                    # read until no more data
                    log.debug("CommandType.SERIAL_READONLY")
                    response_line = b""
                    while True:
                        await asyncio.sleep(0.2)  # give serial port time to receive the data
                        to_read = self.serial_port.in_waiting
                        log.debug("bytes waiting: %s", to_read)
                        if to_read == 0:
                            break
                        # got some data to read
                        response_line += self.serial_port.read(to_read)
                case CommandType.SERIAL_READ_UNTIL_DONE:
                    # this case reads until no more to read or timeout
                    log.debug("case: CommandType.SERIAL_READ_UNTIL_DONE")
                    response_line = b""
                    self.serial_port.timeout = 0.5
                    self.serial_port.write_timeout = 1
                    self.serial_port.reset_input_buffer()
                    self.serial_port.reset_output_buffer()
                    c = self.serial_port.write(full_command)
                    log.debug("wrote %s bytes", c)
                    self.serial_port.flush()
                    # read until no more data
                    while True:
                        # await asyncio.sleep(0.5)  # give serial port time to receive the data
                        time.sleep(0.5)
                        to_read = self.serial_port.in_waiting
                        log.debug("bytes waiting %s", to_read)
                        if to_read == 0:
                            break
                        # got some data to read
                        response_line += self.serial_port.read(to_read)
                case _:
                    # default processing
                    c = self.serial_port.write(full_command)
                    log.debug("Default serial s&r. Wrote %i bytes", c)
                    self.serial_port.flush()
                    time.sleep(0.1)  # give serial port time to receive the data
                    response_line = self.serial_port.read_until(b"\r")
            log.info("serial response was: %s", response_line)
            # response = self.get_protocol().check_response_and_trim(response_line)
            result = command.build_result(raw_response=response_line, protocol=self.protocol)
            return result
        except Exception as e:
            log.warning("Serial read error: %s", e)
            result.error = True
            result.error_messages.append(f"Serial read error {e}")
            self.disconnect()
            return result
