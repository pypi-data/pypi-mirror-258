---

# Redis gRPC ⚡️

by Gautam Sharma https://gsharma.dev

Redis gRPC ⚡️ is a client library that emulates Redis-like features by leveraging gRPC communication. It provides a lightweight and efficient way to interact with a Redis-like server implemented using gRPC, offering developers a fast and seamless experience.

## Features

- Emulates Redis-like functionality
- Utilizes gRPC for communication
- Written in Python for ease of use and integration
- Lightweight and efficient

## Installation

To install the redisgrpc Python client library, you can use pip:

```bash
pip install  redisgrpc==0.2
```

## Usage

Here's an example demonstrating how to use the  redisgrpc client library:

```python
from __future__ import print_function
import logging
from  redisgrpc import redisgrpc as rg


def run():
    # Initialize the Client with the server port
    c = rg.Client(50051)
    # Initialize the connection
    c.init_connection()
    
    # Perform some Redis-like operations
    for idx in range(1, 10):
        k = input("Set Key: ")
        v = input("Set Value: ")
        c.set(k, v)
        # Get the cached value back
        cached_val = c.get(k)
        print("Cached value of key {} is {}".format(k, cached_val))

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig()
    # Run the example
    run()
```

## About

The redisgrpc-server is a library written purely in C++, utilizing gRPC as its communication layer. Despite its small size, this library is powerful and suitable for use in production environments. The aim is to provide developers with the best possible experience while maintaining extreme speed and efficiency.

## Contributing

Contributions to redisgrpc are welcome! Whether it's reporting bugs, suggesting new features, or contributing code, your input is valuable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

.
