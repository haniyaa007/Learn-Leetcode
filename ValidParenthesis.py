# =============================================================================
# VALID PARENTHESES
# =============================================================================
# PROBLEM: Given a string of brackets, return True if every opening bracket
# is closed by the correct type of bracket in the correct order.
#
# VALID examples:   "()"   "()[]{}"   "([])"   "{[()]}"
# INVALID examples: "(]"   "([)]"     "("      "}"
#
# THE THREE RULES:
#   1. Every opening bracket must eventually be closed.
#   2. Every closing bracket must match the MOST RECENT unclosed opening bracket.
#   3. There must be no leftover unclosed brackets at the end.
#
# THE KEY INSIGHT -- "most recent unclosed" screams STACK:
#   A stack is a Last-In-First-Out (LIFO) structure.
#   The last bracket you opened must be the first one you close.
#   That's exactly what a stack models naturally.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS -- Stack:
#
# Walk through the string character by character.
# - If it's an OPENING bracket  ( [ {  -> PUSH it onto the stack.
# - If it's a CLOSING bracket ) ] }:
#     - If the stack is EMPTY  -> no matching opener -> INVALID
#     - POP the top of the stack.
#     - If the popped opener doesn't MATCH this closer -> INVALID
# At the end: if the stack is EMPTY -> VALID (all openers were matched).
#             if the stack is not empty -> INVALID (unclosed openers remain).
#
# STEP-BY-STEP with "([])" :
#
#   char='('   opening -> push    stack=['(']
#   char='['   opening -> push    stack=['(','[']
#   char=']'   closing -> pop '['  does '[' match ']'? YES  stack=['(']
#   char=')'   closing -> pop '('  does '(' match ')'? YES  stack=[]
#   End: stack is empty -> VALID ✓
#
# STEP-BY-STEP with "([)]" :
#
#   char='('   opening -> push    stack=['(']
#   char='['   opening -> push    stack=['(','[']
#   char=')'   closing -> pop '[' does '[' match ')'? NO -> return False
#
# THE MATCHING TRICK:
#   Store the pairs in a dictionary: closer -> opener.
#   When we see a closer, look up its expected opener and check the stack.
#   This avoids a chain of if/elif comparisons.

def is_valid(s):
    stack = []

    # Map each closing bracket to its matching opening bracket
    matching = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in matching:
            # It's a closing bracket
            # Pop the top of the stack (or use '#' as a dummy if empty)
            top = stack.pop() if stack else '#'
            if matching[char] != top:
                return False   # mismatch or empty stack
        else:
            # It's an opening bracket -> push onto stack
            stack.append(char)

    # Valid only if all openers were matched (stack is empty)
    return len(stack) == 0


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(is_valid("()"))        # -> True
print(is_valid("()[]{}"))    # -> True
print(is_valid("(]"))        # -> False
print(is_valid("([])"))      # -> True
print(is_valid("([)]"))      # -> False
print(is_valid("{[]}"))      # -> True
print(is_valid("("))         # -> False  (unclosed opener)
print(is_valid(")"))         # -> False  (closer with empty stack)


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# An object maps closers to openers (same as Python's dict).
# An array acts as the stack (push/pop are built-in array methods).
# hasOwnProperty or 'in' checks if a key exists in the object.
#
# function isValid(s) {
#     const stack = [];
#     const matching = { ')': '(', ']': '[', '}': '{' };
#
#     for (const char of s) {
#         if (char in matching) {
#             const top = stack.length > 0 ? stack.pop() : '#';
#             if (matching[char] !== top) return false;
#         } else {
#             stack.push(char);
#         }
#     }
#
#     return stack.length === 0;
# }
#
# console.log(isValid("()"));      // -> true
# console.log(isValid("()[]{}"));  // -> true
# console.log(isValid("(]"));      // -> false
# console.log(isValid("([])"));    // -> true
# console.log(isValid("([)]"));    // -> false


# =============================================================================
# 3. JAVA
# =============================================================================
# Deque<Character> is Java's recommended stack (ArrayDeque is the impl).
# HashMap<Character, Character> maps closing to opening brackets.
# Character.valueOf() isn't needed -- char comparisons work directly.
#
# import java.util.*;
#
# class Solution {
#     public boolean isValid(String s) {
#         Deque<Character> stack = new ArrayDeque<>();
#         Map<Character, Character> matching = new HashMap<>();
#         matching.put(')', '(');
#         matching.put(']', '[');
#         matching.put('}', '{');
#
#         for (char c : s.toCharArray()) {
#             if (matching.containsKey(c)) {
#                 char top = stack.isEmpty() ? '#' : stack.pop();
#                 if (matching.get(c) != top) return false;
#             } else {
#                 stack.push(c);
#             }
#         }
#
#         return stack.isEmpty();
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# std::stack<char> is C++'s stack. top() peeks, pop() removes (void!).
# unordered_map<char,char> maps closers to openers.
# Note: in C++ stack, you must top() then pop() separately.
#
# #include <string>
# #include <stack>
# #include <unordered_map>
# using namespace std;
#
# bool isValid(string s) {
#     stack<char> stk;
#     unordered_map<char,char> matching = {{')', '('}, {']', '['}, {'}', '{'}};
#
#     for (char c : s) {
#         if (matching.count(c)) {
#             char top = stk.empty() ? '#' : stk.top();
#             stk.empty() ? void() : stk.pop();
#             if (matching[c] != top) return false;
#         } else {
#             stk.push(c);
#         }
#     }
#
#     return stk.empty();
# }


