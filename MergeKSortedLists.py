# =============================================================================
# MERGE K SORTED LISTS
# =============================================================================
# PROBLEM: Merge k sorted linked lists into one sorted linked list.
#
# THIS IS THE BIG BROTHER OF PROBLEM 21 (Merge Two Sorted Lists).
#   Problem 21: merge 2 lists.
#   Problem 23: merge k lists (k can be up to 10,000).
#
# WHY NOT JUST REPEAT PROBLEM 21 k TIMES?
#   We COULD merge lists one pair at a time: merge(merge(l1,l2), l3)...
#   But that's O(kN) where N is total nodes -- repeatedly processing early
#   nodes as the merged list grows. Too slow for large k.
#
#   The EFFICIENT approach: DIVIDE AND CONQUER.
#   Pair up lists and merge in rounds, like a tournament bracket.
#   Each round halves the number of lists. Total: O(N log k).
#
# EXAMPLES:
#   [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]
#   []                      -> []
#   [[]]                    -> []
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# WE SHOW TWO APPROACHES:
#
# ─────────────────────────────────────────────────────
# APPROACH A -- Min-Heap (Priority Queue)
# ─────────────────────────────────────────────────────
# IDEA: At each step we want the SMALLEST current head across all k lists.
# A min-heap answers "what's the smallest?" in O(log k) time.
#
# HOW IT WORKS:
#   1. Push all k list heads into a min-heap (sorted by node value).
#   2. Repeatedly pop the smallest node, attach it to the result.
#   3. If that node has a .next, push the next node onto the heap.
#   4. Stop when the heap is empty.
#
# WHY IS THIS FAST?
#   Each of the N total nodes is pushed and popped from the heap once.
#   Each heap operation costs O(log k).
#   Total: O(N log k).
#
# STEP-BY-STEP with [[1,4,5],[1,3,4],[2,6]]:
#
#   Heap initially: [(1, list0_node1), (1, list1_node1), (2, list2_node2)]
#
#   Pop (1, list0): attach 1. Push list0's next (4). result=1
#   Heap: [(1,l1_node1),(2,l2_node2),(4,l0_node4)]
#
#   Pop (1, list1): attach 1. Push list1's next (3). result=1->1
#   Heap: [(2,l2_node2),(3,l1_node3),(4,l0_node4)]
#
#   Pop (2, list2): attach 2. Push list2's next (6). result=1->1->2
#   Heap: [(3,l1_node3),(4,l0_node4),(6,l2_node6)]
#
#   Pop (3, list1): attach 3. Push list1's next (4). result=1->1->2->3
#   Heap: [(4,l0_node4),(4,l1_node4),(6,l2_node6)]
#
#   ... and so on until heap is empty ...
#   Final: 1->1->2->3->4->4->5->6  ✓
#
# PYTHON HEAP NOTE:
#   heapq is a MIN-heap: heappush adds, heappop removes the SMALLEST.
#   We push tuples (value, id, node) -- the 'id' is a tiebreaker
#   because if two nodes have the same value, Python would try to compare
#   the ListNode objects themselves (which doesn't work). The id ensures
#   uniqueness and breaks ties without comparing nodes.

import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val  = val
        self.next = next


def merge_k_lists(lists):
    dummy   = ListNode(0)
    current = dummy
    heap    = []

    # Push all non-None heads into the heap
    # (val, unique_id, node) -- id breaks ties when vals are equal
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    while heap:
        val, i, node = heapq.heappop(heap)   # grab the smallest
        current.next = node                   # attach it to result
        current      = current.next

        if node.next:
            # Push this list's next node into the heap
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


# ─────────────────────────────────────────────────────
# APPROACH B -- Divide and Conquer
# ─────────────────────────────────────────────────────
# Think of it like a tournament bracket:
#
#   Round 1: merge(l0,l1)  merge(l2,l3)  merge(l4,l5)  ...
#   Round 2: merge(result0, result1)  merge(result2, result3) ...
#   ...
#   Final round: one list remains
#
# Each round processes all N nodes once: O(N).
# There are log2(k) rounds.
# Total: O(N log k) -- same as the heap approach.

