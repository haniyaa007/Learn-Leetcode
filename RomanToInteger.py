# =============================================================================
# ROMAN TO INTEGER
# =============================================================================
# PROBLEM: Convert a Roman numeral string into an integer.
#
# THE NORMAL RULE (largest to smallest, left to right -- just ADD):
#   "XII"  ->  X(10) + I(1) + I(1)  = 12
#   "VIII" ->  V(5) + I(1) + I(1) + I(1) = 8
#
# THE SUBTRACTION RULE (a smaller symbol BEFORE a larger one -- SUBTRACT it):
#   "IV"   ->  5 - 1  = 4    (I before V)
#   "IX"   ->  10 - 1 = 9    (I before X)
#   "XL"   ->  50 - 10 = 40  (X before L)
#   "XC"   ->  100 - 10 = 90 (X before C)
#   "CD"   ->  500 - 100 = 400 (C before D)
#   "CM"   ->  1000 - 100 = 900 (C before M)
#
# THE KEY INSIGHT:
#   When is a symbol subtracted instead of added?
#   Exactly when the NEXT symbol has a LARGER value than the current one.
#   So we only need to compare each symbol to the one after it!
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS -- one pass, peek at the next character:
#
# Walk through the string. For each character:
#   - Look up its value in a dictionary.
#   - If the NEXT character has a LARGER value -> SUBTRACT the current one.
#   - Otherwise                               -> ADD the current one.
#
# STEP-BY-STEP with "MCMXCIV":
#
#   i=0  char='M'  val=1000  next='C'(100)   1000 > 100 -> ADD  1000  total=1000
#   i=1  char='C'  val=100   next='M'(1000)   100 < 1000 -> SUB   100  total=900
#   i=2  char='M'  val=1000  next='X'(10)   1000 > 10  -> ADD  1000  total=1900
#   i=3  char='X'  val=10    next='C'(100)    10 < 100  -> SUB    10  total=1890
#   i=4  char='C'  val=100   next='I'(1)     100 > 1   -> ADD   100  total=1990
#   i=5  char='I'  val=1     next='V'(5)       1 < 5   -> SUB     1  total=1989
#   i=6  char='V'  val=5     no next           -> ADD     5  total=1994
#   Answer: 1994 ✓
#
# ALTERNATIVE ONE-LINER APPROACH:
#   Some people check pairs left-to-right and handle the two-character
#   subtractive cases explicitly. The "peek ahead" approach here is cleaner.

def roman_to_int(s):
    # Lookup table: Roman symbol -> integer value
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
             'C': 100, 'D': 500, 'M': 1000}

    total = 0

    for i in range(len(s)):
        current = value[s[i]]

        # Is there a next character AND is it larger than the current one?
        if i + 1 < len(s) and value[s[i + 1]] > current:
            total -= current   # subtractive case: e.g. I before V -> subtract I
        else:
            total += current   # normal case: just add it

    return total


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(roman_to_int("III"))      # -> 3
print(roman_to_int("LVIII"))    # -> 58
print(roman_to_int("MCMXCIV"))  # -> 1994
print(roman_to_int("IV"))       # -> 4
print(roman_to_int("IX"))       # -> 9
print(roman_to_int("MMMCMXCIX")) # -> 3999


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# An object acts as the lookup table (like Python's dict).
# s[i+1] returns undefined if out of bounds, and value[undefined] is also
# undefined (falsy), so the condition safely handles the last character.
#
# function romanToInt(s) {
#     const value = {I:1, V:5, X:10, L:50, C:100, D:500, M:1000};
#     let total = 0;
#
#     for (let i = 0; i < s.length; i++) {
#         const current = value[s[i]];
#         const next    = value[s[i + 1]];   // undefined if last char (falsy)
#
#         if (next > current) total -= current;
#         else                total += current;
#     }
#
#     return total;
# }
#
# console.log(romanToInt("III"));       // -> 3
# console.log(romanToInt("LVIII"));     // -> 58
# console.log(romanToInt("MCMXCIV"));   // -> 1994


# =============================================================================
# 3. JAVA
# =============================================================================
# HashMap<Character, Integer> maps each Roman char to its integer value.
# s.charAt(i) accesses the character at position i.
# getOrDefault(key, 0) safely returns 0 if the key is missing.
#
# import java.util.HashMap;
# import java.util.Map;
#
# class Solution {
#     public int romanToInt(String s) {
#         Map<Character, Integer> value = new HashMap<>();
#         value.put('I', 1);   value.put('V', 5);   value.put('X', 10);
#         value.put('L', 50);  value.put('C', 100);  value.put('D', 500);
#         value.put('M', 1000);
#
#         int total = 0;
#
#         for (int i = 0; i < s.length(); i++) {
#             int current = value.get(s.charAt(i));
#             int next    = (i + 1 < s.length()) ? value.get(s.charAt(i + 1)) : 0;
#
#             if (next > current) total -= current;
#             else                total += current;
#         }
#
#         return total;
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# unordered_map<char, int> is the lookup table.
# s[i] accesses a character directly. The ternary handles the last character.
#
# #include <string>
# #include <unordered_map>
# using namespace std;
#
# int romanToInt(string s) {
#     unordered_map<char,int> value = {
#         {'I',1},{'V',5},{'X',10},{'L',50},
#         {'C',100},{'D',500},{'M',1000}
#     };
#
#     int total = 0;
#
#     for (int i = 0; i < (int)s.size(); i++) {
#         int current = value[s[i]];
#         int next    = (i + 1 < (int)s.size()) ? value[s[i + 1]] : 0;
#
#         if (next > current) total -= current;
#         else                total += current;
#     }
#
#     return total;
# }


