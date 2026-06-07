# =============================================================================
# ADD TWO NUMBERS (Linked Lists)
# =============================================================================
# PROBLEM: You have two numbers, but each one is stored as a linked list
# where the digits are in REVERSE order.
#
# Example: the number 342 is stored as  2 → 4 → 3
#          the number 465 is stored as  5 → 6 → 4
#
# Add them together and return the result as a linked list (also reversed).
#          342 + 465 = 807  →  stored as  7 → 0 → 8
#
# WHAT IS A LINKED LIST?
#   It's a chain of "nodes". Each node holds:
#     - a value  (e.g. the digit 2)
#     - a pointer to the NEXT node (or None if it's the last one)
#
#   Unlike a regular Python list [], you can't jump to index 3 instantly.
#   You have to walk the chain one node at a time: node → node.next → node.next.next
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS:
#
# Think of adding two numbers by hand, column by column, right to left.
# Since the digits are already stored in reverse order, the HEAD (first node)
# of each list is already the ones place — perfect, we can add straight away!
#
# STEP-BY-STEP with 342 + 465  (stored as 2→4→3  and  5→6→4):
#
#   Column 1 (ones):    2 + 5 = 7        carry = 0   → output node: 7
#   Column 2 (tens):    4 + 6 = 10       carry = 1   → output node: 0
#   Column 3 (hundreds):3 + 4 + 1(carry) = 8  carry=0 → output node: 8
#   Both lists exhausted, carry = 0 → done!
#   Result: 7 → 0 → 8  ✓  (which represents 807)
#
# KEY IDEA — the carry:
#   When a column adds up to 10 or more (e.g. 4+6=10):
#     - the current digit is  10 % 10 = 0
#     - you "carry" the      10 // 10 = 1  into the next column
#
# TRICK — the dummy head node:
#   We create a fake "dummy" node at the start of our result list.
#   This means we never have to do special handling for the very first node.
#   At the end, we return dummy.next (skipping the dummy itself).


# First, define what a linked list Node looks like:
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val    # the digit stored here
        self.next = next  # pointer to the next node (or None)


def add_two_numbers(l1, l2):
    dummy = ListNode(0)   # fake starting node (we skip this at the end)
    current = dummy       # 'current' is our pen — we write new nodes here
    carry = 0             # starts at 0; becomes 1 when a column sums to >= 10

    # keep going while either list still has digits, OR there's a leftover carry
    while l1 or l2 or carry:

        # safely get the digit from each list (use 0 if that list is exhausted)
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total = val1 + val2 + carry       # add the two digits + any carry
        carry = total // 10               # e.g. 10//10=1, 7//10=0
        digit = total % 10                # e.g. 10%10=0, 7%10=7

        current.next = ListNode(digit)    # write this digit as a new node
        current = current.next            # move our pen forward

        # advance each list pointer (if that list still has nodes left)
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next  # skip the dummy, return the real result


# --- Helper to build a linked list from a plain Python list ---
def build_list(nums):
    dummy = ListNode(0)
    cur = dummy
    for n in nums:
        cur.next = ListNode(n)
        cur = cur.next
    return dummy.next

# --- Helper to print a linked list as a plain Python list ---
def to_plain_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")

l1 = build_list([2, 4, 3])         # represents 342
l2 = build_list([5, 6, 4])         # represents 465
print(to_plain_list(add_two_numbers(l1, l2)))   # → [7, 0, 8]  (807)

l1 = build_list([0])
l2 = build_list([0])
print(to_plain_list(add_two_numbers(l1, l2)))   # → [0]

l1 = build_list([9, 9, 9, 9, 9, 9, 9])         # represents 9999999
l2 = build_list([9, 9, 9, 9])                   # represents 9999
print(to_plain_list(add_two_numbers(l1, l2)))   # → [8, 9, 9, 9, 0, 0, 0, 1]  (10009998)


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# JavaScript doesn't have a built-in LinkedList, so we define the node class
# ourselves — just like we did in Python.
#
# class ListNode {
#     constructor(val = 0, next = null) {
#         this.val = val;
#         this.next = next;
#     }
# }
#
# function addTwoNumbers(l1, l2) {
#     const dummy = new ListNode(0);
#     let current = dummy;
#     let carry = 0;
#
#     while (l1 || l2 || carry) {
#         const val1 = l1 ? l1.val : 0;
#         const val2 = l2 ? l2.val : 0;
#
#         const total = val1 + val2 + carry;
#         carry = Math.floor(total / 10);
#         const digit = total % 10;
#
#         current.next = new ListNode(digit);
#         current = current.next;
#
#         if (l1) l1 = l1.next;
#         if (l2) l2 = l2.next;
#     }
#
#     return dummy.next;
# }


