# Test Data Usage Guide

## Overview
This guide explains how to use the consolidated test data CSV files with the automated workflow tool for testing the 10010-Cash-Custody (USD) reconciliation process.

## Quick Start

### Workflow Summary

| Workflow | Required Inputs | Data Files Needed | Test Cases Covered |
|----------|-----------------|-------------------|---------------------|
| **Workflow 1: Cash Custody Initial Check** | 1. `fund_name` (text)<br>2. `navpack_file` (file)<br>3. `position_report_file` (file)<br>4. `quarter_end_date` (text) | Position Report CSV<br>NAV Pack Excel | 35 test cases (33 PASSED, 2 pending workflow updates) |
| **Workflow 2: Cash Custody Mismatch Analysis** | All Workflow 1 inputs +<br>5. `transaction_report_file` (file)<br>6. `daily_cash_file` (file) | Position Report CSV<br>Transaction Report CSV<br>Daily Cash File CSV<br>NAV Pack Excel | 13 test cases (pending) |

## Workflow 1: Cash Custody Initial Check

### Purpose
Initial balance comparison between bank statement and NAV Pack

### Required Inputs

1. **fund_name** (text): Fund name (e.g., `AP WINDSOR CO-INVEST, L.P.`)
2. **navpack_file** (file): NAV Pack Excel file (e.g., `AP Windsor - NAV Pack.xlsm`)
3. **position_report_file** (file): Position Report CSV - **Note: File may contain multiple rows for same fund (multiple bank accounts) - tool should aggregate**
4. **quarter_end_date** (text): Quarter-end date in format `YYYY-MM-DD` (e.g., `2025-09-30`)

### Process

1. Workflow tool filters Position Report by `Last Update Date` = quarter-end date
2. Workflow tool extracts all cash balances for specified fund name (may be multiple rows for multiple bank accounts)
3. Workflow tool aggregates all balances for the fund (sum all `Available` amounts for matching fund name and date)
4. Workflow tool extracts NAV Pack ending balance for matching date and account 10010-Cash-Custody (USD)
5. Compare aggregated bank balance with NAV Pack balance
6. If match: Test passes, no further action
7. If mismatch: Proceed to Workflow 2: Cash Custody Mismatch Analysis

### Available Position Report Files

| File Name | Purpose | Balance/Scenario | Test Cases |
|-----------|---------|------------------|------------|
| `Test-Data-Position-Report.csv` | Happy path and valid break scenarios | Various balances matching NAV Pack | TC-001, TC-002, TC-003, TC-004, TC-010, TC-010A, TC-011, TC-012, TC-017, TC-018, TC-019, TC-020, TC-021, TC-034-TC-040, TC-042, TC-044, TC-045, TC-046 |
| `Test-Data-Position-Report-Mismatch.csv` | Missing $60,237 expense | Bank: $941,754.36, NAV: $881,517.36 | TC-005, TC-008 |
| `Test-Data-Position-Report-Mismatch-TC006.csv` | Missing $25,000 income | Bank: $906,517.36, NAV: $881,517.36 | TC-006 |
| `Test-Data-Position-Report-Mismatch-TC007.csv` | Multiple missing transactions | Bank: $966,517.36, NAV: $881,517.36 | TC-007 |
| `Test-Data-Position-Report-Mismatch-TC009.csv` | Missing $100k sum | Bank: $981,517.36, NAV: $881,517.36 | TC-009 |
| `Test-Data-Position-Report-EdgeCases-TC041.csv` | Zero balance scenario | Bank: $0.00, NAV: $0.00 | TC-041 |
| `Test-Data-Position-Report-EdgeCases-TC043.csv` | Negative balance scenario | Bank: -$5,000.00, NAV: -$5,000.00 | TC-043 |
| `Test-Data-Position-Report-Exception.csv` | Unknown transaction | Bank: $891,517.36, NAV: $881,517.36 | TC-030, TC-031, TC-032 |
| `Test-Data-Position-Report-Exception-Corrected.csv` | Corrected after bank reversal | Bank: $881,517.36 (corrected) | TC-033 |
| `Test-Data-Position-Report-MultiBank.csv` | Multiple bank accounts (single file) | Aggregated: $881,517.36 ($500,000 + $381,517.36) | TC-027, TC-028, TC-029 |

### Available NAV Pack Files

