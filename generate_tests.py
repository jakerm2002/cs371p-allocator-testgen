import random

NUM_TESTS = 24
HEAP_SIZE = 1000
OBJECT_SIZE = 8
TEST_LENGTH = 10
SENTINEL_SIZE = 2 * 4 # size of start & end sentinel
MIN_BLOCK_SIZE = OBJECT_SIZE + 8;

# determine a random number of objects to allocate
def allocate(cur_heap_space, max_bytes):
    
    max_objects = max_bytes // OBJECT_SIZE
    return random.randint(1, max_objects)

def getNumAllocated(blocks):
    return sum(b[1] for b in blocks)

def getBiggestFreeBlock(blocks):
    max_size = 0
    for size, isAllocated in blocks:
        if not isAllocated and size > max_size:
            max_size = size
    return max_size

def getFreeBlock(blocks, num_objects): # index of first free block
    for i, (size, isAllocated) in enumerate(blocks):
        if not isAllocated and size >= (num_objects * OBJECT_SIZE):
            return i
    return -1 # No free block found

def get_nth_allocated_block(blocks, n): # one-indexed
    return next((block for block in blocks if block[1] and not (n := n-1)), None)

# takes one index
def get_nth_allocated_block_index(blocks, n):
    return ([i for i, block in enumerate(blocks) if block[1]][n-1] if n <= len([i for i, block in enumerate(blocks) if block[1]]) else -1)

# given the nth allocated block
def free_allocated_block(blocks, n):
    if n < 1 or n > len(blocks):
        raise ValueError("Invalid block index")
    if not blocks[n-1][1]:
        raise ValueError("Block is not allocated")

    # Free the block
    blocks[n-1] = (blocks[n-1][0], False)

    # Check if adjacent blocks are free and coalesce them
    coalesced = 0
    if n > 1 and not blocks[n-2][1]:
        size = blocks[n-2][0]
        blocks.pop(n-2)
        blocks[n-2] = (blocks[n-2][0] + size + 8, False)
        n -= 1
        coalesced += 1

    if n < len(blocks) and not blocks[n][1]:
        size = blocks[n][0]
        blocks.pop(n)
        blocks[n-1] = (blocks[n-1][0] + size + 8, False)
        coalesced += 1

    return blocks, coalesced


print(NUM_TESTS)
print()
for test_number in range(0, NUM_TESTS):
    cur_heap_space = HEAP_SIZE - SENTINEL_SIZE
    blocks = [((HEAP_SIZE - SENTINEL_SIZE), False)] # size, isAllocated
    
    for process_num in range(0, TEST_LENGTH):
        max_bytes = getBiggestFreeBlock(blocks)
        if getNumAllocated(blocks) == 0: # if no allocated blocks, we can't dealloc
            num_objects = allocate(cur_heap_space, max_bytes)
            index = getFreeBlock(blocks, num_objects)
            assert(index != -1)
            blocks[index] = (blocks[index][0] - OBJECT_SIZE * num_objects - SENTINEL_SIZE, False)
            blocks.insert(index, (OBJECT_SIZE * num_objects, True))
            cur_heap_space += -(OBJECT_SIZE * num_objects + SENTINEL_SIZE)
            print(num_objects)
        else:
            if (random.choice([True, False]) and max_bytes > MIN_BLOCK_SIZE): # allocate
                num_objects = allocate(cur_heap_space, max_bytes);
                index = getFreeBlock(blocks, num_objects)
                assert(index != -1)
                blocks[index] = (blocks[index][0] - OBJECT_SIZE * num_objects - SENTINEL_SIZE, False)
                blocks.insert(index, (OBJECT_SIZE * num_objects, True))
                cur_heap_space += -(OBJECT_SIZE * num_objects + SENTINEL_SIZE)
                print(num_objects)
            else: # deallocate
                dealloc_block_num = random.randint(1, getNumAllocated(blocks))
                dealloc_block_index = get_nth_allocated_block_index(blocks, dealloc_block_num)
                block_size = blocks[dealloc_block_index][0]
                new_block, coalesced = free_allocated_block(blocks, dealloc_block_index + 1)
                block = new_block
                cur_heap_space += block_size + (8 * coalesced)
                print(-dealloc_block_num)
    if (test_number < NUM_TESTS - 1): print()