import math

def calculate_entropy(password):
    
    character_pool = 0
    
    if any(c.islower() for c in password):
        character_pool += 26
        
    if any(c.isupper() for c in password):
        character_pool += 26   
         
    if any(c.isdigit() for c in password):
        character_pool += 10
        
    if any(not c.isalnum() for c in password):
        character_pool += 32
    
    if character_pool ==0:
        return 0
    
    entropy = len(password)*math.log2(character_pool)
    
    return entropy

