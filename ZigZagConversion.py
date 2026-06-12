# =============================================================================
# ZIGZAG CONVERSION
# =============================================================================
# PROBLEM: Write a string in a zigzag pattern across a given number of rows,
# then read it back left-to-right, top-to-bottom.
#
# WHAT DOES "ZIGZAG" MEAN HERE?
#   Imagine writing the string diagonally DOWN the rows, then diagonally
#   back UP, then down again — like a lightning bolt / Z shape on its side.
#
#   "PAYPALISHIRING" with numRows = 3:
#
#   Row 0:  P . . A . . H . . N        (every 4th character, starting at 0)
#   Row 1:  . A P . L S . I I . G      (the in-between characters)
#   Row 2:  . . Y . . I . . R          (every 4th character, starting at 2)
#
#   Visually:
#   P   A   H   N
#   A P L S I I G
#   Y   I   R
#
#   Read row by row: "PAHNAPLSIIGYIR"
#
#   "PAYPALISHIRING" with numRows = 4:
#
#   P     I     N
#   A   L S   I G
#   Y A   H R
#   P     I
#
#   Read row by row: "PINALSIGYAHRPI"
# =============================================================================


# =============================================================================
# 1. PYTHON  ✅  (active - try running this!)
# =============================================================================
#
# HOW IT WORKS — simulate the zigzag with a list of buckets:
#
# Create one "bucket" (string) per row.
# Walk through the input string character by character.
# Drop each character into the current row's bucket.
# After each character, move to the next row — but REVERSE DIRECTION
# when you hit the top (row 0) or the bottom (row numRows-1).
# At the end, join all buckets together.
#
# STEP-BY-STEP with "PAYPALISHIRING", numRows=3:
#
#   rows = ["", "", ""]   current_row=0   going_down=True
#
#   'P' → row 0  rows=["P","",""]        going_down stays True  (not at edge)
#   'A' → row 1  rows=["P","A",""]       going_down stays True
#   'Y' → row 2  rows=["P","A","Y"]      HIT BOTTOM → flip to going_down=False
#   'P' → row 1  rows=["P","AP","Y"]     going_down=False
#   'A' → row 0  rows=["PA","AP","Y"]    HIT TOP → flip to going_down=True
#   'L' → row 1  rows=["PA","APL","Y"]
#   'I' → row 2  rows=["PA","APL","YI"]  HIT BOTTOM → flip
#   'S' → row 1  rows=["PA","APLS","YI"]
#   'H' → row 0  rows=["PAH","APLS","YI"] HIT TOP → flip
#   ... and so on
#
#   Final rows: ["PAHN", "APLSIIG", "YIR"]
#   Join: "PAHN" + "APLSIIG" + "YIR" = "PAHNAPLSIIGYIR"  ✓
#
# EDGE CASE: if numRows is 1 (or >= len(s)), there's no zigzag — return as-is.

def convert(s, numRows):
    # No zigzag possible with 1 row or if the string fits in one cycle
    if numRows == 1 or numRows >= len(s):
        return s

    rows = [""] * numRows   # one bucket per row, all start empty
    current_row = 0
    going_down = True       # we start by moving downward

    for char in s:
        rows[current_row] += char   # drop character into current row's bucket

        # Check if we've hit a boundary and need to reverse direction
        if current_row == numRows - 1:   # hit the bottom
            going_down = False
        elif current_row == 0:           # hit the top
            going_down = True

        # Move to the next row
        current_row += 1 if going_down else -1

    return "".join(rows)   # stick all rows together left-to-right, top-to-bottom


# --- Test it out ---
print("=== PYTHON TESTS ===")
print(convert("PAYPALISHIRING", 3))   # → "PAHNAPLSIIGYIR"
print(convert("PAYPALISHIRING", 4))   # → "PINALSIGYAHRPI"
print(convert("A", 1))               # → "A"
print(convert("AB", 1))              # → "AB"


