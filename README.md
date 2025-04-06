[![progress-banner](https://backend.codecrafters.io/progress/kafka/5d77fb0e-d56c-4c8a-9b9a-7b81dc48ead4)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Kafka" Challenge](https://codecrafters.io/challenges/kafka).

In this challenge, you'll build a toy Kafka clone that's capable of accepting
and responding to APIVersions & Fetch API requests. You'll also learn about
encoding and decoding messages using the Kafka wire protocol. You'll also learn
about handling the network protocol, event loops, TCP sockets and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

## Testing

```sh
codecrafters test
```

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


## API Calls

The Kafka protocol defines over 70 different APIs, all of which do different things. Here are some examples:

* Produce writes events to partitions.
* CreateTopics creates new topics.
* ApiVersions returns the broker's supported API versions.

A Kafka request specifies the API its calling by using the `request_api_key` header field.

### Message body

The schemas for the request and response bodies are determined by the API being called.

For example, here are some of the fields that the Produce request body contains:

* The name of the topic to write to.
* The key of the partition to write to.
* The event data to write.

On the other hand, the `Produce` response body contains a response code for each event. These response codes indicate if the writes succeeded.

### API versioning

Each API supports multiple versions, to allow for different schemas. Here's how API versioning works:

* Requests use the header field request_api_version to specify the API version being requested.
* Responses always use the same API version as the request. For example, a `Produce Request (Version: 3)` will always get a `Produce Response (Version: 3)` back.
* Each API's version history is independent. So, different APIs with the same version are unrelated. For example, `Produce Request (Version: 10)` is not related to `Fetch Request (Version: 10)`.