# =============================================================================
# 3. JAVA
# =============================================================================
# Java requires explicit types everywhere. The logic is identical.
# 'null' in Java is the same as 'None' in Python.
#
# public class Solution {
#
#     // The node definition
#     public class ListNode {
#         int val;
#         ListNode next;
#         ListNode(int val) { this.val = val; }
#     }
#
#     public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
#         ListNode dummy = new ListNode(0);
#         ListNode current = dummy;
#         int carry = 0;
#
#         while (l1 != null || l2 != null || carry != 0) {
#             int val1 = (l1 != null) ? l1.val : 0;
#             int val2 = (l2 != null) ? l2.val : 0;
#
#             int total = val1 + val2 + carry;
#             carry = total / 10;
#             int digit = total % 10;
#
#             current.next = new ListNode(digit);
#             current = current.next;
#
#             if (l1 != null) l1 = l1.next;
#             if (l2 != null) l2 = l2.next;
#         }
#
#         return dummy.next;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# C++ uses 'struct' or 'class' to define the node. 'nullptr' = None/null.
# The '->' operator accesses members through a pointer (like Python's '.').
#
# struct ListNode {
#     int val;
#     ListNode* next;
#     ListNode(int v) : val(v), next(nullptr) {}
# };
#
# ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
#     ListNode dummy(0);
#     ListNode* current = &dummy;
#     int carry = 0;
#
#     while (l1 || l2 || carry) {
#         int val1 = l1 ? l1->val : 0;
#         int val2 = l2 ? l2->val : 0;
#
#         int total = val1 + val2 + carry;
#         carry = total / 10;
#         int digit = total % 10;
#
#         current->next = new ListNode(digit);
#         current = current->next;
#
#         if (l1) l1 = l1->next;
#         if (l2) l2 = l2->next;
#     }
#
#     return dummy.next;
# }