| File Name | Purpose | Cash Custody Balance | Test Cases |
|-----------|---------|---------------------|------------|
| `AP Windsor - NAV Pack.xlsm` | Original NAV Pack (Q3 2025 only) | $881,517.36 | TC-001, TC-002, TC-003, TC-004, TC-005-TC-016, TC-017-TC-021, TC-027-TC-040, TC-044, TC-045, TC-047 |
| `AP Windsor - NAV Pack - TC-041-Zero-Balance.xlsm` | Zero balance test | $0.00 | TC-041 |
| `AP Windsor - NAV Pack - TC-042-Very-Large-Balance.xlsm` | Very large balance test | $10,000,000.00 | TC-042 |
| `AP Windsor - NAV Pack - TC-043-Negative-Balance.xlsm` | Negative balance test | -$5,000.00 | TC-043 |

### Test Cases Covered by Workflow 1 (35 test cases)

| Test Case | Scenario | Position Report File | NAV Pack File | Fund Name | Quarter-End Date | Expected Result |
|-----------|----------|---------------------|-----------|------------------|-----------------|
| **TC-001** | Happy Path - Balance Match | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Match: $881,517.36 |
| **TC-002** | Multiple Currency Accounts - USD Only Processing | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Verify only USD ($881,517.36) is extracted and processed; EUR (€500,000) and GBP (£25,000) are ignored. Workflow should filter to USD only |
| **TC-003** | Single Bank Account | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Match: $881,517.36 |
| **TC-004** | All Quarters Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-03-31, 2025-06-30, 2025-09-30, 2025-12-31 | ✅ All quarters match |
| **TC-005** | Mismatch - Missing $60,237 Expense | `Test-Data-Position-Report-Mismatch.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $941,754.36, NAV $881,517.36 |
| **TC-006** | Mismatch - Missing $25,000 Income | `Test-Data-Position-Report-Mismatch-TC006.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $906,517.36, NAV $881,517.36 |
| **TC-007** | Mismatch - Multiple Missing Transactions | `Test-Data-Position-Report-Mismatch-TC007.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $966,517.36, NAV $881,517.36 |
| **TC-008** | Mismatch - Exact Transaction Match | `Test-Data-Position-Report-Mismatch.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $941,754.36, NAV $881,517.36 |
| **TC-009** | Mismatch - Sum of Transactions | `Test-Data-Position-Report-Mismatch-TC009.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $981,517.36, NAV $881,517.36 |
| **TC-010** | Valid Break - Post Cut-Off | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $881,517.36, NAV $876,517.36 (valid break) |
| **TC-010A** | Valid Break - Cut-Off Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $881,517.36, NAV $876,517.36 (valid break) |
| **TC-011** | Valid Break - Next Day Statement | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Transaction appears in 10/01 statement |
| **TC-012** | Valid Break - Multiple Post Cut-Off | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Multiple post cut-off transactions |
| **TC-017** | Q1 Data Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-03-31 | ✅ Q1 data matches Q1 NAV Pack (logic validated) |
| **TC-018** | Q2 Data Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-06-30 | ✅ Q2 data matches Q2 NAV Pack (logic validated) |
| **TC-019** | Q3 Data Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Q3 data matches Q3 NAV Pack |
| **TC-020** | Q4 Data Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-12-31 | ✅ Q4 data matches Q4 NAV Pack (logic validated) |
| **TC-021** | Quarter-End Date Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-03-31, 2025-06-30, 2025-09-30, 2025-12-31 | ✅ Correct quarter-end dates validated |
| **TC-027** | Multiple Bank Accounts | `Test-Data-Position-Report-MultiBank.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Aggregated: $881,517.36 ($500,000 + $381,517.36) |
| **TC-028** | Multiple Bank Portals | `Test-Data-Position-Report-MultiBank.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Both accounts Q3 2025 validated |
| **TC-029** | Aggregate Balances | `Test-Data-Position-Report-MultiBank.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Aggregated: $881,517.36 (sums all accounts for fund) |
| **TC-030** | Unknown Transaction | `Test-Data-Position-Report-Exception.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Mismatch: Bank $891,517.36, NAV $881,517.36 |
| **TC-033** | Bank Correction | `Test-Data-Position-Report-Exception-Corrected.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Corrected: $881,517.36 (after reversal) |
| **TC-034** | Position Report Date Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | ✅ Date validation |
| **TC-035** | Fund Name Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Fund name matches |
| **TC-036** | Currency Code Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ USD currency validated |
| **TC-037** | Account Number Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Account number format validated |
| **TC-038** | Quarter Selection Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | Q1, Q2, Q3, Q4 | ✅ Quarter selection validated |
| **TC-039** | Year Selection Validation | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025 | ✅ Year selection validated |
| **TC-040** | Quarter Consistency | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | ✅ All data sources Q3 2025 |
| **TC-041** | Zero Balance | `Test-Data-Position-Report-EdgeCases-TC041.csv` | `AP Windsor - NAV Pack - TC-041-Zero-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: $0.00 - Matched |
| **TC-042** | Very Large Balance | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack - TC-042-Very-Large-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: $10,000,000.00 - Matched |
| **TC-043** | Negative Balance | `Test-Data-Position-Report-EdgeCases-TC043.csv` | `AP Windsor - NAV Pack - TC-043-Negative-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: -$5,000.00 - Matched |
| **TC-044** | Position Report Not Available | N/A (Error Handling) | Any fund | 2025-09-30 | Error message displayed |
| **TC-045** | Fund Not Found | `Test-Data-Position-Report.csv` | NON-EXISTENT FUND, L.P. | 2025-09-30 | Error message displayed |
| **TC-046** | Weekend/Holiday Quarter-End | `Test-Data-Position-Report.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | ⚠️ **NEEDS WORKFLOW UPDATE** - Should detect quarter mismatch error |
| **TC-047** | Missing NAV Pack | N/A (Error Handling) | N/A | Any fund | 2025-09-30 | ✅ Error message displayed |

## Workflow 2: Cash Custody Mismatch Analysis

### Purpose
Analyze discrepancies and identify missing transactions

### Required Inputs

**All Workflow 1 inputs plus:**
5. **transaction_report_file** (file): Transaction Report CSV (e.g., `Test-Data-Transaction-Report.csv`)
6. **daily_cash_file** (file): Daily Cash File CSV (e.g., `Test-Data-Daily-Cash-File.csv`)

**Complete list of 6 inputs:**
1. `fund_name` (text)
2. `navpack_file` (file)
3. `position_report_file` (file)
4. `quarter_end_date` (text)
5. `transaction_report_file` (file)
6. `daily_cash_file` (file)

### Process

1. Identify discrepancy amount from Workflow 1
2. Filter Transaction Report by quarter period (based on quarter_end_date)
3. Filter Daily Cash File by quarter period
4. Compare Transaction Report entries with Daily Cash File entries
5. Identify missing transactions (present in Transaction Report but not in Daily Cash File)
6. Check for post cut-off time transactions (after 21:00 ET)
7. Classify as valid break or require remediation

### Required Data Files

| File Type | File Name | Purpose |
|-----------|-----------|---------|
| Position Report | Various (see test cases) | Bank balance data |
| Transaction Report | `Test-Data-Transaction-Report.csv` | All transactions across quarters |
| Daily Cash File | `Test-Data-Daily-Cash-File.csv` | Transactions entered into Investran |
| NAV Pack | `AP Windsor - NAV Pack.xlsm` | Ending balance reference |

### Test Cases Covered by Workflow 2 (16 test cases)

| Test Case | Scenario | Position Report File | Transaction Report | Daily Cash File | Expected Result |
|-----------|----------|---------------------|-------------------|-----------------|-----------------|
| **TC-005** | Missing $60,237 Expense | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing: $60,237 expense on 2025-09-15 |
| **TC-006** | Missing $25,000 Income | `Test-Data-Position-Report-Mismatch-TC006.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing: $25,000 income on 2025-09-20 |
| **TC-007** | Multiple Missing Transactions | `Test-Data-Position-Report-Mismatch-TC007.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing: $35,000 expense + $50,000 income |
| **TC-008** | Exact Transaction Match | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing: $60,237 (exact match to discrepancy) |
| **TC-009** | Sum of Transactions | `Test-Data-Position-Report-Mismatch-TC009.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing: $40k + $35k + $25k = $100k |
| **TC-010** | Post Cut-Off Transaction | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Valid break: $5,000 at 22:00 ET |
| **TC-010A** | Cut-Off Time Validation | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Valid break: After 21:00 ET |
| **TC-011** | Next Day Statement | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Transaction in 10/01 statement |
| **TC-012** | Multiple Post Cut-Off | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Multiple post cut-off transactions |
| **TC-013** | Identify Missing Transaction | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Missing transaction identified |
| **TC-022** | Transaction Data Quarter Validation | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | All transactions within Q3 2025 |
| **TC-023** | Daily Cash File Quarter Validation | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | All transactions within Q3 2025 |
| **TC-030** | Unknown Transaction | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Unknown $10,000 transaction identified |
| **TC-031** | Contact Bank | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Unknown transaction flagged for bank contact |
| **TC-032** | Reverse Transaction | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | Reversal of -$10,000 on 2025-09-25 |
| **TC-040** | Quarter Consistency Validation | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | All data sources validated as Q3 2025 |