def merge_two(l1, l2):
    """Merge two sorted lists (from problem 21)."""
    dummy   = ListNode(0)
    current = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1; l1 = l1.next
        else:
            current.next = l2; l2 = l2.next
        current = current.next
    current.next = l1 or l2
    return dummy.next

def merge_k_lists_divide(lists):
    if not lists:
        return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged
    return lists[0]


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
print("=== PYTHON TESTS (Min-Heap) ===")
lists = [build_list([1,4,5]), build_list([1,3,4]), build_list([2,6])]
print(to_list(merge_k_lists(lists)))    # -> [1,1,2,3,4,4,5,6]
print(to_list(merge_k_lists([])))       # -> []
print(to_list(merge_k_lists([None])))   # -> []

print("=== PYTHON TESTS (Divide & Conquer) ===")
lists = [build_list([1,4,5]), build_list([1,3,4]), build_list([2,6])]
print(to_list(merge_k_lists_divide(lists)))  # -> [1,1,2,3,4,4,5,6]


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# JavaScript has no built-in min-heap. For a LeetCode-friendly approach,
# we use the divide-and-conquer strategy (merge pairs each round).
# This avoids implementing a heap from scratch.
#
# function mergeTwoLists(l1, l2) {
#     const dummy = { val: 0, next: null };
#     let cur = dummy;
#     while (l1 && l2) {
#         if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
#         else                  { cur.next = l2; l2 = l2.next; }
#         cur = cur.next;
#     }
#     cur.next = l1 ?? l2;
#     return dummy.next;
# }
#
# function mergeKLists(lists) {
#     if (!lists.length) return null;
#     while (lists.length > 1) {
#         const merged = [];
#         for (let i = 0; i < lists.length; i += 2) {
#             merged.push(mergeTwoLists(lists[i], lists[i + 1] ?? null));
#         }
#         lists = merged;
#     }
#     return lists[0];
# }
#
# // (Build/test helpers omitted for brevity)


# =============================================================================
# 3. JAVA
# =============================================================================
# PriorityQueue is Java's min-heap. We pass a comparator to sort by node.val.
# offer() adds to the heap; poll() removes the smallest.
#
# import java.util.*;
#
# class Solution {
#     public ListNode mergeKLists(ListNode[] lists) {
#         PriorityQueue<ListNode> heap = new PriorityQueue<>(
#             (a, b) -> a.val - b.val   // min-heap by node value
#         );
#
#         for (ListNode node : lists) {
#             if (node != null) heap.offer(node);
#         }
#
#         ListNode dummy   = new ListNode(0);
#         ListNode current = dummy;
#
#         while (!heap.isEmpty()) {
#             ListNode node = heap.poll();
#             current.next  = node;
#             current       = current.next;
#             if (node.next != null) heap.offer(node.next);
#         }
#
#         return dummy.next;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# priority_queue is a MAX-heap by default in C++.
# We pass a custom comparator (greater val = lower priority) to make it a min-heap.
# top() peeks; pop() removes (separately, unlike Java's poll()).
#
# #include <vector>
# #include <queue>
# using namespace std;
#
# struct ListNode { int val; ListNode* next; ListNode(int v):val(v),next(nullptr){} };
#
# struct Compare {
#     bool operator()(ListNode* a, ListNode* b) {
#         return a->val > b->val;   // min-heap: smaller val has higher priority
#     }
# };
#
# ListNode* mergeKLists(vector<ListNode*>& lists) {
#     priority_queue<ListNode*, vector<ListNode*>, Compare> heap;
#
#     for (ListNode* node : lists) {
#         if (node) heap.push(node);
#     }
#
#     ListNode dummy(0);
#     ListNode* current = &dummy;
#
#     while (!heap.empty()) {
#         ListNode* node = heap.top(); heap.pop();
#         current->next  = node;
#         current        = current->next;
#         if (node->next) heap.push(node->next);
#     }
#
#     return dummy.next;
# }


