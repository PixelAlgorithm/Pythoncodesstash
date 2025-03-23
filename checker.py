import random
import string

def generate_key():
    segments = ['BIKE']
    
    # Second segment with H in the middle
    second_segment = random.choice(string.digits) + 'H' + random.choice(string.digits)
    segments.append(second_segment)
    
    # Third and fourth segments with 4 characters each
    segment_lengths = [4, 4]
    for length in segment_lengths:
        segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        segments.append(segment)
    
    # Last segment with 3 characters
    last_segment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    segments.append(last_segment)
    
    return '-'.join(segments)

key = generate_key()
print("Generated Key: ", key)