**Note**: TC-014, TC-015, TC-016 (Remediation Workflow) require Workflow 2 to identify missing transactions first, then manual remediation entry booking in Investran.

## Test Case to Workflow Mapping

### Complete Reference Table

| Test Case | Test Case Name | Workflow(s) | position_report_file | transaction_report_file | daily_cash_file | navpack_file | fund_name | quarter_end_date | Expected Result |
|-----------|----------------|-------------|---------------------|------------------------|-----------------|--------------|-----------|------------------|-----------------|
| **TC-001** | Happy Path - Balance Match | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Match: $881,517.36 |
| **TC-002** | Multiple Currency Accounts - USD Only Processing | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Verify only USD ($881,517.36) extracted; EUR/GBP ignored. Match: $881,517.36 |
| **TC-003** | Single Bank Account | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Match: $881,517.36 |
| **TC-004** | All Quarters Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-03-31, 2025-06-30, 2025-09-30, 2025-12-31 | All quarters match |
| **TC-005** | Missing $60,237 Expense | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing: $60,237 expense |
| **TC-006** | Missing $25,000 Income | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch-TC006.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing: $25,000 income |
| **TC-007** | Multiple Missing Transactions | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch-TC007.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing: $35k expense + $50k income |
| **TC-008** | Exact Transaction Match | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing: $60,237 (exact match) |
| **TC-009** | Sum of Transactions | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch-TC009.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing: $100k (sum) |
| **TC-010** | Post Cut-Off Transaction | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Valid break: $5,000 at 22:00 ET |
| **TC-010A** | Cut-Off Time Validation | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Valid break: After 21:00 ET |
| **TC-011** | Next Day Statement | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Transaction in 10/01 statement |
| **TC-012** | Multiple Post Cut-Off | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Multiple post cut-off transactions |
| **TC-013** | Identify Missing Transaction | Workflow 1 + 2 | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Missing transaction identified |
| **TC-014** | Book Remediating Entry (Expense) | Workflow 2 + Manual | `Test-Data-Position-Report-Mismatch.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Book $60,237 entry in Investran |
| **TC-015** | Book Remediating Entry (Income) | Workflow 2 + Manual | `Test-Data-Position-Report-Mismatch-TC006.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Book $25,000 entry in Investran |
| **TC-016** | Verify Break Resolved | Workflow 1 (after remediation) | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Break resolved, balances match |
| **TC-017** | Q1 Data Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-03-31 | Q1 data matches Q1 NAV Pack |
| **TC-018** | Q2 Data Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-06-30 | Q2 data matches Q2 NAV Pack |
| **TC-019** | Q3 Data Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Q3 data matches Q3 NAV Pack |
| **TC-020** | Q4 Data Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-12-31 | Q4 data matches Q4 NAV Pack |
| **TC-021** | Quarter-End Date Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-03-31, 2025-06-30, 2025-09-30, 2025-12-31 | Correct quarter-end dates validated |
| **TC-022** | Transaction Data Quarter Validation | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | All transactions within Q3 2025 |
| **TC-023** | Daily Cash File Quarter Validation | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | All transactions within Q3 2025 |
| **TC-024** | Quarter Mismatch - Position vs NAV | Workflow 1 only | `Test-Data-Position-Report.csv` (Q3) + Q2 NAV Pack | N/A | N/A | `AP Windsor - NAV Pack.xlsm` (Q2) | Any fund | 2025-09-30 vs 2025-06-30 | Error: Quarter mismatch |
| **TC-025** | Quarter Mismatch - Position vs Transaction | Workflow 1 + 2 | `Test-Data-Position-Report.csv` (Q3) + Q2 Transaction | `Test-Data-Transaction-Report.csv` (Q2) | `Test-Data-Daily-Cash-File.csv` (Q2) | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 vs 2025-06-30 | Error: Quarter mismatch |
| **TC-026** | Quarter Mismatch - All Sources | Workflow 1 + 2 | `Test-Data-Position-Report.csv` (Q3) | `Test-Data-Transaction-Report.csv` (Q2) | `Test-Data-Daily-Cash-File.csv` (Q2) | `AP Windsor - NAV Pack.xlsm` (Q2) | Any fund | 2025-09-30 vs 2025-06-30 | Error: Quarter mismatch |
| **TC-027** | Multiple Bank Accounts | Workflow 1 only | `Test-Data-Position-Report-MultiBank.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Aggregated: $881,517.36 |
| **TC-028** | Multiple Bank Portals | Workflow 1 only | `Test-Data-Position-Report-MultiBank.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Both accounts Q3 2025 validated |
| **TC-029** | Aggregate Balances | Workflow 1 only | `Test-Data-Position-Report-MultiBank.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Aggregated: $881,517.36 |
| **TC-030** | Unknown Transaction | Workflow 1 + 2 | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Unknown $10,000 transaction identified |
| **TC-031** | Contact Bank | Workflow 1 + 2 | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Unknown transaction flagged for bank contact |
| **TC-032** | Reverse Transaction | Workflow 1 + 2 | `Test-Data-Position-Report-Exception.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Reversal of -$10,000 on 2025-09-25 |
| **TC-033** | Bank Correction | Workflow 1 only | `Test-Data-Position-Report-Exception-Corrected.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Corrected: $881,517.36 (after reversal) |
| **TC-034** | Position Report Date Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | Date validation |
| **TC-035** | Fund Name Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Fund name matches |
| **TC-036** | Currency Code Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | USD currency validated |
| **TC-037** | Account Number Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | Account number format validated |
| **TC-038** | Quarter Selection Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | Q1, Q2, Q3, Q4 | Quarter selection validated |
| **TC-039** | Year Selection Validation | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025 | Year selection validated |
| **TC-040** | Quarter Consistency | Workflow 1 + 2 | `Test-Data-Position-Report.csv` | `Test-Data-Transaction-Report.csv` | `Test-Data-Daily-Cash-File.csv` | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | All data sources Q3 2025 |
| **TC-041** | Zero Balance | Workflow 1 only | `Test-Data-Position-Report-EdgeCases-TC041.csv` | N/A | N/A | `AP Windsor - NAV Pack - TC-041-Zero-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: $0.00 - Matched |
| **TC-042** | Very Large Balance | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack - TC-042-Very-Large-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: $10,000,000.00 - Matched |
| **TC-043** | Negative Balance | Workflow 1 only | `Test-Data-Position-Report-EdgeCases-TC043.csv` | N/A | N/A | `AP Windsor - NAV Pack - TC-043-Negative-Balance.xlsm` | AP WINDSOR CO-INVEST, L.P. | 2025-09-30 | ✅ Balance: -$5,000.00 - Matched |
| **TC-044** | Position Report Not Available | Workflow 1 only (Error) | N/A | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | ✅ Error message displayed |
| **TC-045** | Fund Not Found | Workflow 1 only (Error) | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | NON-EXISTENT FUND, L.P. | 2025-09-30 | ✅ Error message displayed |
| **TC-046** | Weekend/Holiday Quarter-End | Workflow 1 only | `Test-Data-Position-Report.csv` | N/A | N/A | `AP Windsor - NAV Pack.xlsm` | Any fund | 2025-09-30 | ⚠️ **NEEDS WORKFLOW UPDATE** - Should detect quarter mismatch error |
| **TC-047** | Missing NAV Pack | Workflow 1 only (Error) | `Test-Data-Position-Report.csv` | N/A | N/A | N/A | Any fund | 2025-09-30 | ✅ Error message displayed |

