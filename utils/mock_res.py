mock_response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\nS,S,N,S,48:00,S,N,S,4:00,S,N,N,N,N,N",
        "role": "assistant"
      },
      "logprobs": "null"
    },
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "1,2,3,4,6,7,8,12,13,14,15\nS,S,N,S,S,N,S,N,N,N,N",
        "role": "pro-factors"
      },
      "logprobs": "null"
    },
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "10,11\nS,N",
        "role": "con-factors"
      },
      "logprobs": "null"
    },
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "5,9\n48:00,4:00",
        "role": "dimensions"
      },
      "logprobs": "null"
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}