# =============================================================================
# 2. JAVASCRIPT
# =============================================================================
# An array of strings acts as the row buckets.
# The ternary (going_down ? 1 : -1) moves the row index up or down.
#
# function convert(s, numRows) {
#     if (numRows === 1 || numRows >= s.length) return s;
#
#     const rows = Array.from({ length: numRows }, () => "");
#     let currentRow = 0;
#     let goingDown = true;
#
#     for (const char of s) {
#         rows[currentRow] += char;
#
#         if (currentRow === numRows - 1)   goingDown = false;
#         else if (currentRow === 0)        goingDown = true;
#
#         currentRow += goingDown ? 1 : -1;
#     }
#
#     return rows.join("");
# }
#
# console.log(convert("PAYPALISHIRING", 3));   // → "PAHNAPLSIIGYIR"
# console.log(convert("PAYPALISHIRING", 4));   // → "PINALSIGYAHRPI"
# console.log(convert("A", 1));               // → "A"


# =============================================================================
# 3. JAVA
# =============================================================================
# StringBuilder is Java's efficient way to build strings by appending.
# (Regular String concatenation in a loop is slow in Java.)
#
# class Solution {
#     public String convert(String s, int numRows) {
#         if (numRows == 1 || numRows >= s.length()) return s;
#
#         StringBuilder[] rows = new StringBuilder[numRows];
#         for (int k = 0; k < numRows; k++) rows[k] = new StringBuilder();
#
#         int currentRow = 0;
#         boolean goingDown = true;
#
#         for (char c : s.toCharArray()) {
#             rows[currentRow].append(c);
#
#             if (currentRow == numRows - 1)   goingDown = false;
#             else if (currentRow == 0)        goingDown = true;
#
#             currentRow += goingDown ? 1 : -1;
#         }
#
#         StringBuilder result = new StringBuilder();
#         for (StringBuilder row : rows) result.append(row);
#         return result.toString();
#     }
# }


# =============================================================================
# 4. C++
# =============================================================================
# vector<string> holds one string per row.
# The direction variable alternates between +1 (down) and -1 (up).
#
# #include <string>
# #include <vector>
# using namespace std;
#
# string convert(string s, int numRows) {
#     if (numRows == 1 || numRows >= (int)s.size()) return s;
#
#     vector<string> rows(numRows);
#     int currentRow = 0;
#     int direction = 1;   // +1 = going down, -1 = going up
#
#     for (char c : s) {
#         rows[currentRow] += c;
#
#         if (currentRow == numRows - 1)   direction = -1;
#         else if (currentRow == 0)        direction =  1;
#
#         currentRow += direction;
#     }
#
#     string result;
#     for (const string& row : rows) result += row;
#     return result;
# }


# =============================================================================
# 5. C#
# =============================================================================
# StringBuilder[] rows creates an array of StringBuilders — one per row.
# String.Concat joins them all together at the end.
#
# using System.Text;
#
# public class Solution {
#     public string Convert(string s, int numRows) {
#         if (numRows == 1 || numRows >= s.Length) return s;
#
#         var rows = new StringBuilder[numRows];
#         for (int k = 0; k < numRows; k++) rows[k] = new StringBuilder();
#
#         int currentRow = 0;
#         bool goingDown = true;
#
#         foreach (char c in s) {
#             rows[currentRow].Append(c);
#
#             if (currentRow == numRows - 1)   goingDown = false;
#             else if (currentRow == 0)        goingDown = true;
#
#             currentRow += goingDown ? 1 : -1;
#         }
#
#         var result = new StringBuilder();
#         foreach (var row in rows) result.Append(row);
#         return result.ToString();
#     }
# }


# =============================================================================
# 6. GO (Golang)
# =============================================================================
# [][]byte holds a slice of byte slices — one per row — which is efficient
# for building strings by appending. strings.Builder is the modern Go way,
# but []byte is simpler to show here.
#
# import "strings"
#
# func convert(s string, numRows int) string {
#     if numRows == 1 || numRows >= len(s) { return s }
#
#     rows := make([][]byte, numRows)
#     currentRow := 0
#     goingDown := true
#
#     for i := 0; i < len(s); i++ {
#         rows[currentRow] = append(rows[currentRow], s[i])
#
#         if currentRow == numRows-1      { goingDown = false }
#         else if currentRow == 0         { goingDown = true  }
#
#         if goingDown { currentRow++ } else { currentRow-- }
#     }
#
#     var sb strings.Builder
#     for _, row := range rows { sb.Write(row) }
#     return sb.String()
# }


