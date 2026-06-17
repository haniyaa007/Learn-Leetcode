# =============================================================================
# INTEGER TO ROMAN
# =============================================================================
# PROBLEM: Convert an integer (1 to 3999) into a Roman numeral string.
#
# ROMAN NUMERAL BASICS:
#   Symbol:  I    V    X    L    C    D    M
#   Value:   1    5   10   50  100  500  1000
#
# THE SUBTRACTIVE SPECIAL CASES (the "4s and 9s"):
#   Instead of IIII (4), Romans wrote IV  (one before five)
#   Instead of VIIII(9), Romans wrote IX  (one before ten)
#   Instead of XXXX(40), Romans wrote XL  (ten before fifty)
#   Instead of LXXXX(90),Romans wrote XC  (ten before hundred)
#   Instead of CCCC(400),Romans wrote CD  (hundred before five-hundred)
#   Instead of DCCCC(900),Romans wrote CM  (hundred before thousand)
#
# THE KEY TRICK:
#   If we just include the subtractive pairs in our lookup table, sorted
#   from LARGEST to SMALLEST, we can greedily subtract the biggest value
#   that fits and append its symbol -- no special case logic needed!
# =============================================================================


# =============================================================================
# 1. PYTHON  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS -- greedy subtraction with a lookup table:
#
# Build a list of (value, symbol) pairs ordered from LARGEST to SMALLEST.
# Include the six subtractive pairs (CM, CD, XC, XL, IX, IV) right in the table.
#
# Then for each (value, symbol) pair:
#   While num >= value: append symbol to result, subtract value from num.
#   Move to the next (smaller) pair.
#
# STEP-BY-STEP with num = 1994:
#
#   1994 >= 1000? YES -> result="M",     num=994
#    994 >= 1000? NO  -> move on
#    994 >=  900? YES -> result="MCM",   num=94
#     94 >=  900? NO  -> ...
#     94 >=  500? NO
#     94 >=  400? NO
#     94 >=  100? NO
#     94 >=   90? YES -> result="MCMXC", num=4
#      4 >=   90? NO  -> ...
#      4 >=   50? NO
#      4 >=   40? NO
#      4 >=   10? NO
#      4 >=    9? NO
#      4 >=    5? NO
#      4 >=    4? YES -> result="MCMXCIV", num=0
#   num=0, done!
#   Answer: "MCMXCIV" ✓

def int_to_roman(num):
    # The full lookup table, LARGEST to SMALLEST.
    # Subtractive pairs (CM, CD, XC, XL, IX, IV) are included naturally.
    values_and_symbols = [
        (1000, "M"),
        ( 900, "CM"),
        ( 500, "D"),
        ( 400, "CD"),
        ( 100, "C"),
        (  90, "XC"),
        (  50, "L"),
        (  40, "XL"),
        (  10, "X"),
        (   9, "IX"),
        (   5, "V"),
        (   4, "IV"),
        (   1, "I"),
    ]

    result = ""

    for value, symbol in values_and_symbols:
        while num >= value:       # keep subtracting as long as it fits
            result += symbol      # append this symbol
            num    -= value       # subtract this value

    return result


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(int_to_roman(3749))   # -> "MMMDCCXLIX"
print(int_to_roman(58))     # -> "LVIII"
print(int_to_roman(1994))   # -> "MCMXCIV"
print(int_to_roman(3999))   # -> "MMMCMXCIX"
print(int_to_roman(4))      # -> "IV"
print(int_to_roman(9))      # -> "IX"
print(int_to_roman(1))      # -> "I"


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# Arrays of pairs work the same way. We use a for...of loop instead of
# Python's for...in, and while (num >= value) subtracts greedily.
#
# function intToRoman(num) {
#     const valSyms = [
#         [1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],
#         [100,"C"],[90,"XC"],[50,"L"],[40,"XL"],
#         [10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]
#     ];
#
#     let result = "";
#
#     for (const [value, symbol] of valSyms) {
#         while (num >= value) {
#             result += symbol;
#             num    -= value;
#         }
#     }
#
#     return result;
# }
#
# console.log(intToRoman(3749));   // -> "MMMDCCXLIX"
# console.log(intToRoman(58));     // -> "LVIII"
# console.log(intToRoman(1994));   // -> "MCMXCIV"


# =============================================================================
# 3. JAVA
# =============================================================================
# Two parallel arrays (one for values, one for symbols) work cleanly in Java.
# StringBuilder is efficient for building strings by appending.
#
# class Solution {
#     public String intToRoman(int num) {
#         int[]    values  = {1000,900,500,400,100,90,50,40,10,9,5,4,1};
#         String[] symbols = {"M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"};
#
#         StringBuilder result = new StringBuilder();
#
#         for (int i = 0; i < values.length; i++) {
#             while (num >= values[i]) {
#                 result.append(symbols[i]);
#                 num -= values[i];
#             }
#         }
#
#         return result.toString();
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# A vector of pairs<int,string> holds the lookup table.
# The string result is built by += (string concatenation).
#
# #include <string>
# #include <vector>
# using namespace std;
#
# string intToRoman(int num) {
#     vector<pair<int,string>> valSyms = {
#         {1000,"M"},{900,"CM"},{500,"D"},{400,"CD"},
#         {100,"C"},{90,"XC"},{50,"L"},{40,"XL"},
#         {10,"X"},{9,"IX"},{5,"V"},{4,"IV"},{1,"I"}
#     };
#
#     string result;
#
#     for (auto& [value, symbol] : valSyms) {
#         while (num >= value) {
#             result += symbol;
#             num    -= value;
#         }
#     }
#
#     return result;
# }


