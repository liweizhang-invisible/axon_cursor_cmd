# Test Data Files Index

## Overview
This document provides a complete index of all test data files and their usage for testing the 10010-Cash-Custody (USD) reconciliation workflows.

**Important Note**: All testable scenarios use `AP WINDSOR CO-INVEST, L.P.` (Account: FFK30) as the fund name since the NAV Pack file (`AP Windsor - NAV Pack.xlsm`) only contains data for this fund. The workflow tools are designed for USD-only reconciliation, so non-USD currencies in position reports are automatically ignored.

## Position Report Files

### Happy Path & Valid Break Scenarios
- **`Test-Data-Position-Report.csv`**
  - **Purpose**: Happy path scenarios and valid break scenarios
  - **Contains**: All quarters (Q1, Q2, Q3, Q4 2025) with matching balances
  - **Key Balances for AP WINDSOR CO-INVEST, L.P. (FFK30)**:
    - Q3 2025: USD $881,517.36 (matches NAV Pack)
    - Q3 2025: EUR €500,000.00 (for TC-002 - should be ignored by workflow)
    - Q3 2025: GBP £25,000.00 (for TC-002 - should be ignored by workflow)
  - **Test Cases**: TC-001, TC-002, TC-003, TC-004, TC-010, TC-010A, TC-011, TC-012
  - **Note**: TC-002 tests that workflow correctly filters to only USD and ignores EUR/GBP entries

### Mismatch Scenarios
- **`Test-Data-Position-Report-Mismatch.csv`**
  - **Purpose**: TC-005/TC-008 - Missing $60,237 expense transaction
  - **Q3 2025 Balance**: $941,754.36 (discrepancy: $60,237)
  - **Test Cases**: TC-005, TC-008

- **`Test-Data-Position-Report-Mismatch-TC006.csv`**
  - **Purpose**: TC-006 - Missing $25,000 income transaction
  - **Q3 2025 Balance**: $906,517.36 (discrepancy: $25,000)
  - **Test Cases**: TC-006

- **`Test-Data-Position-Report-Mismatch-TC007.csv`**
  - **Purpose**: TC-007 - Multiple missing transactions ($35,000 + $50,000)
  - **Q3 2025 Balance**: $966,517.36 (discrepancy: $85,000)
  - **Test Cases**: TC-007

- **`Test-Data-Position-Report-Mismatch-TC009.csv`**
  - **Purpose**: TC-009 - Missing transactions summing to $100,000
  - **Q3 2025 Balance**: $981,517.36 (discrepancy: $100,000)
  - **Test Cases**: TC-009

### Edge Cases
- **`Test-Data-Position-Report-EdgeCases.csv`**
  - **Purpose**: Edge case scenarios
  - **Contains**:
    - Zero balance fund (ZERO01): $0.00
    - Negative balance fund (NEG01): -$5,000.00
  - **Test Cases**: TC-041, TC-043

### Exception Scenarios
- **`Test-Data-Position-Report-Exception.csv`**
  - **Purpose**: Unknown/incorrect transaction scenarios
  - **Q3 2025 Balance**: $891,517.36 (includes $10,000 unknown transaction)
  - **Test Cases**: TC-030, TC-031

- **`Test-Data-Position-Report-Exception-Corrected.csv`**
  - **Purpose**: Corrected statement after bank reversal
  - **Q3 2025 Balance**: $881,517.36 (corrected after $10,000 reversal)
  - **Test Cases**: TC-033

### Multiple Bank Accounts
- **`Test-Data-Position-Report-MultiBank.csv`**
  - **Purpose**: Single position report with multiple bank accounts for same fund
  - **Contains**: 2 rows for "AP WINDSOR CO-INVEST, L.P." with different account numbers:
    - Account FFK30: $500,000.00
    - Account FFK30-ALT: $381,517.36
  - **Aggregated Total**: $881,517.36 (workflow should sum both accounts)
  - **Test Cases**: TC-027, TC-028, TC-029
  - **Note**: Workflow tool should aggregate all rows for the same fund name and quarter-end date

## Transaction Report File