## Test Data File Descriptions

### 1. Position Report CSV
**File**: `Test-Data-Position-Report.csv`

**Contains**: Bank position data for all quarter-end dates (Q1, Q2, Q3, Q4 2025)

**How to Filter**: Filter rows where `Last Update Date` column equals the quarter-end date
- Q1 2025: `2025-03-31`
- Q2 2025: `2025-06-30`
- Q3 2025: `2025-09-30`
- Q4 2025: `2025-12-31`

**Key Columns**:
- `Account Name`: Fund name (e.g., "AP WINDSOR CO-INVEST, L.P.")
- `Linked Custody Account`: Account number (e.g., "FFK30")
- `Cash Account CCY Code`: Currency code (e.g., "USD")
- `Available`: Cash balance amount
- `Last Update Date`: Quarter-end date for filtering

### 2. Transaction Report CSV
**File**: `Test-Data-Transaction-Report.csv`

**Contains**: All transactions across all quarters

**How to Filter**: Filter rows where `Transaction Date` falls within the quarter period
- Q1 2025: `2025-01-01` to `2025-03-31`
- Q2 2025: `2025-04-01` to `2025-06-30`
- Q3 2025: `2025-07-01` to `2025-09-30`
- Q4 2025: `2025-10-01` to `2025-12-31`

