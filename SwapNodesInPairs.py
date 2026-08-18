# =============================================================================
# SWAP NODES IN PAIRS
# =============================================================================
# PROBLEM: Given a linked list, swap every two adjacent nodes and return
# its head. You must solve it WITHOUT modifying the values in the list's
# nodes (only the nodes themselves may be changed, i.e. rewire pointers).
#
# EXAMPLES:
#   [1,2,3,4]  ->  [2,1,4,3]
#   []         ->  []
#   [1]        ->  [1]
#   [1,2,3]    ->  [2,1,3]
#
# WHY IS "JUST SWAP THE VALUES" NOT ALLOWED?
#   - It's the easy way out, and LeetCode explicitly forbids it here.
#   - The real skill being tested is POINTER REWIRING: rearranging the
#     actual node objects, not their data.
#
# THE NAIVE APPROACH (still valid, but let's do it right):
#   Swap the .val fields of each pair -- O(n) and trivial, but violates
#   the "don't modify node values" constraint. Interviewers want to see
#   you rewire next pointers instead.
#
# THE SMART APPROACH:
#   Use a DUMMY HEAD node + iterate two nodes at a time, relinking
#   pointers as you go: O(n) time, O(1) extra space (O(n) if recursive).
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- Dummy head + relink two nodes at a time:
#
# KEY IDEA: Every swap needs THREE pointers in play: the node BEFORE the
# pair (so we can point it at the new first node), and the pair itself
# (first, second). A dummy head handles the very first swap cleanly, so
# we never need special-case code for "swapping at the front of the list."
#
# STEP 1 -- Create a dummy node pointing at head.
#   dummy -> 1 -> 2 -> 3 -> 4
#   This gives us something to call "prev" before the real head even
#   exists, so the first pair swaps the same way every other pair does.
#
# STEP 2 -- Walk the list two nodes at a time.
#   Keep a "prev" pointer that always sits just before the current pair.
#   prev starts at dummy.
#
# STEP 3 -- For each pair (first, second), rewire FOUR pointers in order:
#   Let first  = prev.next
#   Let second = first.next
#
#   a) prev.next   = second        # prev now points to the new first node
#   b) first.next  = second.next   # first (now second in order) points past the pair
#   c) second.next = first         # second (now first in order) points at first
#   d) prev        = first         # move prev forward to the end of the swapped pair
#
# STEP 4 -- Advance to the next pair.
#   The loop continues while prev.next and prev.next.next both exist
#   (i.e. there's a full pair left to swap). Stop on a lone leftover node.
#
# STEP-BY-STEP with [1,2,3,4]:
#
#   dummy -> 1 -> 2 -> 3 -> 4          prev = dummy
#
#   Pair (1,2): first=1, second=2
#     prev.next = 2      -> dummy -> 2 -> 1 -> 3 -> 4  (1.next still old)
#     first.next = 3     -> dummy -> 2 -> 1 -> 3 -> 4  (1 now points to 3)
#     second.next = 1    -> dummy -> 2 -> 1 -> 3 -> 4  (2 now points to 1)
#     prev = first (1)   -> prev is now node 1
#
#   Pair (3,4): first=3, second=4
#     prev.next = 4       -> dummy -> 2 -> 1 -> 4 -> 3
#     first.next = None   -> 3.next = 4.next (None)
#     second.next = 3     -> 4 -> 3
#     prev = first (3)    -> prev is now node 3
#
#   No pair left (prev.next is None) -> loop ends.
#
#   Result: dummy.next = 2 -> 1 -> 4 -> 3  ✓

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def swap_pairs(head):
    dummy = ListNode(0, head)   # dummy simplifies swapping the very first pair
    prev = dummy

    while prev.next and prev.next.next:
        first  = prev.next
        second = first.next

        # Rewire the three pointers involved in this pair
        prev.next   = second        # a) prev points to what will be the new front
        first.next  = second.next   # b) first leapfrogs past second
        second.next = first         # c) second now points back at first

        prev = first                # d) move prev to the end of this swapped pair

    return dummy.next


