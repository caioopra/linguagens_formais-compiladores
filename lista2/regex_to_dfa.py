class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
    
    def __str__(self) -> str:
        return f"{self.left} <- {self.value} -> {self.right}"

def parse_expression(regex):
    stack = []
    for symbol in regex[::-1]:
        
        
        
        print(f"stack: {[str(node) for node in stack]}")
    return stack.pop()


def process_input(regex: str) -> str:
    operators = {'*', '|', '.', '(', ')'}    
    c = regex[0]
    n = regex[1]

    count  = 1
    while n != "#":
        if c not in operators and n not in operators:
            regex = regex[:count] + "." + regex[count:]
        elif c == "*" and (n == "(" or n not in operators):
            regex = regex[:count] + "." + regex[count:]
        elif c == "*" and n.isalpha():
            regex = regex[:count] + "." + regex[count:]
        elif (c.isalpha() or c == ")" or c == "(") and n == "#":
            regex = regex[:count] + "." + regex[count:]
            
        c = regex[count]
        n = regex[count+1]
        
        count += 1
    
    if regex[-1] != "|":
        regex = regex[:-1] + "." + regex[-1:]

    return regex


def main():
    regex = "ab*(a|b)*b#"
    regex = process_input(regex)
    # root = parse_expression(regex)
    print(root)
    # calculate_nullable(root)
    # calculate_firstpos_lastpos(root)

    # followpos_dict = {pos: set() for pos in root.lastpos}
    # calculate_followpos(root, followpos_dict)

    # print("Nullable:", root.nullable)
    # print("Firstpos:", root.firstpos)
    # print("Lastpos:", root.lastpos)
    # print("Followpos:")
    # for pos, followpos in followpos_dict.items():
    #     print(f"{pos}: {followpos}")

if __name__ == "__main__":
    main()