# =============================================================================
# 5. C#
# =============================================================================
# C# doesn't have a built-in min-heap either. We use divide and conquer
# (same as JS), which is clean and avoids implementing a heap.
#
# public class Solution {
#     private ListNode MergeTwo(ListNode l1, ListNode l2) {
#         ListNode dummy = new ListNode(0), cur = dummy;
#         while (l1 != null && l2 != null) {
#             if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
#             else                  { cur.next = l2; l2 = l2.next; }
#             cur = cur.next;
#         }
#         cur.next = l1 ?? l2;
#         return dummy.next;
#     }
#
#     public ListNode MergeKLists(ListNode[] lists) {
#         if (lists.Length == 0) return null;
#         var active = new System.Collections.Generic.List<ListNode>(lists);
#         while (active.Count > 1) {
#             var next = new System.Collections.Generic.List<ListNode>();
#             for (int i = 0; i < active.Count; i += 2) {
#                 ListNode l2 = (i + 1 < active.Count) ? active[i + 1] : null;
#                 next.Add(MergeTwo(active[i], l2));
#             }
#             active = next;
#         }
#         return active[0];
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go has heap support via container/heap. We implement the heap.Interface.
# This is more verbose than Python but the algorithm is identical.
#
# import "container/heap"
#
# type ListNode struct { Val int; Next *ListNode }
#
# // MinHeap implements heap.Interface for *ListNode
# type MinHeap []*ListNode
# func (h MinHeap) Len() int            { return len(h) }
# func (h MinHeap) Less(i, j int) bool  { return h[i].Val < h[j].Val }
# func (h MinHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
# func (h *MinHeap) Push(x interface{}) { *h = append(*h, x.(*ListNode)) }
# func (h *MinHeap) Pop() interface{}   { old:=*h; n:=len(old); x:=old[n-1]; *h=old[:n-1]; return x }
#
# func mergeKLists(lists []*ListNode) *ListNode {
#     h := &MinHeap{}
#     heap.Init(h)
#     for _, node := range lists {
#         if node != nil { heap.Push(h, node) }
#     }
#     dummy   := &ListNode{}
#     current := dummy
#     for h.Len() > 0 {
#         node       := heap.Pop(h).(*ListNode)
#         current.Next = node
#         current      = current.Next
#         if node.Next != nil { heap.Push(h, node.Next) }
#     }
#     return dummy.Next
# }