**Key Columns**:
- `Fund`: Fund name
- `Account Number`: Account number
- `Transaction Date`: Date of transaction
- `Transaction Time`: Time of transaction (for cut-off time scenarios)
- `Transaction Type`: "Expense" or "Income"
- `Amount`: Transaction amount
- `In Daily Cash File`: "Yes" or "No" (indicates if transaction should be in daily cash file)

### 3. Daily Cash File CSV
**File**: `Test-Data-Daily-Cash-File.csv`

**Contains**: Daily cash file transactions across all quarters

**How to Filter**: Filter rows where `Transaction Date` falls within the quarter period (same as Transaction Report)

**Key Columns**:
- `Fund`: Fund name
- `Account Number`: Account number
- `Transaction Date`: Date of transaction
- `Transaction Type`: "Expense" or "Income"
- `Amount`: Transaction amount

## Example Workflow Tool Calls

### Workflow 1: Cash Custody Initial Check - Happy Path Example
```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack.xlsm
- position_report_file: Test-Data-Position-Report.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance: $881,517.36
- NAV Pack Balance: $881,517.36
- Match: Yes
- Discrepancy: $0.00
- Status: Pass - No further action required
```

### Workflow 1: Cash Custody Initial Check - Mismatch Detected Example
```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack.xlsm
- position_report_file: Test-Data-Position-Report-Mismatch.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance: $941,754.36
- NAV Pack Balance: $881,517.36
- Match: No
- Discrepancy: $60,237.00
- Status: Mismatch detected - Proceed to Workflow 2
```