# =============================================================================
# 5. C#
# =============================================================================
# Dictionary<char, int> is C#'s lookup table. s[i] indexes the string.
# The conditional expression handles the last character safely.
#
# using System.Collections.Generic;
#
# public class Solution {
#     public int RomanToInt(string s) {
#         var value = new Dictionary<char, int> {
#             {'I',1},{'V',5},{'X',10},{'L',50},
#             {'C',100},{'D',500},{'M',1000}
#         };
#
#         int total = 0;
#
#         for (int i = 0; i < s.Length; i++) {
#             int current = value[s[i]];
#             int next    = (i + 1 < s.Length) ? value[s[i + 1]] : 0;
#
#             if (next > current) total -= current;
#             else                total += current;
#         }
#
#         return total;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# map[byte]int maps each byte (ASCII character) to its integer value.
# s[i] returns a byte in Go, which is perfect for our char lookup.
#
# func romanToInt(s string) int {
#     value := map[byte]int{
#         'I':1,'V':5,'X':10,'L':50,
#         'C':100,'D':500,'M':1000,
#     }
#
#     total := 0
#
#     for i := 0; i < len(s); i++ {
#         current := value[s[i]]
#         next    := 0
#         if i+1 < len(s) { next = value[s[i+1]] }
#
#         if next > current { total -= current } else { total += current }
#     }
#
#     return total
# }


# =============================================================================
# 7. RUST
# =============================================================================
# A match expression maps each byte to its value (no HashMap needed for
# such a small fixed set -- match is clean and fast).
# as_bytes() converts the string to a byte slice for easy indexing.
#
# fn roman_to_int(s: String) -> i32 {
#     let val = |c: u8| match c {
#         b'I' => 1, b'V' => 5,   b'X' => 10,
#         b'L' => 50, b'C' => 100, b'D' => 500,
#         b'M' => 1000, _ => 0,
#     };
#
#     let bytes = s.as_bytes();
#     let mut total = 0i32;
#
#     for i in 0..bytes.len() {
#         let current = val(bytes[i]);
#         let next    = if i + 1 < bytes.len() { val(bytes[i + 1]) } else { 0 };
#
#         if next > current { total -= current; }
#         else              { total += current; }
#     }
#
#     total
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# A Dictionary<Character, Int> holds the lookup. Array(s) converts
# the String to [Character] for easy indexed access.
#
# func romanToInt(_ s: String) -> Int {
#     let value: [Character: Int] = [
#         "I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000
#     ]
#
#     let chars = Array(s)
#     var total = 0
#
#     for i in 0..<chars.count {
#         let current = value[chars[i]] ?? 0
#         let next    = (i + 1 < chars.count) ? (value[chars[i + 1]] ?? 0) : 0
#
#         if next > current { total -= current }
#         else              { total += current }
#     }
#
#     return total
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# mapOf<Char, Int> holds the lookup table. s[i] gives a Char in Kotlin.
# getOrDefault(key, 0) safely handles missing keys (won't happen here,
# but it's good defensive practice).
#
# fun romanToInt(s: String): Int {
#     val value = mapOf(
#         'I' to 1, 'V' to 5, 'X' to 10, 'L' to 50,
#         'C' to 100, 'D' to 500, 'M' to 1000
#     )
#
#     var total = 0
#
#     for (i in s.indices) {
#         val current = value[s[i]] ?: 0
#         val next    = if (i + 1 < s.length) value[s[i + 1]] ?: 0 else 0
#
#         if (next > current) total -= current
#         else                total += current
#     }
#
#     return total
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# A plain hash maps each Roman character to its value.
# each_char.with_index gives (character, index) pairs neatly.
# The safe navigation &. handles the nil case when i is the last index.
#
# def roman_to_int(s)
#   value = {'I'=>1,'V'=>5,'X'=>10,'L'=>50,'C'=>100,'D'=>500,'M'=>1000}
#   total = 0
#
#   s.each_char.with_index do |char, i|
#     current = value[char]
#     next_val = value[s[i + 1]] || 0   # nil if last char, || 0 makes it safe
#
#     if next_val > current
#       total -= current
#     else
#       total += current
#     end
#   end
#
#   total
# end
#
# puts roman_to_int("III")       # -> 3
# puts roman_to_int("LVIII")     # -> 58
# puts roman_to_int("MCMXCIV")   # -> 1994


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the PEEK-AHEAD / SUBTRACT-IF-SMALLER rule:
#
#   Build a dictionary: Roman char -> integer value
#
#   Walk the string left to right. For each character:
#     current = value[s[i]]
#     next    = value[s[i+1]]  (or 0 if last character)
#
#     if next > current:  total -= current   (subtractive case)
#     else:               total += current   (normal case)
#
#   Return total.
#
# WHY DOES THIS WORK?
#   In every subtractive pair (IV, IX, XL, XC, CD, CM), the first symbol
#   is always SMALLER than the second. So "is the next symbol bigger?"
#   is the exact condition that identifies every subtractive case.
#
# This is the REVERSE of problem 12 (Integer to Roman):
#   Problem 12: greedily subtract the biggest fitting value, build a string.
#   Problem 13: greedily add each symbol, subtract when peeking sees bigger.
#
# Time complexity:  O(n)  -- one pass through the string
# Space complexity: O(1)  -- the dictionary has exactly 7 entries, always
# =============================================================================
