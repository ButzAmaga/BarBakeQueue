import chardet

# Read the content of the original JSON file
with open('db_data.json', 'rb') as f:
    content = f.read()

# Detect the encoding
result = chardet.detect(content)
encoding = result['encoding']
print(f"Detected encoding: {encoding}")

# Decode the content with the detected encoding
decoded_content = content.decode(encoding)

# Write the decoded content back to a UTF-8 encoded file
with open('db_data_utf8.json', 'w', encoding='utf-8') as f:
    f.write(decoded_content)