### Workflow 1: Multiple Bank Accounts Example
**Note**: The position report contains multiple rows for the same fund (different bank accounts). The workflow tool should aggregate all balances for the fund name and quarter-end date.

```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack.xlsm
- position_report_file: Test-Data-Position-Report-MultiBank.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance (Account 1 - FFK30): $500,000.00
- Bank Balance (Account 2 - FFK30-ALT): $381,517.36
- Aggregated Bank Balance: $881,517.36
- NAV Pack Balance: $881,517.36
- Match: Yes
- Status: Pass - All bank accounts aggregated correctly
```

### Workflow 1: Edge Case Examples

#### TC-041: Zero Balance
```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack - TC-041-Zero-Balance.xlsm
- position_report_file: Test-Data-Position-Report-EdgeCases-TC041.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance: $0.00
- NAV Pack Balance: $0.00
- Match: Yes
- Status: Pass - Zero balance handled correctly
```

#### TC-042: Very Large Balance
```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack - TC-042-Very-Large-Balance.xlsm
- position_report_file: Test-Data-Position-Report.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance: $10,000,000.00
- NAV Pack Balance: $10,000,000.00
- Match: Yes
- Status: Pass - Very large balance handled correctly
```

#### TC-043: Negative Balance
```
Inputs:
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack - TC-043-Negative-Balance.xlsm
- position_report_file: Test-Data-Position-Report-EdgeCases-TC043.csv
- quarter_end_date: 2025-09-30

Expected Output:
- Bank Balance: -$5,000.00
- NAV Pack Balance: -$5,000.00
- Match: Yes
- Status: Pass - Negative balance (overdraft) handled correctly
```