# =============================================================================
# 5. C#
# =============================================================================
# Stack<char> is C#'s generic stack. Peek() reads the top; Pop() removes it.
# Dictionary<char, char> maps closers to openers.
# Count == 0 checks if the stack is empty.
#
# using System.Collections.Generic;
#
# public class Solution {
#     public bool IsValid(string s) {
#         var stack = new Stack<char>();
#         var matching = new Dictionary<char, char> {
#             {')', '('}, {']', '['}, {'}', '{'}
#         };
#
#         foreach (char c in s) {
#             if (matching.ContainsKey(c)) {
#                 char top = stack.Count > 0 ? stack.Pop() : '#';
#                 if (matching[c] != top) return false;
#             } else {
#                 stack.Push(c);
#             }
#         }
#
#         return stack.Count == 0;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# A slice ([]rune) acts as the stack: append() pushes, slicing pops.
# map[rune]rune maps closing to opening rune (Go's character type).
# len(stack) == 0 checks if empty.
#
# func isValid(s string) bool {
#     stack := []rune{}
#     matching := map[rune]rune{')': '(', ']': '[', '}': '{'}
#
#     for _, c := range s {
#         if opener, ok := matching[c]; ok {
#             // It's a closer
#             if len(stack) == 0 || stack[len(stack)-1] != opener {
#                 return false
#             }
#             stack = stack[:len(stack)-1]   // pop
#         } else {
#             stack = append(stack, c)        // push
#         }
#     }
#
#     return len(stack) == 0
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Vec<char> acts as the stack (push/pop are built-in).
# A match expression maps closing chars to their expected openers.
# matches!() is a macro that checks if a value matches a pattern.
#
# fn is_valid(s: String) -> bool {
#     let mut stack: Vec<char> = Vec::new();
#
#     for c in s.chars() {
#         match c {
#             '(' | '[' | '{' => stack.push(c),
#             ')' => if stack.pop() != Some('(') { return false; },
#             ']' => if stack.pop() != Some('[') { return false; },
#             '}' => if stack.pop() != Some('{') { return false; },
#             _   => {}
#         }
#     }
#
#     stack.is_empty()
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# [Character] array as the stack. removeLast() pops; append() pushes.
# A switch statement maps closing chars to their expected openers.
#
# func isValid(_ s: String) -> Bool {
#     var stack = [Character]()
#     let matching: [Character: Character] = [")": "(", "]": "[", "}": "{"]
#
#     for c in s {
#         if let opener = matching[c] {
#             let top = stack.isEmpty ? Character("#") : stack.removeLast()
#             if top != opener { return false }
#         } else {
#             stack.append(c)
#         }
#     }
#
#     return stack.isEmpty
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# ArrayDeque<Char> is Kotlin's stack. addLast() pushes; removeLastOrNull() pops.
# mapOf maps closing to opening chars. containsKey() checks membership.
#
# fun isValid(s: String): Boolean {
#     val stack = ArrayDeque<Char>()
#     val matching = mapOf(')' to '(', ']' to '[', '}' to '{')
#
#     for (c in s) {
#         if (c in matching) {
#             val top = stack.removeLastOrNull() ?: '#'
#             if (matching[c] != top) return false
#         } else {
#             stack.addLast(c)
#         }
#     }
#
#     return stack.isEmpty()
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# An Array acts as the stack (push and pop are built-in).
# A hash maps closing to opening brackets.
# stack.empty? checks if the stack has no elements.
#
# def is_valid(s)
#   stack    = []
#   matching = { ')' => '(', ']' => '[', '}' => '{' }
#
#   s.each_char do |char|
#     if matching.key?(char)
#       top = stack.empty? ? '#' : stack.pop
#       return false if matching[char] != top
#     else
#       stack.push(char)
#     end
#   end
#
#   stack.empty?
# end
#
# puts is_valid("()")       # -> true
# puts is_valid("()[]{}")   # -> true
# puts is_valid("(]")       # -> false
# puts is_valid("([])")     # -> true
# puts is_valid("([)]")     # -> false


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use a STACK:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  For each character in s:                                       │
#   │                                                                  │
#   │    Opening bracket ( [ {  ->  PUSH onto stack                  │
#   │                                                                  │
#   │    Closing bracket ) ] }  ->  POP from stack                   │
#   │      If stack was empty   ->  no opener to match -> False       │
#   │      If popped != expected opener -> mismatch -> False          │
#   │                                                                  │
#   │  At the end:                                                    │
#   │    Stack empty   -> all openers matched -> True                 │
#   │    Stack not empty -> unclosed openers remain -> False          │
#   └──────────────────────────────────────────────────────────────────┘
#
# WHY A STACK?
#   Brackets must be closed in REVERSE order of opening.
#   The most recently opened bracket must be closed first.
#   That's exactly what LIFO (Last In, First Out) models.
#
# THE DUMMY '#' TRICK:
#   When a closing bracket arrives and the stack is empty, we need to
#   return False but we still want to "pop" something to check against.
#   Using '#' as a dummy guarantees '#' != any bracket, so the check fails
#   naturally -- no need for a separate if-empty guard.
#
# Time complexity:  O(n)  -- each character is pushed and popped at most once
# Space complexity: O(n)  -- the stack can hold at most n/2 opening brackets
# =============================================================================
