# =============================================================================
# LETTER COMBINATIONS OF A PHONE NUMBER
# =============================================================================
# PROBLEM: Given a string of digits (2-9), return ALL possible letter
# combinations that those digits could represent on a phone keypad.
#
# THE PHONE KEYPAD:
#   2 -> abc    3 -> def    4 -> ghi    5 -> jkl
#   6 -> mno    7 -> pqrs   8 -> tuv    9 -> wxyz
#
# EXAMPLES:
#   "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
#     digit 2 can be a, b, or c
#     digit 3 can be d, e, or f
#     all combinations: 3 x 3 = 9 results
#
#   "2" -> ["a","b","c"]
#
# HOW MANY RESULTS CAN THERE BE?
#   Each digit produces 3 or 4 letters (7 and 9 have 4: pqrs, wxyz).
#   With 4 digits, worst case: 4^4 = 256 combinations.
#   The constraint says at most 4 digits, so this stays manageable.
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# THE APPROACH -- Backtracking (building combinations one letter at a time):
#
# Backtracking is a technique where you build a solution piece by piece,
# and if you reach a dead end, you "backtrack" and try the next option.
# Here there are no dead ends -- every path leads to a valid combination --
# so it's really just a systematic way to explore all combinations.
#
# THINK OF IT LIKE A DECISION TREE for "23":
#
#                        ""
#              /          |          \
#            a            b            c        (choices for digit '2')
#          / | \        / | \        / | \
#         ad ae af    bd be bf    cd ce cf      (choices for digit '3')
#
# We walk this tree depth-first, building one combination all the way to a
# leaf (where its length == number of digits), then backtrack.
#
# STEP-BY-STEP for "23":
#
#   Call build("", 0):   index=0, digit='2' -> try 'a','b','c'
#     Call build("a", 1): index=1, digit='3' -> try 'd','e','f'
#       Call build("ad", 2): index=2 == len(digits) -> SAVE "ad"
#       Call build("ae", 2): index=2 == len(digits) -> SAVE "ae"
#       Call build("af", 2): index=2 == len(digits) -> SAVE "af"
#     Call build("b", 1): index=1, digit='3' -> try 'd','e','f'
#       Call build("bd", 2): SAVE "bd"
#       Call build("be", 2): SAVE "be"
#       Call build("bf", 2): SAVE "bf"
#     Call build("c", 1): ... (similarly produces "cd","ce","cf")
#
# The CURRENT string being built acts like a stack -- we add a letter,
# recurse deeper, then the call returns and we try the next letter.
# This "add, recurse, undo" cycle is the essence of backtracking.

def letter_combinations(digits):
    if not digits:
        return []

    # Phone keypad mapping
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    result = []

    def build(current, index):
        # BASE CASE: we've chosen one letter for every digit -> save the combination
        if index == len(digits):
            result.append(current)
            return

        # RECURSIVE CASE: try each letter for the current digit
        for letter in phone[digits[index]]:
            build(current + letter, index + 1)
            # No explicit "undo" needed here because Python strings are
            # immutable -- current + letter creates a NEW string each time,
            # so the original 'current' is unchanged when we try the next letter.

    build("", 0)   # start with empty string at digit index 0
    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(letter_combinations("23"))   # -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
print(letter_combinations("2"))    # -> ["a","b","c"]
print(letter_combinations(""))     # -> []
print(letter_combinations("79"))   # -> 4*4 = 16 combinations


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# The backtracking structure is identical. We pass 'current' as a string --
# JS strings are also immutable, so current + letter creates a new string.
# An object literal is used for the phone mapping (like Python's dict).
#
# function letterCombinations(digits) {
#     if (!digits.length) return [];
#
#     const phone = {
#         '2':'abc','3':'def','4':'ghi','5':'jkl',
#         '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'
#     };
#
#     const result = [];
#
#     function build(current, index) {
#         if (index === digits.length) {
#             result.push(current);
#             return;
#         }
#         for (const letter of phone[digits[index]]) {
#             build(current + letter, index + 1);
#         }
#     }
#
#     build("", 0);
#     return result;
# }
#
# console.log(letterCombinations("23"));
# // -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
# console.log(letterCombinations("2"));
# // -> ["a","b","c"]


