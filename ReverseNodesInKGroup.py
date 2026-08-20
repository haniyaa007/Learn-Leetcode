# =============================================================================
# REVERSE NODES IN K-GROUP
# =============================================================================
# PROBLEM: Given the head of a linked list, reverse the nodes k at a time
# and return the modified list. If the number of nodes isn't a multiple
# of k, the leftover nodes at the end stay in their original order.
# You may not alter node VALUES -- only the nodes themselves may move.
#
# EXAMPLES:
#   [1,2,3,4,5], k=2  ->  [2,1,4,3,5]
#   [1,2,3,4,5], k=3  ->  [3,2,1,4,5]
#
# WHY IS THIS HARDER THAN SWAP NODES IN PAIRS?
#   - Swap Pairs is just this problem with k fixed at 2.
#   - Here k is arbitrary, so we can't hardcode "grab two nodes."
#   - We must first CHECK that a full group of k nodes exists before
#     reversing anything -- a leftover partial group must stay untouched.
#
# THE NAIVE APPROACH (still O(n), but heavier):
#   Dump all values into an array, reverse each k-sized chunk, write the
#   values back into the existing nodes. Works, but rewrites node VALUES
#   which some interviewers (and this problem's phrasing) explicitly rule out.
#   It also isn't "true" O(1) extra memory since the array is O(n).
#
# THE SMART APPROACH:
#   Dummy head + for each group: check it has k nodes, reverse it in
#   place with the standard "reverse a linked list" pointer dance, then
#   reconnect it to the previous group and the next group.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- Dummy head + reverse each full group of k, in place:
#
# KEY IDEA: This is "Swap Nodes in Pairs" generalized to group size k,
# combined with the classic "reverse a linked list" trick applied to
# just one group at a time instead of the whole list.
#
# STEP 1 -- Create a dummy node pointing at head.
#   Same reason as Swap Pairs: makes the first group's reversal behave
#   exactly like every other group's, no special-casing the real head.
#
# STEP 2 -- Keep a "groupPrev" pointer -- the node right before the
#   current group. groupPrev starts at dummy.
#
# STEP 3 -- For each group, FIRST check it actually has k nodes.
#   Walk k steps ahead from groupPrev. If we fall off the end (hit None)
#   before reaching k nodes, STOP -- this partial group is left alone.
#
# STEP 4 -- Reverse exactly k nodes using the standard iterative reversal:
#   prev = None, curr = groupPrev.next
#   Repeat k times:
#     nxt = curr.next
#     curr.next = prev
#     prev = curr
#     curr = nxt
#   After this loop: `prev` is the new head of the reversed group,
#   and `curr` is the first node AFTER the group (untouched so far).
#
# STEP 5 -- Reconnect the reversed group to its neighbors:
#   groupPrev.next was the OLD first node of the group -- after
#   reversal that node is now the group's TAIL, so:
#     groupPrev.next.next = curr      # old head (now tail) -> next group
#     groupPrev.next      = prev      # groupPrev -> new head of reversed group
#
# STEP 6 -- Advance groupPrev to the tail of the group just reversed
#   (which is the OLD head, saved before we overwrote groupPrev.next),
#   then repeat from Step 3 for the next group.
#
# STEP-BY-STEP with [1,2,3,4,5], k=2:
#
#   dummy -> 1 -> 2 -> 3 -> 4 -> 5      groupPrev = dummy
#
#   Group check: from groupPrev, walk 2 steps -> lands on node 2. OK, full group.
#   groupNext = 3 (node right after the group)
#
#   Reverse 1 -> 2:
#     prev=None, curr=1
#     step1: nxt=2, 1.next=None, prev=1, curr=2
#     step2: nxt=3, 2.next=1,    prev=2, curr=3
#   Now prev=2 (new group head), curr=3 (correctly stopped at groupNext)
#
#   Reconnect: groupPrev.next (=old head, node 1).next = curr (3)
#              groupPrev.next = prev (2)
#   List so far: dummy -> 2 -> 1 -> 3 -> 4 -> 5
#   groupPrev advances to node 1 (the old head, now tail of this group)
#
#   Group check: from groupPrev(=1), walk 2 steps -> lands on node 4. OK.
#   groupNext = 5
#
#   Reverse 3 -> 4:
#     prev=None, curr=3
#     step1: nxt=4, 3.next=None, prev=3, curr=4
#     step2: nxt=5, 4.next=3,    prev=4, curr=5
#
#   Reconnect: groupPrev.next (=old head, node 3).next = curr (5)
#              groupPrev.next = prev (4)
#   List so far: dummy -> 2 -> 1 -> 4 -> 3 -> 5
#   groupPrev advances to node 3
#
#   Group check: from groupPrev(=3), walk 2 steps -> falls off after node 5
#   (only 1 node left). STOP -- leftover node 5 stays as-is.
#
#   Result: 2 -> 1 -> 4 -> 3 -> 5  ✓

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # STEP 3 -- check there are k nodes left starting after group_prev
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next   # fewer than k nodes left -- done

        group_next = kth.next        # first node AFTER this group
        old_head    = group_prev.next  # will become the tail after reversal

        # STEP 4 -- reverse exactly k nodes
        prev, curr = group_next, group_prev.next
        while curr is not group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # STEP 5 -- reconnect the reversed group to its neighbors
        group_prev.next = kth          # groupPrev -> new head (old kth)
        group_prev = old_head          # STEP 6 -- advance to tail of this group

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
print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)))   # -> [2,1,4,3,5]
print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)))   # -> [3,2,1,4,5]
print(to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 1)))   # -> [1,2,3,4,5]
print(to_list(reverse_k_group(build_list([1]), 1)))                # -> [1]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Same dummy-head + "check-then-reverse-then-reconnect" structure.
#
# function ListNode(val, next) {
#     this.val = val === undefined ? 0 : val;
#     this.next = next === undefined ? null : next;
# }
#
# function reverseKGroup(head, k) {
#     const dummy = new ListNode(0, head);
#     let groupPrev = dummy;
#
#     while (true) {
#         let kth = groupPrev;
#         for (let i = 0; i < k; i++) {
#             kth = kth.next;
#             if (!kth) return dummy.next;
#         }
#
#         const groupNext = kth.next;
#         const oldHead   = groupPrev.next;
#
#         let prev = groupNext, curr = groupPrev.next;
#         while (curr !== groupNext) {
#             const nxt = curr.next;
#             curr.next = prev;
#             prev = curr;
#             curr = nxt;
#         }
#
#         groupPrev.next = kth;
#         groupPrev = oldHead;
#     }
# }