# =============================================================================
# 7. RUST
# =============================================================================
# BinaryHeap in Rust is a MAX-heap. We wrap nodes in Reverse() to get min-heap.
# Or we use divide and conquer (cleaner). Shown here with divide & conquer.
#
# use std::collections::BinaryHeap;
# use std::cmp::Reverse;
#
# // (ListNode definition omitted for brevity -- same as problem 21)
#
# // Divide and conquer approach (avoids Ord impl for ListNode):
# fn merge_two(l1: Option<Box<ListNode>>, l2: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
#     match (l1, l2) {
#         (None, l) | (l, None) => l,
#         (Some(mut a), Some(mut b)) => {
#             if a.val <= b.val {
#                 a.next = merge_two(a.next.take(), Some(b));
#                 Some(a)
#             } else {
#                 b.next = merge_two(Some(a), b.next.take());
#                 Some(b)
#             }
#         }
#     }
# }
#
# fn merge_k_lists(mut lists: Vec<Option<Box<ListNode>>>) -> Option<Box<ListNode>> {
#     if lists.is_empty() { return None; }
#     while lists.len() > 1 {
#         let mut merged = Vec::new();
#         let mut i = 0;
#         while i < lists.len() {
#             let l1 = lists[i].take();
#             let l2 = if i + 1 < lists.len() { lists[i+1].take() } else { None };
#             merged.push(merge_two(l1, l2));
#             i += 2;
#         }
#         lists = merged;
#     }
#     lists.remove(0)
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Swift has no built-in priority queue. Divide and conquer is the clean choice.
# The merge_two helper from problem 21 is reused directly.
#
# func mergeTwo(_ l1: ListNode?, _ l2: ListNode?) -> ListNode? {
#     guard let l1 = l1 else { return l2 }
#     guard let l2 = l2 else { return l1 }
#     if l1.val <= l2.val { l1.next = mergeTwo(l1.next, l2); return l1 }
#     else                { l2.next = mergeTwo(l1, l2.next); return l2 }
# }
#
# func mergeKLists(_ lists: [ListNode?]) -> ListNode? {
#     if lists.isEmpty { return nil }
#     var active = lists
#     while active.count > 1 {
#         var next = [ListNode?]()
#         var i = 0
#         while i < active.count {
#             let l2 = (i + 1 < active.count) ? active[i + 1] : nil
#             next.append(mergeTwo(active[i], l2))
#             i += 2
#         }
#         active = next
#     }
#     return active[0]
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# PriorityQueue (same as Java, since Kotlin runs on JVM).
# compareBy { it.`val` } creates a min-heap comparator by node value.
#
# fun mergeKLists(lists: Array<ListNode?>): ListNode? {
#     val heap = PriorityQueue<ListNode>(compareBy { it.`val` })
#
#     for (node in lists) { if (node != null) heap.offer(node) }
#
#     val dummy = ListNode(0)
#     var current = dummy
#
#     while (heap.isNotEmpty()) {
#         val node   = heap.poll()!!
#         current.next = node
#         current      = current.next!!
#         if (node.next != null) heap.offer(node.next)
#     }
#
#     return dummy.next
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby's standard library doesn't have a heap, but Ruby arrays have min_by
# and sort methods. Divide and conquer is clean and efficient here.
#
# def merge_two(l1, l2)
#   dummy = ListNode.new(0); cur = dummy
#   while l1 && l2
#     if l1.val <= l2.val then cur.next_node = l1; l1 = l1.next_node
#     else                     cur.next_node = l2; l2 = l2.next_node
#     end
#     cur = cur.next_node
#   end
#   cur.next_node = l1 || l2
#   dummy.next_node
# end
#
# def merge_k_lists(lists)
#   return nil if lists.empty?
#   active = lists.compact   # remove nil entries
#   return nil if active.empty?
#   while active.size > 1
#     merged = []
#     active.each_slice(2) { |a, b| merged << merge_two(a, b) }
#     active = merged
#   end
#   active[0]
# end


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# TWO EFFICIENT APPROACHES -- both O(N log k):
#
#   MIN-HEAP (Python/Java/C++/Go/Kotlin):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Push all k heads into a min-heap.                              │
#   │  Repeatedly pop the smallest, attach to result, push its .next. │
#   │  Each of N nodes: 1 push + 1 pop = O(log k) each -> O(N log k).│
#   └──────────────────────────────────────────────────────────────────┘
#
#   DIVIDE AND CONQUER (JS/C#/Rust/Swift/Ruby -- and Python's Approach B):
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Round 1: merge pairs  [l0,l1] [l2,l3] [l4,l5] ...            │
#   │  Round 2: merge pairs of the results                            │
#   │  ...until one list remains.                                      │
#   │  log2(k) rounds, each processing all N nodes -> O(N log k).    │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY NOT NAIVE (merge one by one)?
#   Each time we merge, the running result grows. Early nodes are processed
#   multiple times. Total work: O(kN). Much slower for large k.
#
# LANGUAGE NOTES:
#   Python  -- heapq (min-heap built in)
#   Java    -- PriorityQueue (min-heap with comparator)
#   C++     -- priority_queue with custom comparator (MAX by default!)
#   JS/C#/Swift/Ruby -- no built-in heap -> divide and conquer
#   Go      -- container/heap (requires implementing heap.Interface)
#   Kotlin  -- PriorityQueue (from JVM, same as Java)
#   Rust    -- BinaryHeap (max-heap; use Reverse() or divide & conquer)
#
# Time:  O(N log k)   N = total nodes, k = number of lists
# Space: O(k)         heap holds at most k nodes at once
# =============================================================================

