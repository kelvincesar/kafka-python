[![progress-banner](https://backend.codecrafters.io/progress/kafka/5d77fb0e-d56c-4c8a-9b9a-7b81dc48ead4)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Kafka" Challenge](https://codecrafters.io/challenges/kafka).

In this challenge, you'll build a toy Kafka clone that's capable of accepting
and responding to APIVersions & Fetch API requests. You'll also learn about
encoding and decoding messages using the Kafka wire protocol. You'll also learn
about handling the network protocol, event loops, TCP sockets and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

## Kafka

### Request message

A request message has three parts:

- message_size
- Header
- Body

And here's what the request header looks like (in this stage, we're using request header v2):

Field	Data type	Description
* request_api_key	INT16	The API key for the request
* request_api_version	INT16	The version of the API for the request
* correlation_id	INT32	A unique identifier for the request
* client_id	NULLABLE_STRING	The client ID for the request
* TAG_BUFFER	COMPACT_ARRAY	Optional tagged fields

```sh
00 00 00 23  // message_size:        35
00 12        // request_api_key:     18
00 04        // request_api_version: 4
6f 7f c6 61  // correlation_id:      1870644833
```

```sh
echo -n "00000023001200046f7fc66100096b61666b612d636c69000a6b61666b612d636c6904302e3100" | xxd -r -p | nc localhost 9092 | hexdump -C
```