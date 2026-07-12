# =============================================================================
# MERGE TWO SORTED LISTS
# =============================================================================
# PROBLEM: Merge two already-sorted linked lists into one sorted linked list.
# You must REUSE the existing nodes (splice them together), not create new ones.
#
# EXAMPLES:
#   list1=[1,2,4], list2=[1,3,4]  ->  [1,1,2,3,4,4]
#   list1=[],      list2=[]       ->  []
#   list1=[],      list2=[0]      ->  [0]
#
# HOW TO THINK ABOUT IT:
#   Imagine two sorted piles of numbered cards, face-up.
#   At each step, look at the TOP card of each pile.
#   Pick the smaller one and add it to your result pile.
#   Keep going until one pile is empty, then dump the rest of the other pile.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# WE SHOW TWO APPROACHES -- iterative and recursive -- both fully explained.
#
# ─────────────────────────────────────────────────────
# APPROACH A -- Iterative (with dummy head)
# ─────────────────────────────────────────────────────
# Same dummy-head trick from problem 2 (Add Two Numbers) and problem 19.
# 'current' is our pen -- we attach nodes to it one by one.
#
# STEP-BY-STEP with list1=[1,2,4], list2=[1,3,4]:
#
#   dummy -> (empty)    current=dummy   l1=1  l2=1
#
#   l1.val(1) <= l2.val(1): attach l1(1)  current=1  l1=2  l2=1
#   l1.val(2) >  l2.val(1): attach l2(1)  current=1  l1=2  l2=3
#   l1.val(2) <= l2.val(3): attach l1(2)  current=2  l1=4  l2=3
#   l1.val(4) >  l2.val(3): attach l2(3)  current=3  l1=4  l2=4
#   l1.val(4) <= l2.val(4): attach l1(4)  current=4  l1=None  l2=4
#   l1 is None -> attach rest of l2(4)    current=4  l2=None
#   Done! Result: 1->1->2->3->4->4  ✓

class ListNode:
    def __init__(self, val=0, next=None):
        self.val  = val
        self.next = next


def merge_two_lists_iterative(list1, list2):
    dummy   = ListNode(0)   # fake starting node -- skip this at the end
    current = dummy         # 'pen' -- we attach nodes here

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1    # attach the smaller node
            list1         = list1.next
        else:
            current.next = list2
            list2         = list2.next
        current = current.next      # advance our pen

    # One list is exhausted -- attach the REST of the other (already sorted)
    current.next = list1 if list1 else list2

    return dummy.next   # skip dummy, return real head


# ─────────────────────────────────────────────────────
# APPROACH B -- Recursive (elegant but uses call stack space)
# ─────────────────────────────────────────────────────
# At each step:
#   - Pick the node with the smaller value as the "head" of the merged list.
#   - Its .next points to the result of merging everything that remains.
#
# STEP-BY-STEP with list1=[1,2,4], list2=[1,3,4]:
#
#   merge(1->2->4, 1->3->4)
#     l1.val(1) <= l2.val(1): l1 wins
#     l1.next = merge(2->4, 1->3->4)
#       l1.val(2) > l2.val(1): l2 wins
#       l2.next = merge(2->4, 3->4)
#         l1.val(2) <= l2.val(3): l1 wins
#         l1.next = merge(4, 3->4)
#           l1.val(4) > l2.val(3): l2 wins
#           l2.next = merge(4, 4)
#             l1.val(4) <= l2.val(4): l1 wins
#             l1.next = merge(None, 4)
#               l1 is None -> return l2(4)
#             l1.next = 4, return l1(4)
#           l2.next = 4->4, return l2(3) [3->4->4]
#         ... and so on unwinds ...
#   Result: 1->1->2->3->4->4  ✓

def merge_two_lists_recursive(list1, list2):
    # Base cases: if either list is empty, return the other
    if not list1:
        return list2
    if not list2:
        return list1

    # Pick the smaller head; its next is the merge of what's left
    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_recursive(list1, list2.next)
        return list2