### Workflow 2: Cash Custody Mismatch Analysis Example
```
Inputs (from Workflow 1 + additional):
- fund_name: "AP WINDSOR CO-INVEST, L.P."
- navpack_file: AP Windsor - NAV Pack.xlsm
- position_report_file: Test-Data-Position-Report-Mismatch.csv
- quarter_end_date: 2025-09-30
- transaction_report_file: Test-Data-Transaction-Report.csv
- daily_cash_file: Test-Data-Daily-Cash-File.csv

Expected Output:
- Discrepancy: $60,237.00
- Missing Transaction Found: Yes
- Missing Transaction Details:
  - Date: 2025-09-15
  - Type: Expense
  - Amount: $60,237.00
  - Status: Present in Transaction Report but missing from Daily Cash File
- Action Required: Remediation entry needed
```

## Available Test Data Values

### Fund Names (for fund_name input)
- `AP WINDSOR CO-INVEST, L.P.` (Account: FFK30) - **Primary test fund** (matches NAV Pack)
- `NON-EXISTENT FUND, L.P.` - For error handling tests (TC-045)

**Note**: Other funds exist in test data files but cannot be tested without corresponding NAV Pack entries. All testable scenarios use `AP WINDSOR CO-INVEST, L.P.`

### Quarter-End Dates (for quarter_end_date input)
- `2025-03-31` (Q1 2025)
- `2025-06-30` (Q2 2025)
- `2025-09-30` (Q3 2025)
- `2025-12-31` (Q4 2025)

### Test Data Files Summary
- **Position Report (Happy Path)**: `Test-Data-Position-Report.csv` - Use for happy path and valid break scenarios
- **Position Report (Mismatch - TC-005/TC-008)**: `Test-Data-Position-Report-Mismatch.csv` - Balance: $941,754.36
- **Position Report (Mismatch - TC-006)**: `Test-Data-Position-Report-Mismatch-TC006.csv` - Balance: $906,517.36
- **Position Report (Mismatch - TC-007)**: `Test-Data-Position-Report-Mismatch-TC007.csv` - Balance: $966,517.36
- **Position Report (Mismatch - TC-009)**: `Test-Data-Position-Report-Mismatch-TC009.csv` - Balance: $981,517.36
- **Position Report (Edge Cases)**: `Test-Data-Position-Report-EdgeCases.csv` - Contains zero balance and negative balance scenarios
- **Position Report (Exception Scenarios)**: `Test-Data-Position-Report-Exception.csv` - Contains unknown transaction scenario (Balance: $891,517.36 with $10,000 unknown transaction)
- **Position Report (Exception - Corrected)**: `Test-Data-Position-Report-Exception-Corrected.csv` - Contains corrected balance after bank reversal (Balance: $881,517.36)
- **Position Report (Multiple Banks)**: `Test-Data-Position-Report-MultiBank.csv` - Contains 2 bank accounts for same fund: FFK30 ($500,000) + FFK30-ALT ($381,517.36), aggregates to $881,517.36
- **Transaction Report**: `Test-Data-Transaction-Report.csv` - Contains all transactions across quarters (includes exception scenarios)
- **Daily Cash File**: `Test-Data-Daily-Cash-File.csv` - Contains transactions that were entered into Investran
- **NAV Pack**: `AP Windsor - NAV Pack.xlsm` (sample file)

## Notes

- **Primary Test Fund**: Most test cases use `AP WINDSOR CO-INVEST, L.P.` (Account: FFK30) since the NAV Pack file only contains data for this fund. All testable scenarios are based on this fund.

- **Multi-Currency Testing**: TC-002 tests that when a fund has multiple currencies (USD, EUR, GBP), only USD is processed and other currencies are ignored. The position report contains EUR and GBP entries for AP WINDSOR CO-INVEST, L.P. for Q3 2025, but the workflow should filter to only USD entries and calculate balance based on USD only ($881,517.36).

- **Multiple Bank Accounts**: Position reports may contain multiple rows for the same fund (different bank accounts). The workflow tool should automatically aggregate all balances for the fund name and quarter-end date. See `Test-Data-Position-Report-MultiBank.csv` for example.

- All test data is organized in consolidated CSV files to allow the workflow tool to filter by quarter-end date
- The workflow tool should handle date filtering automatically based on the provided quarter-end date
- Quarter consistency is enforced: Q1 data only tests against Q1, Q2 against Q2, etc.
- Cut-off time for JP Morgan is 21:00 ET
- Workflow 1 (Initial Check) is required first; Workflow 2 (Mismatch Analysis) is only needed when a discrepancy is detected
