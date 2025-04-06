from dataclasses import dataclass
import struct

SUPPORTED_VERSION = 4
UNSUPPORTED_VERSION = 35


@dataclass
class RequestMessage:
    message_size: int
    api_key: int
    api_version: int
    correlation_id: int

    @staticmethod
    def from_bytes(data: int) -> "RequestMessage":
        if len(data) < 12:
            raise ValueError("Not enough bytes to parse RequestMessage")
        
        # '>' Big endian
        # 'I' Unsigned int (4 bytes)
        # 'H' Unsigned short (2 bytes)
        message_size = struct.unpack(">I", data[:4])[0]
        api_key = struct.unpack(">H", data[4:6])[0]
        api_version = struct.unpack(">H", data[6:8])[0]
        correlation_id = struct.unpack(">I", data[8:12])[0]

        return RequestMessage(message_size, api_key, api_version, correlation_id)
    
    def check_version_error_code(self, supported_version: int) -> int:
        if self.api_version == supported_version:
            return 0
        return UNSUPPORTED_VERSION
    
    


@dataclass
class ResponseMessage:
    message_size: int = 0
    correlation_id: int = 0
    error_code: int = 0

    @staticmethod
    def from_request(request: RequestMessage) -> "ResponseMessage":
        return ResponseMessage(
            message_size=request.message_size,
            correlation_id=request.correlation_id,
            error_code=request.check_version_error_code(SUPPORTED_VERSION)
        )
    
    
    def to_bytes(self) -> bytes:
        
        return struct.pack(
            ">IIH",
            self.message_size,
            self.correlation_id,
            self.error_code,
        )