# Use the iterative version as the main solution
def merge_two_lists(list1, list2):
    return merge_two_lists_iterative(list1, list2)


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
print(to_list(merge_two_lists(build_list([1,2,4]), build_list([1,3,4]))))  # -> [1,1,2,3,4,4]
print(to_list(merge_two_lists(build_list([]), build_list([]))))            # -> []
print(to_list(merge_two_lists(build_list([]), build_list([0]))))           # -> [0]
print(to_list(merge_two_lists(build_list([2]), build_list([1]))))          # -> [1,2]

# Test recursive version too
print("--- Recursive ---")
print(to_list(merge_two_lists_recursive(build_list([1,2,4]), build_list([1,3,4])))) # -> [1,1,2,3,4,4]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Same dummy-head iterative approach. null instead of None.
# No separate class needed -- LeetCode provides ListNode.
#
# function mergeTwoLists(list1, list2) {
#     const dummy = { val: 0, next: null };
#     let current = dummy;
#
#     while (list1 && list2) {
#         if (list1.val <= list2.val) {
#             current.next = list1;
#             list1 = list1.next;
#         } else {
#             current.next = list2;
#             list2 = list2.next;
#         }
#         current = current.next;
#     }
#
#     current.next = list1 ?? list2;   // attach remaining list
#     return dummy.next;
# }


# =============================================================================
# 3. JAVA
# =============================================================================
# Same iterative approach. ListNode is provided by LeetCode's environment.
# null is Java's equivalent of Python's None.
#
# class Solution {
#     public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
#         ListNode dummy   = new ListNode(0);
#         ListNode current = dummy;
#
#         while (list1 != null && list2 != null) {
#             if (list1.val <= list2.val) {
#                 current.next = list1;
#                 list1 = list1.next;
#             } else {
#                 current.next = list2;
#                 list2 = list2.next;
#             }
#             current = current.next;
#         }
#
#         current.next = (list1 != null) ? list1 : list2;
#         return dummy.next;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Same iterative approach. nullptr is C++'s null pointer.
# Pointer arithmetic: current->next accesses next through a pointer.
#
# struct ListNode {
#     int val;
#     ListNode* next;
#     ListNode(int v) : val(v), next(nullptr) {}
# };
#
# class Solution {
# public:
#     ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
#         ListNode dummy(0);
#         ListNode* current = &dummy;
#
#         while (list1 && list2) {
#             if (list1->val <= list2->val) {
#                 current->next = list1;
#                 list1 = list1->next;
#             } else {
#                 current->next = list2;
#                 list2 = list2->next;
#             }
#             current = current->next;
#         }
#
#         current->next = list1 ? list1 : list2;
#         return dummy.next;
#     }
# };