# --- Helpers for testing ---
def build_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(to_list(swap_pairs(build_list([1, 2, 3, 4]))))   # -> [2,1,4,3]
print(to_list(swap_pairs(build_list([]))))              # -> []
print(to_list(swap_pairs(build_list([1]))))              # -> [1]
print(to_list(swap_pairs(build_list([1, 2, 3]))))        # -> [2,1,3]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# No classes needed -- a linked list node is just { val, next }.
# The pointer-rewiring logic is identical to Python.
#
# function ListNode(val, next) {
#     this.val = val === undefined ? 0 : val;
#     this.next = next === undefined ? null : next;
# }
#
# function swapPairs(head) {
#     const dummy = new ListNode(0, head);
#     let prev = dummy;
#
#     while (prev.next && prev.next.next) {
#         const first  = prev.next;
#         const second = first.next;
#
#         prev.next   = second;
#         first.next  = second.next;
#         second.next = first;
#
#         prev = first;
#     }
#
#     return dummy.next;
# }


# =============================================================================
# 3. JAVA
# =============================================================================
# Standard LeetCode ListNode definition. Same four-pointer rewire.
#
# class ListNode {
#     int val;
#     ListNode next;
#     ListNode(int val) { this.val = val; }
#     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
# }
#
# class Solution {
#     public ListNode swapPairs(ListNode head) {
#         ListNode dummy = new ListNode(0, head);
#         ListNode prev = dummy;
#
#         while (prev.next != null && prev.next.next != null) {
#             ListNode first  = prev.next;
#             ListNode second = first.next;
#
#             prev.next   = second;
#             first.next  = second.next;
#             second.next = first;
#
#             prev = first;
#         }
#
#         return dummy.next;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Use raw pointers (or smart pointers if preferred). Same rewiring order.
#
# struct ListNode {
#     int val;
#     ListNode *next;
#     ListNode(int x) : val(x), next(nullptr) {}
#     ListNode(int x, ListNode *n) : val(x), next(n) {}
# };
#
# ListNode* swapPairs(ListNode* head) {
#     ListNode dummy(0, head);
#     ListNode* prev = &dummy;
#
#     while (prev->next && prev->next->next) {
#         ListNode* first  = prev->next;
#         ListNode* second = first->next;
#
#         prev->next   = second;
#         first->next  = second->next;
#         second->next = first;
#
#         prev = first;
#     }
#
#     return dummy.next;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Same pattern, just C# class syntax for the node.
#
# public class ListNode {
#     public int val;
#     public ListNode next;
#     public ListNode(int val = 0, ListNode next = null) {
#         this.val = val;
#         this.next = next;
#     }
# }
#
# public class Solution {
#     public ListNode SwapPairs(ListNode head) {
#         ListNode dummy = new ListNode(0, head);
#         ListNode prev = dummy;
#
#         while (prev.next != null && prev.next.next != null) {
#             ListNode first  = prev.next;
#             ListNode second = first.next;
#
#             prev.next   = second;
#             first.next  = second.next;
#             second.next = first;
#
#             prev = first;
#         }
#
#         return dummy.next;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Structs and pointers stand in for classes. Same four-line rewire.
#
# type ListNode struct {
#     Val  int
#     Next *ListNode
# }
#
# func swapPairs(head *ListNode) *ListNode {
#     dummy := &ListNode{Next: head}
#     prev := dummy
#
#     for prev.Next != nil && prev.Next.Next != nil {
#         first  := prev.Next
#         second := first.Next
#
#         prev.Next   = second
#         first.Next  = second.Next
#         second.Next = first
#
#         prev = first
#     }
#
#     return dummy.Next
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust's ownership rules make raw linked-list rewiring painful, so LeetCode's
# Rust signature uses Option<Box<ListNode>>. We take ownership and hand
# ownership back at each step instead of "pointer swapping."
#
# #[derive(PartialEq, Eq, Clone, Debug)]
# pub struct ListNode {
#     pub val: i32,
#     pub next: Option<Box<ListNode>>,
# }
#
# impl ListNode {
#     fn new(val: i32) -> Self {
#         ListNode { val, next: None }
#     }
# }
#
# pub fn swap_pairs(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
#     match head {
#         None => None,
#         Some(mut first) => {
#             match first.next.take() {
#                 None => Some(first),               // odd one out, nothing to swap
#                 Some(mut second) => {
#                     first.next = swap_pairs(second.next.take()); // recurse on the rest
#                     second.next = Some(first);       // second now points at first
#                     Some(second)                      // second becomes the new head of this pair
#                 }
#             }
#         }
#     }
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Classes are reference types in Swift, so pointer-style rewiring works
# just like Java/C#.
#
# public class ListNode {
#     public var val: Int
#     public var next: ListNode?
#     public init(_ val: Int) { self.val = val; self.next = nil }
# }
#
# func swapPairs(_ head: ListNode?) -> ListNode? {
#     let dummy = ListNode(0)
#     dummy.next = head
#     var prev = dummy
#
#     while let first = prev.next, let second = first.next {
#         prev.next   = second
#         first.next  = second.next
#         second.next = first
#
#         prev = first
#     }
#
#     return dummy.next
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Same dummy-head pattern; Kotlin's nullable types (?) stand in for
# Java's null checks.
#
# class ListNode(var `val`: Int) {
#     var next: ListNode? = null
# }
#
# fun swapPairs(head: ListNode?): ListNode? {
#     val dummy = ListNode(0).apply { next = head }
#     var prev = dummy
#
#     while (prev.next != null && prev.next?.next != null) {
#         val first  = prev.next!!
#         val second = first.next!!
#
#         prev.next   = second
#         first.next  = second.next
#         second.next = first
#
#         prev = first
#     }
#
#     return dummy.next
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# attr_accessor generates the val/next getters and setters.
# Same four-pointer rewire as every other language.
#
# class ListNode
#   attr_accessor :val, :next
#   def initialize(val = 0, nxt = nil)
#     @val = val
#     @next = nxt
#   end
# end
#
# def swap_pairs(head)
#   dummy = ListNode.new(0, head)
#   prev = dummy
#
#   while prev.next && prev.next.next
#     first  = prev.next
#     second = first.next
#
#     prev.next   = second
#     first.next  = second.next
#     second.next = first
#
#     prev = first
#   end
#
#   dummy.next
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use a DUMMY HEAD + ITERATIVE PAIR REWIRING (Rust shows
# the idiomatic recursive alternative too):
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. Create a dummy node pointing at head.                       │
#   │       Lets the first pair swap the same way as every other pair. │
#   │                                                                  │
#   │  2. prev starts at dummy. Loop while a full pair remains:       │
#   │       prev.next != null AND prev.next.next != null              │
#   │                                                                  │
#   │  3. For each pair (first, second), rewire FOUR pointers:        │
#   │       prev.next   = second                                       │
#   │       first.next  = second.next                                  │
#   │       second.next = first                                        │
#   │       prev         = first   (advance past the swapped pair)     │
#   │                                                                  │
#   │  4. Return dummy.next (the new head of the list).               │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY A DUMMY HEAD?
#   Without it, swapping the very first pair requires special-casing
#   "update the function's head pointer" separately from every other
#   swap. The dummy node turns that special case into an ordinary one.
#
# !! COMMON MISTAKE !!
#   Rewiring pointers in the wrong ORDER overwrites a link before you've
#   saved it. Always capture `first` and `second` BEFORE touching any
#   .next pointers, and only then reassign prev.next / first.next /
#   second.next in that sequence.
#
# Time complexity:  O(n) -- each node is visited and relinked once
# Space complexity: O(1) iterative (just a few pointers);
#                    O(n) recursive (Rust version) due to the call stack
# =============================================================================
