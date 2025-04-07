from dataclasses import dataclass

SUPPORTED_VERSION = 4
UNSUPPORTED_VERSION = 35
HEADER_SIZE = 8

@dataclass
class RequestMessage:
    api_key: int
    api_version: int
    correlation_id: int
    client_id: str

    @staticmethod
    def from_bytes(data: int) -> "RequestMessage":
        if len(data) < HEADER_SIZE: 
            raise ValueError("Not enough bytes to parse RequestMessage")
        
        api_key = int.from_bytes(data[:2], byteorder="big", signed=True)
        api_version = int.from_bytes(data[2:4], byteorder="big", signed=True)
        correlation_id = int.from_bytes(data[4:HEADER_SIZE], byteorder="big", signed=True)
        client_id =  bytes.decode(data[HEADER_SIZE:], "utf-8")

        return RequestMessage(api_key, api_version, correlation_id, client_id)
    
    def check_version_error_code(self, supported_version: int) -> int:
        if self.api_version in [0, 1, 2, 3, 4]:
            return 0
        return UNSUPPORTED_VERSION
    
    


@dataclass
class ResponseMessage:
    correlation_id: int = 0
    error_code: int = 0
    api_key: int = 0

    @staticmethod
    def from_request(request: RequestMessage) -> "ResponseMessage":
        return ResponseMessage(
            correlation_id=request.correlation_id,
            error_code=request.check_version_error_code(SUPPORTED_VERSION),
            api_key=request.api_key
        )
    
    
    def to_bytes(self) -> bytes:
        min_version = 0
        max_version = 4
        num_of_api_keys = 2
        throttle_time_ms = 0
        tag_buffer = b'\x00'

        body = (
            self.correlation_id.to_bytes(4, byteorder="big", signed=True) +
            self.error_code.to_bytes(2, byteorder="big", signed=True) +
            num_of_api_keys.to_bytes(1, byteorder="big", signed=True) +
            self.api_key.to_bytes(2, byteorder="big", signed=True) +
            min_version.to_bytes(2, byteorder="big", signed=True) +
            max_version.to_bytes(2, byteorder="big", signed=True) +
            tag_buffer +
            throttle_time_ms.to_bytes(4, byteorder="big", signed=True) +
            tag_buffer
        )

        message_size = len(body).to_bytes(4, byteorder="big", signed=True)
        
        return message_size + body