- **`Test-Data-Transaction-Report.csv`**
  - **Purpose**: All transactions across all quarters
  - **Contains**:
    - Happy path transactions (Q1, Q2, Q3)
    - Missing transactions for mismatch scenarios:
      - $60,237 expense (TC-005/TC-008)
      - $25,000 income (TC-006)
      - $35,000 expense + $50,000 income (TC-007)
      - $40,000 + $35,000 + $25,000 expenses (TC-009)
    - Post cut-off transactions (TC-010, TC-010A, TC-011, TC-012)
    - Unknown transaction: $10,000 (TC-030/TC-031)
    - Reversal transaction: -$10,000 (TC-032/TC-033)
  - **Key Column**: `In Daily Cash File` - "Yes" or "No" indicates if transaction should be in daily cash file
  - **Test Cases**: All mismatch detection, valid break, and exception scenarios

## Daily Cash File

- **`Test-Data-Daily-Cash-File.csv`**
  - **Purpose**: Transactions that were entered into Investran
  - **Contains**: Only transactions marked as "Yes" in Transaction Report
  - **Missing**: All transactions marked as "No" in Transaction Report (these cause mismatches)
  - **Test Cases**: All mismatch detection scenarios (TC-005 to TC-009, TC-013)

## Test Data by Test Case Category

### Happy Path (4 test cases)
- **Files**: `Test-Data-Position-Report.csv`
- **Coverage**: ✅ Complete

### Mismatch Detection (5 test cases)
- **Files**: 
  - Mismatch position reports (4 files)
  - `Test-Data-Transaction-Report.csv`
  - `Test-Data-Daily-Cash-File.csv`
- **Coverage**: ✅ Complete

### Valid Break Scenarios (4 test cases)
- **Files**: 
  - `Test-Data-Position-Report.csv`
  - `Test-Data-Transaction-Report.csv`
- **Coverage**: ✅ Complete

### Remediation Workflow (4 test cases)
- **Files**: 
  - Mismatch position reports
  - `Test-Data-Transaction-Report.csv`
  - `Test-Data-Daily-Cash-File.csv`
- **Coverage**: ✅ Complete (requires Workflow 2 execution)

### Quarterly Data Consistency (10 test cases)
- **Files**: `Test-Data-Position-Report.csv` (all quarters)
- **Coverage**: ✅ Complete (validation logic testing)

### Multiple Bank Accounts (3 test cases)
- **Files**: 
  - `Test-Data-Position-Report-MultiBank.csv` (single file with 2 accounts)
- **Coverage**: ✅ Complete

### Exception Handling (4 test cases)
- **Files**: 
  - `Test-Data-Position-Report-Exception.csv`
  - `Test-Data-Position-Report-Exception-Corrected.csv`
  - `Test-Data-Transaction-Report.csv`
- **Coverage**: ✅ Complete

### Edge Cases (8 test cases)
- **Files**: 
  - `Test-Data-Position-Report-EdgeCases.csv` (zero, negative balance scenarios)
  - `Test-Data-Position-Report.csv` (for validation tests)
  - Error handling tests (no data files needed)
- **Coverage**: ⚠️ **Partial** - TC-041, TC-042, TC-043 require NAV Pack updates for AP WINDSOR to test edge case balances

### Data Validation (7 test cases)
- **Files**: `Test-Data-Position-Report.csv` (validation logic testing)
- **Coverage**: ✅ Complete

## Summary

**Total Test Data Files**: 11
- Position Reports: 9 files
- Transaction Report: 1 file
- Daily Cash File: 1 file

**Test Case Coverage**: 
- **Fully Testable**: 46/49 test cases have complete test data available
- **Requires NAV Pack Updates**: 3 test cases (TC-041, TC-042, TC-043) need NAV Pack entries for edge case scenarios
- ✅ All core scenarios covered
- ✅ All mismatch scenarios covered
- ✅ All exception scenarios covered
- ✅ All validation scenarios covered
- ⚠️ Edge cases partially covered (require NAV Pack updates)

**Ready for Testing**: 46 test cases are ready to use with the workflow tools. All testable scenarios use `AP WINDSOR CO-INVEST, L.P.` as the fund name.

