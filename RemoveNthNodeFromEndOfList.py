# =============================================================================
# REMOVE NTH NODE FROM END OF LIST
# =============================================================================
# PROBLEM: Given a linked list, remove the nth node from the END and return
# the updated list's head.
#
# WHAT DOES "NTH FROM THE END" MEAN?
#   List: 1 -> 2 -> 3 -> 4 -> 5
#   From the end:  5=1st, 4=2nd, 3=3rd, 2=4th, 1=5th
#   Remove n=2 from end -> remove node 4 -> list becomes 1 -> 2 -> 3 -> 5
#
# THE CHALLENGE:
#   In a singly linked list, you can only move FORWARD.
#   You don't know the length until you've walked the whole list.
#   So how do you find the nth from the end efficiently?
#
# TWO APPROACHES:
#   A) Two-pass: count the length, then remove the (length-n)th from start.
#   B) One-pass: two pointers with a gap of n (shown below -- more elegant).
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE ONE-PASS TWO-POINTER APPROACH:
#
# We use two pointers: 'fast' and 'slow', both starting at a dummy node.
#
# STEP 1: Advance 'fast' by n+1 steps.
#         (The +1 is so 'slow' stops at the node BEFORE the one to delete.)
#
# STEP 2: Move BOTH pointers forward together until 'fast' falls off the end.
#
# STEP 3: Now 'slow' is pointing to the node just BEFORE the one to delete.
#         Do slow.next = slow.next.next to skip over the target node.
#
# WHY DOES THIS WORK?
#   When fast reaches None (end of list), there's a gap of n+1 between them.
#   So slow is exactly n+1 positions behind fast's final position (None),
#   which means slow is at position (length - n) from the start --
#   exactly one node before the node we want to delete.
#
# STEP-BY-STEP with [1,2,3,4,5], n=2:
#
#   dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
#
#   Advance fast by n+1=3 steps from dummy:
#     fast starts at dummy (step 0)
#     fast -> 1  (step 1)
#     fast -> 2  (step 2)
#     fast -> 3  (step 3)
#
#   Now slow=dummy, fast=node(3). Move both until fast==None:
#     slow=1, fast=4
#     slow=2, fast=5
#     slow=3, fast=None  <- STOP
#
#   slow is at node(3). slow.next is node(4) -- the one to delete!
#   slow.next = slow.next.next  ->  node(3).next = node(5)
#   Result: 1 -> 2 -> 3 -> 5  ✓
#
# WHY THE DUMMY NODE?
#   Handles the edge case of deleting the HEAD (the first node).
#   Without dummy: if n == length (delete head), slow would be null.
#   With dummy: slow lands on dummy, and slow.next = slow.next.next
#   naturally skips the head. Clean and no special cases needed!

class ListNode:
    def __init__(self, val=0, next=None):
        self.val  = val
        self.next = next


def remove_nth_from_end(head, n):
    dummy      = ListNode(0)   # fake node before the head
    dummy.next = head
    fast       = dummy
    slow       = dummy

    # Step 1: advance fast by n+1 steps
    for _ in range(n + 1):
        fast = fast.next

    # Step 2: move both until fast falls off the end
    while fast is not None:
        fast = fast.next
        slow = slow.next

    # Step 3: slow is right before the node to delete -- skip it
    slow.next = slow.next.next

    return dummy.next   # dummy.next is the (possibly new) head


# --- Helpers ---
def build_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(to_list(remove_nth_from_end(build_list([1,2,3,4,5]), 2)))  # -> [1,2,3,5]
print(to_list(remove_nth_from_end(build_list([1]), 1)))          # -> []
print(to_list(remove_nth_from_end(build_list([1,2]), 1)))        # -> [1]
print(to_list(remove_nth_from_end(build_list([1,2]), 2)))        # -> [2]  (remove head)


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Same dummy node + two-pointer approach.
# null in JS is the same as None in Python for the end of the list.
#
# function removeNthFromEnd(head, n) {
#     const dummy = { val: 0, next: head };
#     let fast = dummy, slow = dummy;
#
#     for (let i = 0; i <= n; i++) {
#         fast = fast.next;
#     }
#
#     while (fast !== null) {
#         fast = fast.next;
#         slow = slow.next;
#     }
#
#     slow.next = slow.next.next;
#     return dummy.next;
# }