# =============================================================================
# 3. JAVA
# =============================================================================
# StringBuilder is used to build the current string efficiently.
# Unlike Python/JS, Java's StringBuilder IS mutable -- so we MUST undo
# the append (with deleteCharAt) after the recursive call returns.
# This explicit "undo" is the classic backtracking pattern in Java/C++.
#
# import java.util.*;
#
# class Solution {
#     private static final String[] PHONE = {
#         "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
#     };
#
#     public List<String> letterCombinations(String digits) {
#         List<String> result = new ArrayList<>();
#         if (digits == null || digits.isEmpty()) return result;
#         build(digits, 0, new StringBuilder(), result);
#         return result;
#     }
#
#     private void build(String digits, int index, StringBuilder current, List<String> result) {
#         if (index == digits.length()) {
#             result.add(current.toString());
#             return;
#         }
#         for (char letter : PHONE[digits.charAt(index) - '0'].toCharArray()) {
#             current.append(letter);             // add
#             build(digits, index + 1, current, result);
#             current.deleteCharAt(current.length() - 1); // UNDO (backtrack)
#         }
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# string& current is passed by reference and mutated in place.
# current.push_back(letter) adds a char; current.pop_back() undoes it.
# This explicit push/pop is the C++ backtracking idiom.
#
# #include <string>
# #include <vector>
# using namespace std;
#
# class Solution {
#     const string PHONE[10] = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
#
#     void build(const string& digits, int index, string& current, vector<string>& result) {
#         if (index == (int)digits.size()) {
#             result.push_back(current);
#             return;
#         }
#         for (char letter : PHONE[digits[index] - '0']) {
#             current.push_back(letter);          // add
#             build(digits, index + 1, current, result);
#             current.pop_back();                  // UNDO (backtrack)
#         }
#     }
#
# public:
#     vector<string> letterCombinations(string digits) {
#         vector<string> result;
#         if (digits.empty()) return result;
#         string current;
#         build(digits, 0, current, result);
#         return result;
#     }
# };


# =============================================================================
# 5. C#
# =============================================================================
# StringBuilder with Append/Remove is used for the mutable current string.
# The Remove(sb.Length - 1, 1) call removes the last character (the undo step).
#
# using System.Collections.Generic;
# using System.Text;
#
# public class Solution {
#     private static readonly string[] PHONE = {
#         "","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"
#     };
#
#     public IList<string> LetterCombinations(string digits) {
#         var result = new List<string>();
#         if (string.IsNullOrEmpty(digits)) return result;
#         Build(digits, 0, new StringBuilder(), result);
#         return result;
#     }
#
#     private void Build(string digits, int index, StringBuilder current, List<string> result) {
#         if (index == digits.Length) {
#             result.Add(current.ToString());
#             return;
#         }
#         foreach (char letter in PHONE[digits[index] - '0']) {
#             current.Append(letter);                       // add
#             Build(digits, index + 1, current, result);
#             current.Remove(current.Length - 1, 1);       // UNDO
#         }
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# Go strings are immutable like Python, so we pass current as a string value
# and current+string(letter) creates a new string -- no explicit undo needed.
# Closures (anonymous functions) capture the outer 'result' and 'phone' vars.
#
# func letterCombinations(digits string) []string {
#     if len(digits) == 0 { return []string{} }
#
#     phone := map[byte]string{
#         '2':"abc",'3':"def",'4':"ghi",'5':"jkl",
#         '6':"mno",'7':"pqrs",'8':"tuv",'9':"wxyz",
#     }
#
#     result := []string{}
#
#     var build func(current string, index int)
#     build = func(current string, index int) {
#         if index == len(digits) {
#             result = append(result, current)
#             return
#         }
#         for _, letter := range phone[digits[index]] {
#             build(current + string(letter), index + 1)
#         }
#     }
#
#     build("", 0)
#     return result
# }