# =============================================================================
# 5. C#
# =============================================================================
# Same iterative approach. null in C# (same as Java).
# ListNode class is provided by LeetCode's C# environment.
#
# public class Solution {
#     public ListNode MergeTwoLists(ListNode list1, ListNode list2) {
#         ListNode dummy   = new ListNode(0);
#         ListNode current = dummy;
#
#         while (list1 != null && list2 != null) {
#             if (list1.val <= list2.val) {
#                 current.next = list1;
#                 list1 = list1.next;
#             } else {
#                 current.next = list2;
#                 list2 = list2.next;
#             }
#             current = current.next;
#         }
#
#         current.next = list1 ?? list2;   // null-coalescing: use list1 if not null
#         return dummy.next;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Same iterative approach. nil is Go's null pointer.
# dummy := &ListNode{} creates a new node on the heap.
#
# type ListNode struct {
#     Val  int
#     Next *ListNode
# }
#
# func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {
#     dummy   := &ListNode{}
#     current := dummy
#
#     for list1 != nil && list2 != nil {
#         if list1.Val <= list2.Val {
#             current.Next = list1
#             list1 = list1.Next
#         } else {
#             current.Next = list2
#             list2 = list2.Next
#         }
#         current = current.Next
#     }
#
#     if list1 != nil {
#         current.Next = list1
#     } else {
#         current.Next = list2
#     }
#
#     return dummy.Next
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Rust's recursive approach is cleaner here than the iterative one.
# Option<Box<ListNode>> is either Some(node) or None.
# take() moves the value out of an Option, leaving None in its place.
#
# #[derive(Debug)]
# pub struct ListNode {
#     pub val:  i32,
#     pub next: Option<Box<ListNode>>,
# }
#
# impl ListNode {
#     fn new(val: i32) -> Self { ListNode { val, next: None } }
# }
#
# pub fn merge_two_lists(
#     list1: Option<Box<ListNode>>,
#     list2: Option<Box<ListNode>>,
# ) -> Option<Box<ListNode>> {
#     match (list1, list2) {
#         (None, l2)   => l2,
#         (l1,   None) => l1,
#         (Some(mut l1), Some(mut l2)) => {
#             if l1.val <= l2.val {
#                 l1.next = merge_two_lists(l1.next.take(), Some(l2));
#                 Some(l1)
#             } else {
#                 l2.next = merge_two_lists(Some(l1), l2.next.take());
#                 Some(l2)
#             }
#         }
#     }
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Recursive approach -- clean and idiomatic Swift.
# ListNode? is an optional (can be nil). guard let unwraps safely.
#
# public class ListNode {
#     public var val:  Int
#     public var next: ListNode?
#     public init(_ val: Int) { self.val = val; self.next = nil }
# }
#
# func mergeTwoLists(_ list1: ListNode?, _ list2: ListNode?) -> ListNode? {
#     guard let l1 = list1 else { return list2 }
#     guard let l2 = list2 else { return list1 }
#
#     if l1.val <= l2.val {
#         l1.next = mergeTwoLists(l1.next, l2)
#         return l1
#     } else {
#         l2.next = mergeTwoLists(l1, l2.next)
#         return l2
#     }
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Iterative approach with dummy head. null safety handled with ?: operator.
# ListNode class is provided by LeetCode; we show the standard definition.
#
# class ListNode(var `val`: Int = 0, var next: ListNode? = null)
#
# fun mergeTwoLists(list1: ListNode?, list2: ListNode?): ListNode? {
#     val dummy = ListNode(0)
#     var current: ListNode = dummy
#     var l1 = list1
#     var l2 = list2
#
#     while (l1 != null && l2 != null) {
#         if (l1.`val` <= l2.`val`) {
#             current.next = l1
#             l1 = l1.next
#         } else {
#             current.next = l2
#             l2 = l2.next
#         }
#         current = current.next!!
#     }
#
#     current.next = l1 ?: l2
#     return dummy.next
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Recursive approach -- Ruby's clean syntax makes it shine here.
# nil is Ruby's null. The ternary handles which list to return at base cases.
#
# class ListNode
#   attr_accessor :val, :next_node
#   def initialize(val = 0, next_node = nil)
#     @val = val; @next_node = next_node
#   end
# end
#
# def merge_two_lists(list1, list2)
#   return list2 unless list1
#   return list1 unless list2
#
#   if list1.val <= list2.val
#     list1.next_node = merge_two_lists(list1.next_node, list2)
#     list1
#   else
#     list2.next_node = merge_two_lists(list1, list2.next_node)
#     list2
#   end
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# TWO APPROACHES, both shown:
#
#   ITERATIVE (Python, JS, Java, C++, C#, Go, Kotlin):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  dummy -> (result builds here)                                  │
#   │  current = dummy                                                 │
#   │                                                                  │
#   │  While both lists have nodes:                                   │
#   │    Pick the smaller head node                                    │
#   │    Attach it to current.next                                    │
#   │    Advance that list's pointer AND current                      │
#   │                                                                  │
#   │  Attach whatever remains of the non-empty list                  │
#   │  Return dummy.next                                               │
#   └──────────────────────────────────────────────────────────────────┘
#
#   RECURSIVE (Python, Rust, Swift, Ruby):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Base: if either list is None/nil -> return the other           │
#   │                                                                  │
#   │  Pick the node with the smaller val as the "winner"             │
#   │  winner.next = merge(winner.next, the_other_list)               │
#   │  Return winner                                                   │
#   └──────────────────────────────────────────────────────────────────┘
#
# ITERATIVE vs RECURSIVE:
#   Iterative: O(1) extra space (no call stack growth). Preferred in production.
#   Recursive: Elegant and short. Uses O(m+n) stack space (one frame per node).
#
# Both are O(m+n) time where m and n are the lengths of the two lists.
# =============================================================================