# =============================================================================
# 3. JAVA
# =============================================================================
# ListNode class is typically provided in LeetCode's Java environment.
# null is Java's equivalent of Python's None.
# The structure is identical to the JS and Python solutions.
#
# class Solution {
#     public ListNode removeNthFromEnd(ListNode head, int n) {
#         ListNode dummy = new ListNode(0);
#         dummy.next = head;
#         ListNode fast = dummy, slow = dummy;
#
#         for (int i = 0; i <= n; i++) {
#             fast = fast.next;
#         }
#
#         while (fast != null) {
#             fast = fast.next;
#             slow = slow.next;
#         }
#
#         slow.next = slow.next.next;
#         return dummy.next;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# ListNode struct is typically defined with val and *next pointer.
# nullptr is C++'s null pointer (same role as None/null).
# The -> operator accesses members through a pointer.
#
# struct ListNode {
#     int val;
#     ListNode* next;
#     ListNode(int v) : val(v), next(nullptr) {}
# };
#
# class Solution {
# public:
#     ListNode* removeNthFromEnd(ListNode* head, int n) {
#         ListNode dummy(0);
#         dummy.next = head;
#         ListNode* fast = &dummy;
#         ListNode* slow = &dummy;
#
#         for (int i = 0; i <= n; i++) {
#             fast = fast->next;
#         }
#
#         while (fast != nullptr) {
#             fast = fast->next;
#             slow = slow->next;
#         }
#
#         slow->next = slow->next->next;
#         return dummy.next;
#     }
# };