# =============================================================================
# 3. JAVA
# =============================================================================
# Standard LeetCode ListNode definition. Identical group-check + reverse
# + reconnect flow.
#
# class ListNode {
#     int val;
#     ListNode next;
#     ListNode(int val) { this.val = val; }
#     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
# }
#
# class Solution {
#     public ListNode reverseKGroup(ListNode head, int k) {
#         ListNode dummy = new ListNode(0, head);
#         ListNode groupPrev = dummy;
#
#         while (true) {
#             ListNode kth = groupPrev;
#             for (int i = 0; i < k; i++) {
#                 kth = kth.next;
#                 if (kth == null) return dummy.next;
#             }
#
#             ListNode groupNext = kth.next;
#             ListNode oldHead   = groupPrev.next;
#
#             ListNode prev = groupNext, curr = groupPrev.next;
#             while (curr != groupNext) {
#                 ListNode nxt = curr.next;
#                 curr.next = prev;
#                 prev = curr;
#                 curr = nxt;
#             }
#
#             groupPrev.next = kth;
#             groupPrev = oldHead;
#         }
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# Raw pointers. Same three phases: check group size, reverse, reconnect.
#
# struct ListNode {
#     int val;
#     ListNode *next;
#     ListNode(int x) : val(x), next(nullptr) {}
#     ListNode(int x, ListNode *n) : val(x), next(n) {}
# };
#
# ListNode* reverseKGroup(ListNode* head, int k) {
#     ListNode dummy(0, head);
#     ListNode* groupPrev = &dummy;
#
#     while (true) {
#         ListNode* kth = groupPrev;
#         for (int i = 0; i < k && kth; i++) kth = kth->next;
#         if (!kth) return dummy.next;
#
#         ListNode* groupNext = kth->next;
#         ListNode* oldHead   = groupPrev->next;
#
#         ListNode* prev = groupNext;
#         ListNode* curr = groupPrev->next;
#         while (curr != groupNext) {
#             ListNode* nxt = curr->next;
#             curr->next = prev;
#             prev = curr;
#             curr = nxt;
#         }
#
#         groupPrev->next = kth;
#         groupPrev = oldHead;
#     }
# }


