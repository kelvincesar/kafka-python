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
class KafkaKey:
    api_key: int
    min_version: int
    max_version: int

@dataclass
class KeyApiVersions(KafkaKey):
    def __init__(self, api_key: int = 18):
        super().__init__(api_key, min_version=0, max_version=4)

@dataclass
class KeyDescribeTopicPartitions(KafkaKey):
    def __init__(self, api_key: int = 75):
        super().__init__(api_key, min_version=0, max_version=0)
    
SUPPORTED_KEYS: dict[int, KafkaKey] = {
    18: KeyApiVersions(),
    75: KeyDescribeTopicPartitions()
}

@dataclass
class ResponseMessage:
    keys: list[KafkaKey]
    correlation_id: int = 0
    error_code: int = 0

    @staticmethod
    def from_request(request: RequestMessage) -> "ResponseMessage":
        kafka_key = SUPPORTED_KEYS.get(request.api_key)

        if kafka_key is None:
            raise ValueError(f"Unsupported API key: {request.api_key}")
        print(list(SUPPORTED_KEYS.values()))

        return ResponseMessage(
            correlation_id=request.correlation_id,
            error_code=request.check_version_error_code(SUPPORTED_VERSION),
            keys=list(SUPPORTED_KEYS.values()),
        )
    
    
    def to_bytes(self) -> bytes:
        throttle_time_ms = 0
        tag_buffer = b'\x00'
        
        api_keys_bytes = b""
        for key in self.keys:
            print("Key:", key.api_key)
            api_keys_bytes += key.api_key.to_bytes(2, "big", signed=True)
            api_keys_bytes += key.min_version.to_bytes(2, "big", signed=True)
            api_keys_bytes += key.max_version.to_bytes(2, "big", signed=True)
            api_keys_bytes += tag_buffer
            
           
        num_of_api_keys = (len(self.keys) + 1).to_bytes(1, byteorder="big", signed=True)
        print(f"Number of API keys: {num_of_api_keys}")
        body = (
            self.correlation_id.to_bytes(4, byteorder="big", signed=True) +
            self.error_code.to_bytes(2, byteorder="big", signed=True) +
            num_of_api_keys +
            api_keys_bytes +
            throttle_time_ms.to_bytes(4, byteorder="big", signed=True) +
            tag_buffer
        )

        message_size = len(body).to_bytes(4, byteorder="big", signed=True)
        
        return message_size + body