# =============================================================================
# 5. C#
# =============================================================================
# ListNode class with public int val and public ListNode next.
# null is C#'s null reference (same as Java).
#
# public class Solution {
#     public ListNode RemoveNthFromEnd(ListNode head, int n) {
#         ListNode dummy = new ListNode(0) { next = head };
#         ListNode fast = dummy, slow = dummy;
#
#         for (int i = 0; i <= n; i++) {
#             fast = fast.next;
#         }
#
#         while (fast != null) {
#             fast = fast.next;
#             slow = slow.next;
#         }
#
#         slow.next = slow.next.next;
#         return dummy.next;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# ListNode struct with Val int and Next *ListNode.
# nil is Go's null pointer.
# := creates and assigns variables (short declaration).
#
# type ListNode struct {
#     Val  int
#     Next *ListNode
# }
#
# func removeNthFromEnd(head *ListNode, n int) *ListNode {
#     dummy := &ListNode{Val: 0, Next: head}
#     fast  := dummy
#     slow  := dummy
#
#     for i := 0; i <= n; i++ {
#         fast = fast.Next
#     }
#
#     for fast != nil {
#         fast = fast.Next
#         slow = slow.Next
#     }
#
#     slow.Next = slow.Next.Next
#     return dummy.Next
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust's ownership model makes linked lists famously tricky.
# Option<Box<ListNode>> is the safe way: Some(node) or None.
# The cleanest LeetCode-friendly approach converts to a Vec, removes the
# element, then rebuilds -- avoiding borrow-checker battles with raw pointers.
#
# #[derive(Debug)]
# pub struct ListNode {
#     pub val: i32,
#     pub next: Option<Box<ListNode>>,
# }
#
# impl ListNode {
#     fn new(val: i32) -> Self { ListNode { val, next: None } }
# }
#
# pub fn remove_nth_from_end(head: Option<Box<ListNode>>, n: i32) -> Option<Box<ListNode>> {
#     // Collect all values into a Vec
#     let mut vals = Vec::new();
#     let mut cur  = &head;
#     while let Some(node) = cur {
#         vals.push(node.val);
#         cur = &node.next;
#     }
#
#     // Remove the nth from the end
#     let remove_idx = vals.len() - n as usize;
#     vals.remove(remove_idx);
#
#     // Rebuild the linked list from back to front
#     let mut result: Option<Box<ListNode>> = None;
#     for &val in vals.iter().rev() {
#         let mut node = ListNode::new(val);
#         node.next = result;
#         result = Some(Box::new(node));
#     }
#
#     result
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# ListNode class with var val: Int and var next: ListNode?.
# Optional chaining (?) handles the potential nil next pointer.
#
# public class ListNode {
#     public var val:  Int
#     public var next: ListNode?
#     public init(_ val: Int) { self.val = val; self.next = nil }
# }
#
# func removeNthFromEnd(_ head: ListNode?, _ n: Int) -> ListNode? {
#     let dummy     = ListNode(0)
#     dummy.next    = head
#     var fast: ListNode? = dummy
#     var slow: ListNode? = dummy
#
#     for _ in 0...n {
#         fast = fast?.next
#     }
#
#     while fast != nil {
#         fast = fast?.next
#         slow = slow?.next
#     }
#
#     slow?.next = slow?.next?.next
#     return dummy.next
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# ListNode class with var val: Int and var next: ListNode? = null.
# Safe call ?.next handles nullable references.
#
# class ListNode(var `val`: Int = 0, var next: ListNode? = null)
#
# fun removeNthFromEnd(head: ListNode?, n: Int): ListNode? {
#     val dummy = ListNode(0)
#     dummy.next = head
#     var fast: ListNode? = dummy
#     var slow: ListNode? = dummy
#
#     repeat(n + 1) { fast = fast?.next }
#
#     while (fast != null) {
#         fast = fast?.next
#         slow = slow?.next
#     }
#
#     slow?.next = slow?.next?.next
#     return dummy.next
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# ListNode class with attr_accessor for val and next_node.
# nil is Ruby's null. The structure is clean and readable.
#
# class ListNode
#   attr_accessor :val, :next_node
#   def initialize(val = 0, next_node = nil)
#     @val = val; @next_node = next_node
#   end
# end
#
# def remove_nth_from_end(head, n)
#   dummy          = ListNode.new(0)
#   dummy.next_node = head
#   fast           = dummy
#   slow           = dummy
#
#   (n + 1).times { fast = fast.next_node }
#
#   while fast
#     fast = fast.next_node
#     slow = slow.next_node
#   end
#
#   slow.next_node = slow.next_node.next_node
#   dummy.next_node
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All solutions (except Rust) use the DUMMY NODE + TWO POINTERS trick:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  dummy -> head -> ... -> None                                   │
#   │  fast = slow = dummy                                            │
#   │                                                                  │
#   │  1. Advance fast by n+1 steps.                                 │
#   │                                                                  │
#   │  2. Move BOTH forward until fast == None.                      │
#   │                                                                  │
#   │  3. slow is now just BEFORE the node to delete.                │
#   │     slow.next = slow.next.next  (skip the target node)         │
#   │                                                                  │
#   │  4. Return dummy.next (the real head, possibly updated).       │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY n+1 STEPS (not n)?
#   We want slow to stop at the node BEFORE the target, not ON it.
#   An extra step of gap means slow is one step behind where it needs to be.
#
# WHY THE DUMMY NODE?
#   Without it, deleting the HEAD requires a special case.
#   With dummy, slow can be at dummy when the head needs deleting,
#   and slow.next = slow.next.next cleanly removes the head -- no special case.
#
# Time complexity:  O(sz)  -- one pass through the list
# Space complexity: O(1)   -- just two pointers, no extra storage
# =============================================================================
