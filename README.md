# Linear Code Error Correction

A Python implementation of syndrome decoding for error detection and correction in communication channels. This library provides tools to create, encode, and decode linear codes with a focus on ASCII text transmission.

## Background

### Syndrome Decoding & Linear Codes

Linear codes are a fundamental error correction technique in coding theory. They work by adding redundant bits to messages in a mathematically structured way, allowing detection and correction of transmission errors.

Key concepts:

1. **Generator Matrix (G)**: Transforms k-bit messages into n-bit codewords
   - G is a k×n matrix where k is message length and n is codeword length
   - Encoded message: m × G = c (where m is the message and c is the codeword)

2. **Parity Check Matrix (H)**: Used for error detection
   - H is an (n-k)×n matrix
   - For valid codewords: c × H^T = 0
   - When errors occur: c × H^T = syndrome

3. **Syndrome Decoding**:
   - Syndrome = received_word × H^T
   - Non-zero syndrome indicates errors
   - Syndrome pattern uniquely identifies error location
   - Lookup syndrome in pre-computed table to find error pattern

### Error Correction Process

1. Message encoding: c = m × G
2. Transmission through noisy channel: c → r (received word)
3. Syndrome computation: s = r × H^T
4. Error pattern lookup: e = syndrome_table[s]
5. Error correction: m = r - e

## Installation

```bash
git clone https://github.com/ameanasad/syndrome-error-correction.git
cd syndrome-error-correction
pip install -r requirements.txt
```

### Simulation Results

![Simulation Results](https://github.com/AmeanAsad/Syndrome-Error-Decoding/blob/master/simulation_result.png)
*Sample simulation results with 500 words, 10 trials, comparing different code parameters*


## Usage Examples

### Basic Linear Code Operations

```python
from linear_code import LinearCode

# Create a (12,8) linear code
code = LinearCode(k=8, n=12)

# Get encoding matrices
G = code.get_generator_matrix()
H = code.get_parity_check_matrix()
syndrome_table = code.get_syndrome_decoding_table()

# Example: Encode a message
message = np.array([1, 0, 1, 1, 0, 1, 0, 1])
encoded = np.matmul(message, G) % 2  # Binary arithmetic
```

### ASCII Text Encoding/Decoding

```python
from ascii_code import AsciiCode

# Initialize ASCII encoder/decoder
ascii_code = AsciiCode(k=8, n=12)

# Encode and decode a single character
text = "A"
# Get binary representation
binary = ascii_code.ascii_to_bin[text]

# Simulate transmission error
received = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]  # Corrupted codeword
decoded = ascii_code.decode_letter(received)
print(f"Original: {text}, Decoded: {decoded}")

# Process entire string
def process_text(text, ascii_code):
    decoded_text = ""
    for char in text:
        # In real implementation, you'd include encoding and channel simulation
        received = # ... simulated received codeword
        decoded_char = ascii_code.decode_letter(received)
        decoded_text += decoded_char
    return decoded_text
```

### Error Simulation

```python
from decoding_simulation import visualization

# Basic simulation
visualization(word_limit=100, num_trials=5)

# Detailed simulation with custom parameters
visualization(
    word_limit=500,
    num_trials=10,
    error_rate=0.125,  # 12.5% bit error rate
    code_parameters=[(8,12), (8,14), (8,16)]  # Compare different code sizes
)
```

## Implementation Details

### Linear Code Class
- Implements core mathematical operations
- Generates systematic form of generator matrix
- Computes parity check matrix
- Builds syndrome lookup table

### ASCII Code Class
- Handles text-specific encoding/decoding
- Maps ASCII characters to binary vectors
- Implements syndrome decoding for error correction
- Maintains codeword dictionary

## Performance Analysis

### Error Correction Capability

The library's error correction performance depends on:
1. Code rate (k/n)
2. Minimum Hamming distance
3. Channel error rate

Typical performance metrics:
- Single error correction guaranteed
- Some double error detection capability
- Performance degrades with burst errors

### Computational Complexity

- Encoding: O(k×n) per character
- Syndrome computation: O(n×(n-k))
- Decoding table lookup: O(1)
- Total processing: O(n²) per character

## Advanced Features

### Custom Error Patterns
```python
# Define custom error patterns for testing
error_patterns = [
    [1,0,0,0,0,0,0,0],  # Single bit error
    [1,1,0,0,0,0,0,0],  # Double bit error
    [1,1,1,0,0,0,0,0],  # Triple bit error
]
```

### Performance Monitoring
```python
# Track correction success rate
success_count = 0
total_trials = 1000

for _ in range(total_trials):
    # Simulation code here
    if decoded == original:
        success_count += 1

success_rate = success_count / total_trials
```

## Limitations and Future Work

- Currently limited to binary linear codes
- Single error correction guaranteed
- Future improvements:
  - Reed-Solomon code implementation
  - Burst error handling
  - Soft-decision decoding
  - Variable code rate support

## Contributing

Contributions welcome! Areas of interest:
- Additional encoding schemes
- Performance optimizations
- Extended error pattern support
- Documentation improvements

## License

This project is licensed under the MIT License.
