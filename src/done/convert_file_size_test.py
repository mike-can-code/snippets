# Basic conversions
assert convert_file_size(size=1024, from_unit='KB', to_unit='MB') == 1.0
assert convert_file_size(size=1, from_unit='GB', to_unit='MB') == 1024.0
assert convert_file_size(size=1, from_unit='MB', to_unit='B') == 1048576

# Same unit
assert convert_file_size(size=100, from_unit='MB', to_unit='MB') == 100.0

# Zero size
assert convert_file_size(size=0, from_unit='GB', to_unit='KB') == 0.0

# Float input
assert convert_file_size(size=1.5, from_unit='GB', to_unit='MB') == 1536.0

# Case insensitivity
assert convert_file_size(size=1, from_unit='gb', to_unit='mb') == 1024.0

# Error cases
try:
    convert_file_size(size=-5, from_unit='MB', to_unit='KB')
except ValueError as e:
    print(f"✓ Caught negative size: {e}")

try:
    convert_file_size(size=100, from_unit='XB', to_unit='MB')
except ValueError as e:
    print(f"✓ Caught invalid unit: {e}")