# =============================================================================
# 5. C#
# =============================================================================
# Same three-phase structure, C# class syntax.
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
#     public ListNode ReverseKGroup(ListNode head, int k) {
#         ListNode dummy = new ListNode(0, head);
#         ListNode groupPrev = dummy;
#
#         while (true) {
#             ListNode kth = groupPrev;
#             for (int i = 0; i < k; i++) {
#                 kth = kth?.next;
#                 if (kth == null) return dummy.next;
#             }
#
#             ListNode groupNext = kth.next;
#             ListNode oldHead   = groupPrev.next;
#
#             ListNode prev = groupNext, curr = groupPrev.next;
#             while (curr != groupNext) {
#                 ListNode nxt = curr.next;
#                 curr.next = prev;
#                 prev = curr;
#                 curr = nxt;
#             }
#
#             groupPrev.next = kth;
#             groupPrev = oldHead;
#         }
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Structs and pointers. Same three phases as every other language.
#
# type ListNode struct {
#     Val  int
#     Next *ListNode
# }
#
# func reverseKGroup(head *ListNode, k int) *ListNode {
#     dummy := &ListNode{Next: head}
#     groupPrev := dummy
#
#     for {
#         kth := groupPrev
#         ok := true
#         for i := 0; i < k; i++ {
#             if kth.Next == nil {
#                 ok = false
#                 break
#             }
#             kth = kth.Next
#         }
#         if !ok {
#             return dummy.Next
#         }
#
#         groupNext := kth.Next
#         oldHead := groupPrev.Next
#
#         prev, curr := groupNext, groupPrev.Next
#         for curr != groupNext {
#             nxt := curr.Next
#             curr.Next = prev
#             prev = curr
#             curr = nxt
#         }
#
#         groupPrev.Next = kth
#         groupPrev = oldHead
#     }
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Ownership makes the "walk ahead k steps, then reverse in place" trick
# awkward, so the idiomatic Rust solution recurses: reverse the first k
# nodes, recursively solve the rest, then splice the two together.
#
# #[derive(PartialEq, Eq, Clone, Debug)]
# pub struct ListNode {
#     pub val: i32,
#     pub next: Option<Box<ListNode>>,
# }
#
# pub fn reverse_k_group(head: Option<Box<ListNode>>, k: i32) -> Option<Box<ListNode>> {
#     // First, confirm k nodes exist from here; if not, return head unchanged.
#     let mut count = 0;
#     let mut node = &head;
#     while count < k {
#         match node {
#             Some(n) => { node = &n.next; count += 1; }
#             None => return head,   // fewer than k nodes left, leave as-is
#         }
#     }
#
#     // Reverse the first k nodes, threading the (already-solved) remainder in.
#     let mut prev = reverse_k_group_tail(&head, k); // remainder, recursively processed
#     let mut curr = head;
#     for _ in 0..k {
#         let mut n = curr.take().unwrap();
#         curr = n.next.take();
#         n.next = prev;
#         prev = Some(n);
#     }
#     prev
# }
#
# // Helper: returns the recursively-reversed remainder starting at the (k+1)-th node.
# fn reverse_k_group_tail(head: &Option<Box<ListNode>>, k: i32) -> Option<Box<ListNode>> {
#     let mut rest = head;
#     for _ in 0..k { rest = &rest.as_ref().unwrap().next; }
#     reverse_k_group(rest.clone(), k)
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Classes are reference types, so the same pointer-rewiring approach
# from Java/C# applies directly.
#
# public class ListNode {
#     public var val: Int
#     public var next: ListNode?
#     public init(_ val: Int) { self.val = val; self.next = nil }
# }
#
# func reverseKGroup(_ head: ListNode?, _ k: Int) -> ListNode? {
#     let dummy = ListNode(0)
#     dummy.next = head
#     var groupPrev: ListNode? = dummy
#
#     while true {
#         var kth = groupPrev
#         for _ in 0..<k {
#             kth = kth?.next
#             if kth == nil { return dummy.next }
#         }
#
#         let groupNext = kth?.next
#         let oldHead = groupPrev?.next
#
#         var prev = groupNext
#         var curr = groupPrev?.next
#         while curr !== groupNext {
#             let nxt = curr?.next
#             curr?.next = prev
#             prev = curr
#             curr = nxt
#         }
#
#         groupPrev?.next = kth
#         groupPrev = oldHead
#     }
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Same three-phase structure; nullable types stand in for the null checks.
#
# class ListNode(var `val`: Int) {
#     var next: ListNode? = null
# }
#
# fun reverseKGroup(head: ListNode?, k: Int): ListNode? {
#     val dummy = ListNode(0).apply { next = head }
#     var groupPrev: ListNode? = dummy
#
#     while (true) {
#         var kth = groupPrev
#         for (i in 0 until k) {
#             kth = kth?.next ?: return dummy.next
#         }
#
#         val groupNext = kth?.next
#         val oldHead = groupPrev?.next
#
#         var prev = groupNext
#         var curr = groupPrev?.next
#         while (curr !== groupNext) {
#             val nxt = curr?.next
#             curr?.next = prev
#             prev = curr
#             curr = nxt
#         }
#
#         groupPrev?.next = kth
#         groupPrev = oldHead
#     }
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# attr_accessor for val/next. Same check -> reverse -> reconnect flow,
# using Ruby's `loop do ... end` for the outer infinite loop.
#
# class ListNode
#   attr_accessor :val, :next
#   def initialize(val = 0, nxt = nil)
#     @val = val
#     @next = nxt
#   end
# end
#
# def reverse_k_group(head, k)
#   dummy = ListNode.new(0, head)
#   group_prev = dummy
#
#   loop do
#     kth = group_prev
#     k.times do
#       kth = kth&.next
#       return dummy.next unless kth
#     end
#
#     group_next = kth.next
#     old_head    = group_prev.next
#
#     prev, curr = group_next, group_prev.next
#     while curr != group_next
#       nxt = curr.next
#       curr.next = prev
#       prev = curr
#       curr = nxt
#     end
#
#     group_prev.next = kth
#     group_prev = old_head
#   end
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use DUMMY HEAD + CHECK-THEN-REVERSE-THEN-RECONNECT,
# repeated group by group (Rust shows the idiomatic recursive alternative):
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  1. Create a dummy node pointing at head.                        │
#   │       Lets the first group reverse the same way as every other.  │
#   │                                                                    │
#   │  2. groupPrev starts at dummy. Repeat for each group:            │
#   │                                                                    │
#   │  3. CHECK: walk k steps from groupPrev. If you fall off the end  │
#   │       before k steps, STOP -- leave this partial group untouched.│
#   │                                                                    │
#   │  4. REVERSE: standard iterative reversal, but only k nodes,      │
#   │       stopping curr at groupNext (the node right after the group).│
#   │       prev=groupNext, curr=groupPrev.next                        │
#   │       while curr != groupNext: nxt=curr.next; curr.next=prev;    │
#   │                                 prev=curr; curr=nxt              │
#   │                                                                    │
#   │  5. RECONNECT: groupPrev.next = kth (new group head)             │
#   │       groupPrev advances to oldHead (the group's new tail)       │
#   │                                                                    │
#   │  6. Return dummy.next once a partial group (or the end) is hit.  │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY CHECK BEFORE REVERSING?
#   Reversing first and checking after would require UNDOING the
#   reversal if fewer than k nodes were found -- messy and wasteful.
#   Walking ahead k steps first is a cheap, clean way to know whether
#   this group is eligible before touching a single pointer.
#
# !! COMMON MISTAKE !!
#   Forgetting to stop the reversal loop at `groupNext` (rather than at
#   None) will reverse the ENTIRE rest of the list instead of just this
#   group. `curr != groupNext` is what boundaries the reversal correctly.
#
# RELATIONSHIP TO "SWAP NODES IN PAIRS":
#   Swap Pairs is this exact algorithm with k hardcoded to 2. Everything
#   here -- dummy head, groupPrev, checking before acting -- generalizes
#   that problem's pattern to an arbitrary group size.
#
# Time complexity:  O(n) -- every node is visited and relinked a constant
#                    number of times across all groups
# Space complexity: O(1) extra space (iterative versions) -- satisfies
#                    the follow-up. Recursive versions (e.g. Rust) use
#                    O(n/k) stack frames instead.
# =============================================================================