# =============================================================================
# 5. C#
# =============================================================================
# A list of ValueTuples (int value, string symbol) holds the table.
# string.Concat or += builds the result. The foreach loop is clean.
#
# public class Solution {
#     public string IntToRoman(int num) {
#         var valSyms = new (int v, string s)[] {
#             (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
#             (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
#             (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")
#         };
#
#         string result = "";
#
#         foreach (var (value, symbol) in valSyms) {
#             while (num >= value) {
#                 result += symbol;
#                 num    -= value;
#             }
#         }
#
#         return result;
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# A struct holds the value/symbol pair. Slice of structs is idiomatic Go.
# strings.Builder is Go's efficient way to build strings by appending.
#
# import "strings"
#
# func intToRoman(num int) string {
#     type pair struct { val int; sym string }
#     valSyms := []pair{
#         {1000,"M"},{900,"CM"},{500,"D"},{400,"CD"},
#         {100,"C"},{90,"XC"},{50,"L"},{40,"XL"},
#         {10,"X"},{9,"IX"},{5,"V"},{4,"IV"},{1,"I"},
#     }
#
#     var sb strings.Builder
#
#     for _, p := range valSyms {
#         for num >= p.val {
#             sb.WriteString(p.sym)
#             num -= p.val
#         }
#     }
#
#     return sb.String()
# }


# =============================================================================
# 7. RUST
# =============================================================================
# An array of (i32, &str) tuples holds the lookup table.
# String::new() creates an empty String; push_str() appends a &str.
#
# fn int_to_roman(mut num: i32) -> String {
#     let val_syms: &[(i32, &str)] = &[
#         (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
#         (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
#         (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I"),
#     ];
#
#     let mut result = String::new();
#
#     for &(value, symbol) in val_syms {
#         while num >= value {
#             result.push_str(symbol);
#             num -= value;
#         }
#     }
#
#     result
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# An array of tuples (Int, String) holds the lookup table.
# String concatenation with += builds the result cleanly.
#
# func intToRoman(_ num: Int) -> String {
#     let valSyms: [(Int, String)] = [
#         (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
#         (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
#         (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")
#     ]
#
#     var result = ""
#     var n = num
#
#     for (value, symbol) in valSyms {
#         while n >= value {
#             result += symbol
#             n -= value
#         }
#     }
#
#     return result
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# A list of Pair<Int, String> holds the table. buildString is Kotlin's
# efficient string builder DSL -- append() inside it builds the result.
#
# fun intToRoman(num: Int): String {
#     val valSyms = listOf(
#         1000 to "M", 900 to "CM", 500 to "D", 400 to "CD",
#         100  to "C",  90 to "XC",  50 to "L",  40 to "XL",
#          10  to "X",   9 to "IX",   5 to "V",   4 to "IV",
#           1  to "I"
#     )
#
#     var n = num
#     return buildString {
#         for ((value, symbol) in valSyms) {
#             while (n >= value) {
#                 append(symbol)
#                 n -= value
#             }
#         }
#     }
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# An array of [value, symbol] pairs. << appends to a string in Ruby.
# The inner while loop subtracts greedily, just like every other language.
#
# def int_to_roman(num)
#   val_syms = [
#     [1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],
#     [100,"C"],[90,"XC"],[50,"L"],[40,"XL"],
#     [10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]
#   ]
#
#   result = ""
#
#   val_syms.each do |value, symbol|
#     while num >= value
#       result << symbol
#       num    -= value
#     end
#   end
#
#   result
# end
#
# puts int_to_roman(3749)   # -> "MMMDCCXLIX"
# puts int_to_roman(58)     # -> "LVIII"
# puts int_to_roman(1994)   # -> "MCMXCIV"


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use GREEDY SUBTRACTION with a lookup table:
#
#   Build a table of 13 (value, symbol) pairs, largest to smallest.
#   Include the 6 subtractive forms (CM, CD, XC, XL, IX, IV) in the table.
#
#   For each (value, symbol):
#     While num >= value:
#       append symbol to result
#       subtract value from num
#
#   Return result.
#
# WHY DOES GREEDY WORK HERE?
#   Roman numerals are built by place value (thousands, hundreds, tens, ones).
#   Taking the largest possible symbol at each step always builds the correct
#   representation -- there's no case where taking a smaller symbol first
#   would lead to a better (shorter/more correct) answer.
#
# WHY INCLUDE CM, CD, XC, XL, IX, IV IN THE TABLE?
#   These six "subtractive pairs" are the only exceptions to the normal rules.
#   By hardcoding them into the table (between the relevant single symbols),
#   the greedy loop handles them automatically -- no if/else needed!
#
# Time complexity:  O(1)  -- the loop runs at most 13 iterations total,
#                            and the while subloop runs at most 3 times
#                            (since no symbol repeats more than 3 times).
#                            The input is bounded to 1-3999, so it's constant.
# Space complexity: O(1)  -- the table has exactly 13 entries, always.
# =============================================================================