# =============================================================================
# 7. RUST
# =============================================================================
# Vec<String> holds one String per row.
# The direction variable is i32 (+1 or -1) to safely add/subtract from index.
#
# fn convert(s: String, num_rows: i32) -> String {
#     let num_rows = num_rows as usize;
#     if num_rows == 1 || num_rows >= s.len() { return s; }
#
#     let mut rows: Vec<String> = vec![String::new(); num_rows];
#     let mut current_row: i32 = 0;
#     let mut direction: i32 = 1;   // +1 down, -1 up
#
#     for c in s.chars() {
#         rows[current_row as usize].push(c);
#
#         if current_row == num_rows as i32 - 1 { direction = -1; }
#         else if current_row == 0              { direction =  1; }
#
#         current_row += direction;
#     }
#
#     rows.concat()
# }


# =============================================================================
# 8. SWIFT
# =============================================================================
# [String] holds the row buckets. Swift's append() adds a character to a String.
# joined() concatenates an array of strings with no separator.
#
# func convert(_ s: String, _ numRows: Int) -> String {
#     if numRows == 1 || numRows >= s.count { return s }
#
#     var rows = Array(repeating: "", count: numRows)
#     var currentRow = 0
#     var goingDown = true
#
#     for char in s {
#         rows[currentRow].append(char)
#
#         if currentRow == numRows - 1      { goingDown = false }
#         else if currentRow == 0           { goingDown = true  }
#
#         currentRow += goingDown ? 1 : -1
#     }
#
#     return rows.joined()
# }


# =============================================================================
# 9. KOTLIN
# =============================================================================
# StringBuilder for each row, then joinToString("") concatenates them.
# Kotlin's if/else as an expression lets us set direction inline.
#
# fun convert(s: String, numRows: Int): String {
#     if (numRows == 1 || numRows >= s.length) return s
#
#     val rows = Array(numRows) { StringBuilder() }
#     var currentRow = 0
#     var goingDown = true
#
#     for (char in s) {
#         rows[currentRow].append(char)
#
#         if (currentRow == numRows - 1)      goingDown = false
#         else if (currentRow == 0)           goingDown = true
#
#         currentRow += if (goingDown) 1 else -1
#     }
#
#     return rows.joinToString("")
# }


# =============================================================================
# 10. RUBY
# =============================================================================
# An array of strings as row buckets. Ruby's << operator appends to a string.
# .join('') glues all rows together at the end.
#
# def convert(s, num_rows)
#   return s if num_rows == 1 || num_rows >= s.length
#
#   rows = Array.new(num_rows, "")   # ["", "", "", ...]
#   current_row = 0
#   going_down = true
#
#   s.each_char do |char|
#     rows[current_row] << char
#
#     if current_row == num_rows - 1    then going_down = false
#     elsif current_row == 0            then going_down = true
#     end
#
#     current_row += going_down ? 1 : -1
#   end
#
#   rows.join
# end
#
# puts convert("PAYPALISHIRING", 3)   # → "PAHNAPLSIIGYIR"
# puts convert("PAYPALISHIRING", 4)   # → "PINALSIGYAHRPI"
# puts convert("A", 1)               # → "A"


# =============================================================================
# QUICK SUMMARY
# =============================================================================
#
# All 10 solutions use the SIMULATE THE ZIGZAG approach:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Create one bucket (string/builder) per row.                    │
#   │                                                                  │
#   │  Walk the input character by character:                         │
#   │    - Drop the character into the current row's bucket           │
#   │    - Move to the next row (down or up)                          │
#   │    - If you hit the bottom → reverse direction (go up)          │
#   │    - If you hit the top    → reverse direction (go down)        │
#   │                                                                  │
#   │  At the end: concatenate all buckets top-to-bottom.            │
#   └──────────────────────────────────────────────────────────────────┘
#
# Time complexity:  O(n)  — every character is visited exactly once
# Space complexity: O(n)  — the buckets together hold all n characters
#
# The tricky part is purely conceptual — visualising the zigzag.
# Once you see that each character belongs to exactly ONE row and that
# you just bounce a pointer up and down, the code writes itself. ⚡
# =============================================================================