# =============================================================================
# 7. RUST
# =============================================================================
# We pass a mutable Vec<char> as the current path, push and pop for backtracking.
# iter().collect::<String>() converts the Vec<char> back to a String to save.
#
# fn letter_combinations(digits: String) -> Vec<String> {
#     if digits.is_empty() { return vec![]; }
#
#     let phone: std::collections::HashMap<char, &str> = [
#         ('2',"abc"),('3',"def"),('4',"ghi"),('5',"jkl"),
#         ('6',"mno"),('7',"pqrs"),('8',"tuv"),('9',"wxyz"),
#     ].iter().cloned().collect();
#
#     let mut result = Vec::new();
#     let chars: Vec<char> = digits.chars().collect();
#
#     fn build(
#         chars: &[char], index: usize, current: &mut Vec<char>,
#         result: &mut Vec<String>, phone: &std::collections::HashMap<char, &str>
#     ) {
#         if index == chars.len() {
#             result.push(current.iter().collect());
#             return;
#         }
#         for letter in phone[&chars[index]].chars() {
#             current.push(letter);                           // add
#             build(chars, index + 1, current, result, phone);
#             current.pop();                                   // UNDO
#         }
#     }
#
#     build(&chars, 0, &mut Vec::new(), &mut result, &phone);
#     result
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# Strings in Swift are value types (like Python/JS), so passing 'current'
# as a String into a recursive call automatically creates a copy -- no undo needed.
# The local function 'build' captures the mutable 'result' array via inout.
#
# func letterCombinations(_ digits: String) -> [String] {
#     if digits.isEmpty { return [] }
#
#     let phone: [Character: String] = [
#         "2":"abc","3":"def","4":"ghi","5":"jkl",
#         "6":"mno","7":"pqrs","8":"tuv","9":"wxyz"
#     ]
#
#     var result = [String]()
#     let digitsArr = Array(digits)
#
#     func build(_ current: String, _ index: Int) {
#         if index == digitsArr.count {
#             result.append(current)
#             return
#         }
#         for letter in phone[digitsArr[index]] ?? "" {
#             build(current + String(letter), index + 1)
#         }
#     }
#
#     build("", 0)
#     return result
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# Strings are immutable in Kotlin (like Python/JS/Swift), so current + letter
# creates a new string -- no explicit backtracking/undo step needed.
# The inner 'build' function is defined as a local fun inside the main function.
#
# fun letterCombinations(digits: String): List<String> {
#     if (digits.isEmpty()) return emptyList()
#
#     val phone = mapOf(
#         '2' to "abc", '3' to "def", '4' to "ghi", '5' to "jkl",
#         '6' to "mno", '7' to "pqrs", '8' to "tuv", '9' to "wxyz"
#     )
#
#     val result = mutableListOf<String>()
#
#     fun build(current: String, index: Int) {
#         if (index == digits.length) {
#             result.add(current)
#             return
#         }
#         for (letter in phone[digits[index]] ?: "") {
#             build(current + letter, index + 1)
#         }
#     }
#
#     build("", 0)
#     return result
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# Ruby strings ARE mutable, but we build via concatenation (<<current<<letter)
# which creates new strings, keeping the clean immutable-style approach.
# The recursive lambda captures the outer 'result' array automatically.
#
# def letter_combinations(digits)
#   return [] if digits.empty?
#
#   phone = {
#     '2'=>'abc','3'=>'def','4'=>'ghi','5'=>'jkl',
#     '6'=>'mno','7'=>'pqrs','8'=>'tuv','9'=>'wxyz'
#   }
#
#   result = []
#
#   build = lambda do |current, index|
#     if index == digits.length
#       result << current
#       return
#     end
#     phone[digits[index]].each_char do |letter|
#       build.call(current + letter, index + 1)
#     end
#   end
#
#   build.call("", 0)
#   result
# end
#
# puts letter_combinations("23").inspect
# # -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]
# puts letter_combinations("2").inspect
# # -> ["a","b","c"]


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use BACKTRACKING (recursive depth-first tree traversal):
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Define a helper: build(current_string, current_digit_index)   │
#   │                                                                  │
#   │  BASE CASE:                                                      │
#   │    index == len(digits) -> we've placed a letter for every      │
#   │    digit -> save current_string to results                      │
#   │                                                                  │
#   │  RECURSIVE CASE:                                                 │
#   │    For each letter mapped to digits[index]:                     │
#   │      build(current + letter, index + 1)                        │
#   │                                                                  │
#   │  Start: build("", 0)                                            │
#   └──────────────────────────────────────────────────────────────────┘
#
# TWO FLAVOURS OF BACKTRACKING seen across the languages:
#
#   IMMUTABLE strings (Python, JS, Go, Swift, Kotlin):
#     current + letter creates a NEW string each call.
#     No explicit "undo" needed -- the old string is untouched.
#
#   MUTABLE builders (Java, C++, C#, Rust):
#     append/push_back MODIFIES the builder in place.
#     MUST explicitly undo: deleteCharAt / pop_back / Remove / pop.
#     This is the classic "add -> recurse -> undo" backtracking pattern.
#
# Time complexity:  O(4^n * n)  -- at most 4 choices per digit, n digits,
#                                   and each result takes O(n) to build.
# Space complexity: O(n)        -- the recursion stack goes n levels deep.
# =============================================================================
