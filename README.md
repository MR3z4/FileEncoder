# FileEncoder
A repository for python to encode a file with a password. it works perfectly with pytorch model weights.


<!-- USAGE EXAMPLES -->
## Usage
```python
import io
from encoder import AESCipher
enc = AESCipher('123456789')
enc.encrypt_file('test.pth')
decoded_bytes = ec.decrypt_file('test.enc')
import torch
torch.load(io.BytesIO(decoded_bytes))
```