# =============================================================================
# 5. C#
# =============================================================================
# C# (Microsoft) looks similar to Java. 'null' instead of None.
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
#     public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {
#         ListNode dummy = new ListNode(0);
#         ListNode current = dummy;
#         int carry = 0;
#
#         while (l1 != null || l2 != null || carry != 0) {
#             int val1 = l1 != null ? l1.val : 0;
#             int val2 = l2 != null ? l2.val : 0;
#
#             int total = val1 + val2 + carry;
#             carry = total / 10;
#             int digit = total % 10;
#
#             current.next = new ListNode(digit);
#             current = current.next;
#
#             if (l1 != null) l1 = l1.next;
#             if (l2 != null) l2 = l2.next;
#         }
#
#         return dummy.next;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go uses structs for the node. The ':=' shorthand creates+assigns a variable.
# 'nil' in Go is the same as None/null.
#
# type ListNode struct {
#     Val  int
#     Next *ListNode
# }
#
# func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
#     dummy := &ListNode{}
#     current := dummy
#     carry := 0
#
#     for l1 != nil || l2 != nil || carry != 0 {
#         val1, val2 := 0, 0
#         if l1 != nil { val1 = l1.Val; l1 = l1.Next }
#         if l2 != nil { val2 = l2.Val; l2 = l2.Next }
#
#         total := val1 + val2 + carry
#         carry = total / 10
#         current.Next = &ListNode{Val: total % 10}
#         current = current.Next
#     }
#
#     return dummy.Next
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust is strict about memory ownership. Option<Box<ListNode>> means
# "either a node (Some) or nothing (None)" — Rust's safe way to do pointers.
#
# #[derive(Debug)]
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
# pub fn add_two_numbers(
#     mut l1: Option<Box<ListNode>>,
#     mut l2: Option<Box<ListNode>>,
# ) -> Option<Box<ListNode>> {
#     let mut dummy = ListNode::new(0);
#     let mut current = &mut dummy;
#     let mut carry = 0;
#
#     while l1.is_some() || l2.is_some() || carry != 0 {
#         let val1 = l1.as_ref().map_or(0, |n| n.val);
#         let val2 = l2.as_ref().map_or(0, |n| n.val);
#
#         let total = val1 + val2 + carry;
#         carry = total / 10;
#
#         current.next = Some(Box::new(ListNode::new(total % 10)));
#         current = current.next.as_mut().unwrap();
#
#         l1 = l1.and_then(|n| n.next);
#         l2 = l2.and_then(|n| n.next);
#     }
#
#     dummy.next
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift uses 'class' for the node. '?' means optional (might be nil).
# The 'defer' trick advances the pointer at the end of each loop iteration.
#
# public class ListNode {
#     public var val: Int
#     public var next: ListNode?
#     public init(_ val: Int) { self.val = val; self.next = nil }
# }
#
# func addTwoNumbers(_ l1: ListNode?, _ l2: ListNode?) -> ListNode? {
#     let dummy = ListNode(0)
#     var current: ListNode? = dummy
#     var carry = 0
#     var p1 = l1, p2 = l2
#
#     while p1 != nil || p2 != nil || carry != 0 {
#         let val1 = p1?.val ?? 0
#         let val2 = p2?.val ?? 0
#
#         let total = val1 + val2 + carry
#         carry = total / 10
#
#         current?.next = ListNode(total % 10)
#         current = current?.next
#
#         p1 = p1?.next
#         p2 = p2?.next
#     }
#
#     return dummy.next
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Kotlin is concise and modern. '?' means nullable (might be null).
# The Elvis operator '?:' means "use this value, or 0 if it's null".
#
# class ListNode(var `val`: Int = 0, var next: ListNode? = null)
#
# fun addTwoNumbers(l1: ListNode?, l2: ListNode?): ListNode? {
#     val dummy = ListNode(0)
#     var current = dummy
#     var carry = 0
#     var p1 = l1; var p2 = l2
#
#     while (p1 != null || p2 != null || carry != 0) {
#         val val1 = p1?.`val` ?: 0
#         val val2 = p2?.`val` ?: 0
#
#         val total = val1 + val2 + carry
#         carry = total / 10
#
#         current.next = ListNode(total % 10)
#         current = current.next!!
#
#         p1 = p1?.next
#         p2 = p2?.next
#     }
#
#     return dummy.next
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby is clean and readable. 'nil' is Ruby's version of None/null.
# '||' between two values means "use the left one, unless it's nil/false".
#
# class ListNode
#   attr_accessor :val, :next_node
#   def initialize(val = 0, next_node = nil)
#     @val = val
#     @next_node = next_node
#   end
# end
#
# def add_two_numbers(l1, l2)
#   dummy = ListNode.new(0)
#   current = dummy
#   carry = 0
#
#   while l1 || l2 || carry > 0
#     val1 = l1 ? l1.val : 0
#     val2 = l2 ? l2.val : 0
#
#     total = val1 + val2 + carry
#     carry = total / 10
#
#     current.next_node = ListNode.new(total % 10)
#     current = current.next_node
#
#     l1 = l1.next_node if l1
#     l2 = l2.next_node if l2
#   end
#
#   dummy.next_node
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the SAME core idea:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Walk both lists at the same time, one node (digit) at a time.  │
#   │                                                                  │
#   │  At each step:                                                   │
#   │    total = digit_from_l1 + digit_from_l2 + carry                │
#   │    new digit  = total % 10   (remainder after dividing by 10)   │
#   │    new carry  = total // 10  (0 or 1)                           │
#   │                                                                  │
#   │  Keep going until BOTH lists are empty AND carry is 0.          │
#   │  Use a dummy head node to make building the result list clean.  │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(max(m, n))  — m and n are the lengths of each list
# Space complexity: O(max(m, n))  — the result list is at most one node longer
#
# The +1 in space/time is for a possible final carry node
# e.g.  999 + 1 = 1000  →  result list is longer than either input!
# =============================================================================
