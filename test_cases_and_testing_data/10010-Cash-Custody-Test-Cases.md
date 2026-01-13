# Test Cases for 10010-Cash-Custody (USD) Business Process

## Overview
This document contains comprehensive test cases for the NAV Pack Review process for 10010-Cash-Custody (USD) account reconciliation. All test cases ensure quarterly data consistency (Q1 data only tests against Q1, Q2 against Q2, etc.).

---

## 1. Happy Path Test Cases

### TC-001: Successful Balance Match Between Bank Statement and NAV Pack
**Objective**: Verify that when bank statement cash balance matches NAV Pack ending balance, no further action is required.

**Prerequisites**:
- Position report data available for the fund (e.g., AP Windsor Co-Invest L.P.)
- NAV Pack data available for the fund for the required quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. Extract cash balance for "AP WINDSOR CO-INVEST, L.P." (Account: FFK30) from position report
3. NAV Pack for AP Windsor Co-Invest L.P. for Q3 2025 (09.30.2025) is processed by workflow tool
4. Extract ending balance for account 10010-Cash-Custody (USD) from NAV Pack
5. Compare the two balances

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Cash Balance (USD): $881,517.36
- NAV Pack Ending Balance (USD): $881,517.36

**Expected Results**:
- Balances match exactly
- No discrepancy identified
- No further action required
- Test passes

**Priority**: High
**Category**: Happy Path

---

### TC-002: Multiple Currency Accounts Reconciliation
**Objective**: Verify reconciliation process works correctly when a fund has multiple currency accounts (USD, EUR, GBP).

**Prerequisites**:
- Position report data available for a fund with multiple currency accounts
- NAV Pack data available for the same fund for the required quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. Identify fund with multiple currencies (e.g., APOLLO LINCOLN FIXED INCOME FUND, L.P. - AEY28)
3. Extract USD cash balance from position report
4. Extract EUR cash balance from position report
5. Extract GBP cash balance from position report
6. NAV Pack for the same fund for Q3 2025 is processed by workflow tool
7. Compare each currency balance separately

**Test Data**:
- Fund: APOLLO LINCOLN FIXED INCOME FUND, L.P.
- Account Number: AEY28
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement USD Balance: $2,161,488.30
- Bank Statement EUR Balance: €1,937,624.29
- Bank Statement GBP Balance: £38,566.25
- NAV Pack USD Ending Balance: $2,161,488.30
- NAV Pack EUR Ending Balance: €1,937,624.29
- NAV Pack GBP Ending Balance: £38,566.25

**Expected Results**:
- All currency balances match between bank statement and NAV Pack
- No discrepancies for any currency
- Test passes

**Priority**: High
**Category**: Happy Path

---

### TC-003: Fund with Single Bank Account Reconciliation
**Objective**: Verify reconciliation process for a fund with only one bank account.

**Prerequisites**:
- Position report data available for a fund with single bank account
- NAV Pack data available for the same fund for the required quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. Identify fund with single account (e.g., APOLLO CREDIT OPPORTUNITY FUND III, LP - ABC75)
3. Extract USD cash balance from position report
4. NAV Pack for the same fund for Q3 2025 is processed by workflow tool
5. Compare the balances

**Test Data**:
- Fund: APOLLO CREDIT OPPORTUNITY FUND III, LP
- Account Number: ABC75 (P 13961)
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Cash Balance (USD): $183,048.53
- NAV Pack Ending Balance (USD): $183,048.53

**Expected Results**:
- Balances match exactly
- No discrepancy identified
- Test passes

**Priority**: Medium
**Category**: Happy Path

---

### TC-004: Quarterly Position Report Processing
**Objective**: Verify that position reports can be processed for each quarter (Q1, Q2, Q3, Q4).

**Prerequisites**:
- Position report data available for Q1, Q2, Q3, Q4
- NAV Pack data available for Q1, Q2, Q3, Q4

**Test Steps**:
1. Position report for Q1 2025 (as of 03/31/2025) is processed by workflow tool
2. Position report for Q2 2025 (as of 06/30/2025) is processed by workflow tool
3. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
4. Position report for Q4 2025 (as of 12/31/2025) is processed by workflow tool
5. Verify each report contains data for the correct quarter-end date
6. Process each report and verify it matches the corresponding NAV Pack

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Q1 2025 Position Report Date: 03/31/2025
- Q2 2025 Position Report Date: 06/30/2025
- Q3 2025 Position Report Date: 09/30/2025
- Q4 2025 Position Report Date: 12/31/2025

**Expected Results**:
- All quarterly position reports processed successfully
- Each report contains data for the correct quarter-end date
- Each report can be matched with corresponding NAV Pack
- Test passes

**Priority**: High
**Category**: Happy Path

---

## 2. Mismatch Detection Test Cases

### TC-005: Missing Expense Transaction in Daily Cash File
**Objective**: Verify that a missing expense transaction in the daily cash file is detected when comparing transaction report to daily cash file.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy between bank statement and NAV Pack (e.g., $60,237)
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Compare transaction report entries with daily cash file entries
7. Identify missing expense transaction of $60,237 in daily cash file

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $941,754.36
- NAV Pack Ending Balance: $881,517.36
- Discrepancy: $60,237.00
- Missing Transaction: Expense of $60,237.00 (present in transaction report, missing in daily cash file)

**Expected Results**:
- Discrepancy identified: $60,237.00
- Missing expense transaction found in transaction report but not in daily cash file
- Root cause identified: Missing expense entry
- Test passes

**Priority**: High
**Category**: Mismatch Detection

---

### TC-006: Missing Income Transaction in Daily Cash File
**Objective**: Verify that a missing income transaction in the daily cash file is detected.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy between bank statement and NAV Pack (e.g., $25,000)
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Compare transaction report entries with daily cash file entries
7. Identify missing income transaction of $25,000 in daily cash file

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $906,517.36
- NAV Pack Ending Balance: $881,517.36
- Discrepancy: $25,000.00
- Missing Transaction: Income of $25,000.00 (present in transaction report, missing in daily cash file)

**Expected Results**:
- Discrepancy identified: $25,000.00
- Missing income transaction found in transaction report but not in daily cash file
- Root cause identified: Missing income entry
- Test passes

**Priority**: High
**Category**: Mismatch Detection

---

### TC-007: Multiple Missing Transactions Causing Break
**Objective**: Verify that multiple missing transactions are detected when causing a discrepancy.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy between bank statement and NAV Pack (e.g., $85,000)
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Compare transaction report entries with daily cash file entries
7. Identify multiple missing transactions: $35,000 expense and $50,000 income

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $966,517.36
- NAV Pack Ending Balance: $881,517.36
- Discrepancy: $85,000.00
- Missing Transactions:
  - Expense: $35,000.00 (present in transaction report, missing in daily cash file)
  - Income: $50,000.00 (present in transaction report, missing in daily cash file)

**Expected Results**:
- Discrepancy identified: $85,000.00
- Multiple missing transactions identified
- All missing transactions listed
- Test passes

**Priority**: High
**Category**: Mismatch Detection

---

### TC-008: Break Amount Matches Single Transaction Amount
**Objective**: Verify that when break amount exactly matches a single transaction amount, that transaction is identified as the root cause.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $60,237.00
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Search transaction report for transaction amount of $60,237.00
7. Verify this transaction is missing from daily cash file

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $941,754.36
- NAV Pack Ending Balance: $881,517.36
- Discrepancy: $60,237.00
- Missing Transaction: $60,237.00 expense (exact match to discrepancy)

**Expected Results**:
- Discrepancy matches single transaction amount exactly
- Transaction identified as root cause
- Test passes

**Priority**: Medium
**Category**: Mismatch Detection

---

### TC-009: Break Amount Matches Sum of Multiple Transactions
**Objective**: Verify that when break amount matches the sum of multiple transactions, all transactions are identified.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $100,000.00
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Search transaction report for transactions that sum to $100,000.00
7. Verify these transactions are missing from daily cash file

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $981,517.36
- NAV Pack Ending Balance: $881,517.36
- Discrepancy: $100,000.00
- Missing Transactions:
  - Transaction 1: $40,000.00
  - Transaction 2: $35,000.00
  - Transaction 3: $25,000.00
  - Sum: $100,000.00

**Expected Results**:
- Discrepancy matches sum of multiple transactions
- All contributing transactions identified
- Test passes

**Priority**: Medium
**Category**: Mismatch Detection

---

## 3. Valid Break Scenarios

### TC-010: Post Cut-Off Time Transaction (Expense Paid After 9/30 Cut-Off)
**Objective**: Verify that a transaction made after quarter-end cut-off time (21:00 ET) is correctly identified as a valid break requiring no action.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data for Q3 2025
- Transaction report data showing post cut-off transaction
- Transaction report data for 10/01/2025

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $5,000.00
4. Transaction report for 09/30/2025 is processed by workflow tool
5. Transaction report for 10/01/2025 is processed by workflow tool
6. Identify expense of $5,000.00 paid on 09/30/2025 after 21:00 ET cut-off time
7. Verify transaction appears in 10/01/2025 bank statement
8. Classify as valid break requiring no action

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance (09/30/2025): $881,517.36
- NAV Pack Ending Balance (09/30/2025): $876,517.36
- Discrepancy: $5,000.00
- Transaction: Expense of $5,000.00 paid on 09/30/2025 at 22:00 ET (after 21:00 ET cut-off)
- Cut-Off Time: 21:00 ET (JP Morgan standard)
- Transaction appears in: 10/01/2025 bank statement

**Expected Results**:
- Discrepancy identified: $5,000.00
- Transaction identified as post cut-off time transaction (after 21:00 ET)
- Transaction appears in next day's bank statement
- System correctly identifies as valid break - no action required
- Test passes

**Priority**: High
**Category**: Valid Break Scenarios

---

### TC-011: Transaction Appears in Next Day's Bank Statement
**Objective**: Verify that transactions appearing in the next day's bank statement are correctly identified as valid breaks.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data for Q3 2025
- Transaction report data for 09/30/2025 and 10/01/2025

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy
4. Transaction report for 10/01/2025 is processed by workflow tool
5. Identify transaction that occurred on 09/30/2025 after 21:00 ET cut-off but appears in 10/01/2025 statement
6. Classify as valid break

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance (09/30/2025): $881,517.36
- NAV Pack Ending Balance (09/30/2025): $876,517.36
- Discrepancy: $5,000.00
- Transaction Date: 09/30/2025 (after 21:00 ET cut-off)
- Cut-Off Time: 21:00 ET (JP Morgan standard)
- Transaction appears in: 10/01/2025 bank statement
- Transaction Amount: $5,000.00 expense

**Expected Results**:
- Transaction identified in next day's statement
- System correctly identifies as valid break (post 21:00 ET cut-off)
- No action required
- Test passes

**Priority**: High
**Category**: Valid Break Scenarios

---

### TC-012: Multiple Post Cut-Off Transactions
**Objective**: Verify that multiple post cut-off time transactions (after 21:00 ET) are all correctly identified as valid breaks.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data for Q3 2025
- Transaction report data showing multiple post cut-off transactions

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $15,000.00
4. Transaction report for 10/01/2025 is processed by workflow tool
5. Identify multiple transactions that occurred after 09/30/2025 21:00 ET cut-off
6. Classify all as valid breaks

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance (09/30/2025): $881,517.36
- NAV Pack Ending Balance (09/30/2025): $866,517.36
- Discrepancy: $15,000.00
- Cut-Off Time: 21:00 ET (JP Morgan standard)
- Post Cut-Off Transactions:
  - Transaction 1: $5,000.00 expense (09/30/2025 22:00 ET)
  - Transaction 2: $7,000.00 expense (09/30/2025 23:00 ET)
  - Transaction 3: $3,000.00 expense (09/30/2025 23:30 ET)
  - All appear in: 10/01/2025 bank statement

**Expected Results**:
- Multiple post cut-off transactions identified (all after 21:00 ET)
- All transactions appear in next day's statement
- System correctly identifies all as valid breaks
- No action required
- Test passes

**Priority**: Medium
**Category**: Valid Break Scenarios

---

### TC-010A: Cut-Off Time Validation (21:00 ET) - Expense Paid After Cut-Off
**Objective**: Verify that expenses paid after the 21:00 ET cut-off time on quarter-end date are correctly identified as valid breaks, as Investran will reflect the balance including the expense but the bank statement for the quarter-end date will not reflect this entry since it was done past cut-off time.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data for Q3 2025
- Transaction report data for 09/30/2025
- Transaction report data for 10/01/2025

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $5,000.00
4. Transaction report for 09/30/2025 is processed by workflow tool
5. Identify expense of $5,000.00 paid on 09/30/2025 at 22:00 ET (after 21:00 ET cut-off)
6. Verify Investran reflects balance including the $5,000 expense
7. Verify bank statement for 09/30/2025 does not reflect this entry
8. Transaction report for 10/01/2025 is processed by workflow tool
9. Verify transaction appears in 10/01/2025 bank statement
10. Classify as valid break requiring no action

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance (09/30/2025): $881,517.36
- NAV Pack Ending Balance (09/30/2025): $876,517.36 (includes $5,000 expense in Investran)
- Discrepancy: $5,000.00
- Transaction: Expense of $5,000.00 paid on 09/30/2025 at 22:00 ET
- Cut-Off Time: 21:00 ET (JP Morgan standard)
- Transaction appears in: 10/01/2025 bank statement
- Investran Status: Balance includes $5,000 expense
- Bank Statement Status: Does not include $5,000 expense on 09/30/2025

**Expected Results**:
- Discrepancy identified: $5,000.00
- Transaction identified as post cut-off time transaction (after 21:00 ET)
- Investran balance correctly includes the expense
- Bank statement for 09/30/2025 correctly excludes the expense
- Transaction appears in next day's (10/01/2025) bank statement
- System correctly identifies as valid break - no further action required
- Test passes

**Priority**: High
**Category**: Valid Break Scenarios

---

## 4. Remediation Workflow Test Cases

### TC-013: Identify Missing Transaction in Transaction Report vs Daily Cash File
**Objective**: Verify that missing transactions are correctly identified by comparing transaction report to daily cash file.

**Prerequisites**:
- Position report data for Q3 2025
- NAV Pack data with discrepancy
- Transaction report data for the quarter
- Daily cash file data for the quarter

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy: $60,237.00
4. Transaction report for Q3 2025 is processed by workflow tool
5. Daily cash file for Q3 2025 is processed by workflow tool
6. Compare each transaction in transaction report with daily cash file
7. Identify transaction of $60,237.00 expense present in transaction report but missing in daily cash file

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Discrepancy: $60,237.00
- Transaction Report Entry: Expense $60,237.00 on 09/15/2025
- Daily Cash File Entry: Not present

**Expected Results**:
- Missing transaction identified: $60,237.00 expense
- Transaction details captured (date, amount, type)
- Ready for remediation entry
- Test passes

**Priority**: High
**Category**: Remediation Workflow

---

### TC-014: Book Remediating Entry in Investran for Missing Expense
**Objective**: Verify that a remediating entry can be booked in Investran for a missing expense transaction.

**Prerequisites**:
- Missing transaction identified (from TC-013)
- Investran system integration available
- System has appropriate permissions to book entries

**Test Steps**:
1. Identify missing expense transaction: $60,237.00
2. Create remediating journal entry in Investran
3. Select fund: AP WINDSOR CO-INVEST, L.P.
4. Select account: 10010-Cash-Custody (USD)
5. Enter debit amount: $60,237.00
6. Select appropriate expense account for credit
7. Enter transaction date: 09/15/2025
8. Enter description: "Remediating entry for missing expense transaction"
9. Post the entry to Investran
10. Verify entry is posted successfully

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account: 10010-Cash-Custody (USD)
- Transaction Date: 09/15/2025
- Amount: $60,237.00
- Transaction Type: Expense
- Debit: 10010-Cash-Custody (USD) $60,237.00
- Credit: [Appropriate Expense Account] $60,237.00

**Expected Results**:
- Journal entry created successfully
- Entry posted to Investran
- Entry reflects in trial balance
- Test passes

**Priority**: High
**Category**: Remediation Workflow

---

### TC-015: Book Remediating Entry in Investran for Missing Income
**Objective**: Verify that a remediating entry can be booked in Investran for a missing income transaction.

**Prerequisites**:
- Missing transaction identified
- Investran system integration available
- System has appropriate permissions to book entries

**Test Steps**:
1. Identify missing income transaction: $25,000.00
2. Create remediating journal entry in Investran
3. Select fund: AP WINDSOR CO-INVEST, L.P.
4. Select account: 10010-Cash-Custody (USD)
5. Enter credit amount: $25,000.00
6. Select appropriate income account for debit
7. Enter transaction date: 09/20/2025
8. Enter description: "Remediating entry for missing income transaction"
9. Post the entry to Investran
10. Verify entry is posted successfully

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account: 10010-Cash-Custody (USD)
- Transaction Date: 09/20/2025
- Amount: $25,000.00
- Transaction Type: Income
- Debit: [Appropriate Income Account] $25,000.00
- Credit: 10010-Cash-Custody (USD) $25,000.00

**Expected Results**:
- Journal entry created successfully
- Entry posted to Investran
- Entry reflects in trial balance
- Test passes

**Priority**: High
**Category**: Remediation Workflow

---

### TC-016: Verify Break Resolved After Booking Entry
**Objective**: Verify that after booking a remediating entry, the break is resolved and balances match.

**Prerequisites**:
- Remediating entry booked in Investran (from TC-014 or TC-015)
- Updated NAV Pack available
- Bank statement available

**Test Steps**:
1. Book remediating entry for missing transaction (from TC-014 or TC-015)
2. Wait for Investran to process the entry
3. Generate updated trial balance from Investran
4. Process updated NAV Pack
5. Compare updated NAV Pack ending balance with bank statement balance
6. Verify balances now match

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Original Bank Statement Balance: $941,754.36
- Original NAV Pack Ending Balance: $881,517.36
- Original Discrepancy: $60,237.00
- Remediating Entry: $60,237.00 expense
- Updated NAV Pack Ending Balance: $941,754.36
- Updated Bank Statement Balance: $941,754.36

**Expected Results**:
- Remediating entry reflected in updated NAV Pack
- Updated NAV Pack balance matches bank statement balance
- Discrepancy resolved: $0.00
- Break successfully resolved
- Test passes

**Priority**: High
**Category**: Remediation Workflow

---

## 4a. Quarterly Data Consistency Test Cases

### TC-017: Validate Q1 Position Report Matches Q1 NAV Pack Data
**Objective**: Verify that Q1 position report data is only compared against Q1 NAV Pack data.

**Prerequisites**:
- Position report data available
- Q1 2025 position report
- Q1 2025 NAV Pack

**Test Steps**:
1. Position report for Q1 2025 (as of 03/31/2025) is processed by workflow tool
2. Verify report date is 03/31/2025
3. Q1 2025 NAV Pack (03.31.2025) is processed by workflow tool
4. Extract cash balance from Q1 position report
5. Extract ending balance from Q1 NAV Pack
6. Compare Q1 position report balance with Q1 NAV Pack balance
7. Verify system rejects comparison with Q2, Q3, or Q4 NAV Pack

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Q1 2025 Position Report Date: 03/31/2025
- Q1 2025 NAV Pack Date: 03.31.2025
- Q1 Position Report Balance: $850,000.00
- Q1 NAV Pack Ending Balance: $850,000.00

**Expected Results**:
- Q1 position report matches Q1 NAV Pack
- System validates quarter consistency
- System rejects comparison with non-Q1 NAV Pack
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-018: Validate Q2 Position Report Matches Q2 NAV Pack Data
**Objective**: Verify that Q2 position report data is only compared against Q2 NAV Pack data.

**Prerequisites**:
- Position report data available
- Q2 2025 position report
- Q2 2025 NAV Pack

**Test Steps**:
1. Position report for Q2 2025 (as of 06/30/2025) is processed by workflow tool
2. Verify report date is 06/30/2025
3. Q2 2025 NAV Pack (06.30.2025) is processed by workflow tool
4. Extract cash balance from Q2 position report
5. Extract ending balance from Q2 NAV Pack
6. Compare Q2 position report balance with Q2 NAV Pack balance
7. Verify system rejects comparison with Q1, Q3, or Q4 NAV Pack

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Q2 2025 Position Report Date: 06/30/2025
- Q2 2025 NAV Pack Date: 06.30.2025
- Q2 Position Report Balance: $865,000.00
- Q2 NAV Pack Ending Balance: $865,000.00

**Expected Results**:
- Q2 position report matches Q2 NAV Pack
- System validates quarter consistency
- System rejects comparison with non-Q2 NAV Pack
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-019: Validate Q3 Position Report Matches Q3 NAV Pack Data
**Objective**: Verify that Q3 position report data is only compared against Q3 NAV Pack data.

**Prerequisites**:
- Position report data available
- Q3 2025 position report
- Q3 2025 NAV Pack

**Test Steps**:
1. Position report for Q3 2025 (as of 09/30/2025) is processed by workflow tool
2. Verify report date is 09/30/2025
3. Q3 2025 NAV Pack (09.30.2025) is processed by workflow tool
4. Extract cash balance from Q3 position report
5. Extract ending balance from Q3 NAV Pack
6. Compare Q3 position report balance with Q3 NAV Pack balance
7. Verify system rejects comparison with Q1, Q2, or Q4 NAV Pack

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Q3 2025 Position Report Date: 09/30/2025
- Q3 2025 NAV Pack Date: 09.30.2025
- Q3 Position Report Balance: $881,517.36
- Q3 NAV Pack Ending Balance: $881,517.36

**Expected Results**:
- Q3 position report matches Q3 NAV Pack
- System validates quarter consistency
- System rejects comparison with non-Q3 NAV Pack
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-020: Validate Q4 Position Report Matches Q4 NAV Pack Data
**Objective**: Verify that Q4 position report data is only compared against Q4 NAV Pack data.

**Prerequisites**:
- Position report data available
- Q4 2025 position report
- Q4 2025 NAV Pack

**Test Steps**:
1. Position report for Q4 2025 (as of 12/31/2025) is processed by workflow tool
2. Verify report date is 12/31/2025
3. Q4 2025 NAV Pack (12.31.2025) is processed by workflow tool
4. Extract cash balance from Q4 position report
5. Extract ending balance from Q4 NAV Pack
6. Compare Q4 position report balance with Q4 NAV Pack balance
7. Verify system rejects comparison with Q1, Q2, or Q3 NAV Pack

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Q4 2025 Position Report Date: 12/31/2025
- Q4 2025 NAV Pack Date: 12.31.2025
- Q4 Position Report Balance: $900,000.00
- Q4 NAV Pack Ending Balance: $900,000.00

**Expected Results**:
- Q4 position report matches Q4 NAV Pack
- System validates quarter consistency
- System rejects comparison with non-Q4 NAV Pack
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-021: Validate Quarter-End Date Matches Position Report Date
**Objective**: Verify that quarter-end dates are correctly validated (Q1: 3/31, Q2: 6/30, Q3: 9/30, Q4: 12/31).

**Prerequisites**:
- Position report data available
- Position reports for all quarters

**Test Steps**:
1. Position report for Q1 2025 is processed by workflow tool
2. Verify report date is 03/31/2025
3. Position report for Q2 2025 is processed by workflow tool
4. Verify report date is 06/30/2025
5. Position report for Q3 2025 is processed by workflow tool
6. Verify report date is 09/30/2025
7. Position report for Q4 2025 is processed by workflow tool
8. Verify report date is 12/31/2025
9. Verify system rejects position reports with incorrect quarter-end dates

**Test Data**:
- Q1 2025 Expected Date: 03/31/2025
- Q2 2025 Expected Date: 06/30/2025
- Q3 2025 Expected Date: 09/30/2025
- Q4 2025 Expected Date: 12/31/2025

**Expected Results**:
- All quarter-end dates validated correctly
- System accepts correct quarter-end dates
- System rejects incorrect quarter-end dates
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-022: Validate Transaction Data Matches Selected Quarter Period
**Objective**: Verify that transaction data is validated to ensure it falls within the selected quarter period.

**Prerequisites**:
- Transaction report data for Q3 2025
- Daily cash file data for Q3 2025

**Test Steps**:
1. Select quarter: Q3 2025 (07/01/2025 - 09/30/2025)
2. Transaction report for Q3 2025 is processed by workflow tool
3. Verify all transactions fall within 07/01/2025 - 09/30/2025
4. Daily cash file for Q3 2025 is processed by workflow tool
5. Verify all transactions in daily cash file fall within Q3 2025 period
6. Flag any transactions outside Q3 2025 period

**Test Data**:
- Quarter: Q3 2025
- Quarter Period: 07/01/2025 - 09/30/2025
- Valid Transaction Dates: 07/01/2025 through 09/30/2025
- Invalid Transaction Date: 06/30/2025 (Q2) - should be flagged
- Invalid Transaction Date: 10/01/2025 (Q4) - should be flagged

**Expected Results**:
- All Q3 transactions validated within quarter period
- Transactions outside Q3 period flagged
- System enforces quarter consistency
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-023: Validate Daily Cash File Transactions Are Within Selected Quarter
**Objective**: Verify that daily cash file transactions are validated to ensure they fall within the selected quarter.

**Prerequisites**:
- Daily cash file data for Q3 2025

**Test Steps**:
1. Select quarter: Q3 2025
2. Daily cash file for Q3 2025 is processed by workflow tool
3. Review all transaction dates in daily cash file
4. Verify all transactions fall within Q3 2025 (07/01/2025 - 09/30/2025)
5. Flag any transactions outside Q3 2025 period

**Test Data**:
- Quarter: Q3 2025
- Quarter Period: 07/01/2025 - 09/30/2025
- Daily Cash File Transactions:
  - 07/15/2025: $10,000.00 (Valid)
  - 08/20/2025: $15,000.00 (Valid)
  - 09/25/2025: $20,000.00 (Valid)
  - 06/30/2025: $5,000.00 (Invalid - Q2)
  - 10/01/2025: $3,000.00 (Invalid - Q4)

**Expected Results**:
- Valid Q3 transactions accepted
- Invalid transactions (outside Q3) flagged
- System enforces quarter consistency
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-024: Reject Position Report from Different Quarter Than NAV Pack
**Objective**: Verify that the system rejects attempts to compare position reports and NAV Packs from different quarters.

**Prerequisites**:
- Q2 2025 position report
- Q3 2025 NAV Pack

**Test Steps**:
1. Q2 2025 position report (06/30/2025) is processed by workflow tool
2. Attempt to process Q3 2025 NAV Pack (09.30.2025)
3. Attempt to compare Q2 position report with Q3 NAV Pack
4. Verify system rejects the comparison
5. Verify error message indicates quarter mismatch

**Test Data**:
- Position Report Quarter: Q2 2025 (06/30/2025)
- NAV Pack Quarter: Q3 2025 (09.30.2025)
- Quarter Mismatch: Yes

**Expected Results**:
- System rejects comparison
- Error message: "Quarter mismatch: Position report is Q2 2025, NAV Pack is Q3 2025"
- Comparison blocked
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-025: Reject Transaction Data from Different Quarter Than Position Report
**Objective**: Verify that the system rejects attempts to use transaction data from a different quarter than the position report.

**Prerequisites**:
- Q3 2025 position report
- Q2 2025 transaction report

**Test Steps**:
1. Q3 2025 position report (09/30/2025) is processed by workflow tool
2. Attempt to use Q2 2025 transaction report (06/30/2025)
3. Attempt to reconcile using Q2 transaction data with Q3 position report
4. Verify system rejects the reconciliation
5. Verify error message indicates quarter mismatch

**Test Data**:
- Position Report Quarter: Q3 2025 (09/30/2025)
- Transaction Report Quarter: Q2 2025 (06/30/2025)
- Quarter Mismatch: Yes

**Expected Results**:
- System rejects reconciliation
- Error message: "Quarter mismatch: Position report is Q3 2025, Transaction report is Q2 2025"
- Reconciliation blocked
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

### TC-026: Validate All Test Data Sources Are from Same Quarter
**Objective**: Verify that all data sources (position report, NAV Pack, transaction report, daily cash file) are validated to ensure they are from the same quarter.

**Prerequisites**:
- Position report, NAV Pack, transaction report, daily cash file for Q3 2025

**Test Steps**:
1. Select quarter: Q3 2025
2. Q3 2025 position report (09/30/2025) is processed by workflow tool
3. Q3 2025 NAV Pack (09.30.2025) is processed by workflow tool
4. Q3 2025 transaction report is processed by workflow tool
5. Q3 2025 daily cash file is processed by workflow tool
6. Verify all data sources are validated as Q3 2025
7. Attempt to mix Q2 data with Q3 data
8. Verify system rejects mixed quarter data

**Test Data**:
- Selected Quarter: Q3 2025
- Position Report: Q3 2025 (09/30/2025) - Valid
- NAV Pack: Q3 2025 (09.30.2025) - Valid
- Transaction Report: Q3 2025 - Valid
- Daily Cash File: Q3 2025 - Valid
- Mixed Data Test: Q2 2025 transaction report with Q3 2025 position report - Invalid

**Expected Results**:
- All Q3 data sources validated as same quarter
- Mixed quarter data rejected
- System enforces quarter consistency across all data sources
- Test passes

**Priority**: High
**Category**: Quarterly Data Consistency

---

## 5. Multiple Bank Account Scenarios

### TC-027: Co-Invest Fund with Multiple Bank Accounts
**Objective**: Verify reconciliation process for a co-invest fund that has multiple bank accounts requiring statements from multiple bank portals.

**Prerequisites**:
- Position report data from multiple bank portals
- Co-invest fund with multiple bank accounts
- NAV Pack data for the fund

**Test Steps**:
1. Identify co-invest fund with multiple bank accounts
2. Position report for Q3 2025 from first bank (e.g., JP Morgan) is processed by workflow tool
3. Extract cash balance from first bank account
4. Position report for Q3 2025 from second bank (if applicable) is processed by workflow tool
5. Extract cash balance from second bank account
6. Sum balances from all bank accounts
7. NAV Pack for Q3 2025 is processed by workflow tool
8. Compare aggregated bank balance with NAV Pack ending balance

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Bank Account 1 (JP Morgan): $500,000.00
- Bank Account 2 (Other Bank): $381,517.36
- Total Bank Balance: $881,517.36
- NAV Pack Ending Balance: $881,517.36

**Expected Results**:
- Multiple bank accounts identified
- Balances extracted from all accounts
- Aggregated balance calculated correctly
- Aggregated balance matches NAV Pack
- Test passes

**Priority**: Medium
**Category**: Multiple Bank Account Scenarios

---

### TC-028: Download Statements from Multiple Bank Portals
**Objective**: Verify that statements can be downloaded from multiple bank portals for the same fund.

**Prerequisites**:
- Position report data from multiple bank portals
- Co-invest fund with accounts at multiple banks

**Test Steps**:
1. Identify fund with multiple bank accounts
2. Position report for Q3 2025 from first bank portal (e.g., JP Morgan) is processed by workflow tool
3. Position report for Q3 2025 from second bank portal for the same fund is processed by workflow tool
4. Verify both reports are processed successfully
5. Verify both reports are for the same quarter (Q3 2025)

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Bank Portal 1: JP Morgan
- Bank Portal 2: [Other Bank]
- Quarter: Q3 2025 (09/30/2025)

**Expected Results**:
- Position reports downloaded from both bank portals
- Both reports are for Q3 2025
- Reports contain data for the same fund
- Test passes

**Priority**: Medium
**Category**: Multiple Bank Account Scenarios

---

### TC-029: Aggregate Balances Across Multiple Accounts (Same Quarter)
**Objective**: Verify that balances from multiple bank accounts are correctly aggregated when all accounts are from the same quarter.

**Prerequisites**:
- Multiple bank account statements for Q3 2025
- NAV Pack data for Q3 2025

**Test Steps**:
1. Position report from Bank 1 for Q3 2025 is processed by workflow tool
2. Extract cash balance: $500,000.00
3. Position report from Bank 2 for Q3 2025 is processed by workflow tool
4. Extract cash balance: $381,517.36
5. Verify both reports are Q3 2025
6. Sum the balances: $500,000.00 + $381,517.36 = $881,517.36
7. Q3 2025 NAV Pack is processed by workflow tool
8. Compare aggregated balance with NAV Pack ending balance

**Test Data**:
- Quarter: Q3 2025 (09/30/2025)
- Bank Account 1 Balance (Q3 2025): $500,000.00
- Bank Account 2 Balance (Q3 2025): $381,517.36
- Aggregated Balance: $881,517.36
- NAV Pack Ending Balance (Q3 2025): $881,517.36

**Expected Results**:
- All accounts validated as Q3 2025
- Balances aggregated correctly
- Aggregated balance matches NAV Pack
- Quarter consistency maintained
- Test passes

**Priority**: High
**Category**: Multiple Bank Account Scenarios

---

## 6. Exception Handling Test Cases

### TC-030: Bank Statement Shows Incorrect Entry
**Objective**: Verify that when a bank statement shows an incorrect entry that the controller is not aware of, the system supports contacting the bank for verification.

**Prerequisites**:
- Position report data with unknown/incorrect entry
- NAV Pack data for Q3 2025
- Transaction report data
- Bank contact information available

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. NAV Pack for Q3 2025 is processed by workflow tool
3. Identify discrepancy
4. Transaction report is processed by workflow tool
5. Identify transaction that controller is not aware of
6. Document the unknown transaction
7. Flag transaction for bank verification
8. Contact bank to verify source/reason for transaction
9. If incorrect, request bank to rectify statement and reverse transaction

**Test Data**:
- Fund: AP WINDSOR CO-INVEST, L.P.
- Account Number: FFK30
- Quarter: Q3 2025 (09/30/2025)
- Unknown Transaction: $10,000.00 debit on 09/20/2025
- Transaction Description: "Unknown transaction - requires bank verification"
- Bank Contact: JP Morgan Relationship Manager

**Expected Results**:
- Unknown transaction identified
- Transaction documented
- Bank contacted for verification
- If incorrect, bank rectifies statement
- Test passes

**Priority**: Medium
**Category**: Exception Handling

---

### TC-031: Contact Bank to Verify Unknown Transaction
**Objective**: Verify the process for contacting the bank to verify an unknown transaction.

**Prerequisites**:
- Unknown transaction identified
- Bank contact information available

**Test Steps**:
1. Identify unknown transaction in bank statement
2. Document transaction details (date, amount, description)
3. Contact bank relationship manager
4. Provide transaction details to bank
5. Request verification of transaction source/reason
6. Document bank's response
7. Take appropriate action based on bank's response

**Test Data**:
- Unknown Transaction Date: 09/20/2025
- Unknown Transaction Amount: $10,000.00
- Unknown Transaction Type: Debit
- Bank Contact: JP Morgan Relationship Manager
- Contact Method: Email/Phone

**Expected Results**:
- Bank contacted successfully
- Transaction details provided to bank
- Bank response received
- Appropriate action taken based on response
- Test passes

**Priority**: Medium
**Category**: Exception Handling

---

### TC-032: Request Bank to Reverse Incorrect Transaction
**Objective**: Verify the process for requesting the bank to reverse an incorrect transaction.

**Prerequisites**:
- Incorrect transaction identified
- Bank has confirmed transaction is incorrect
- Bank contact information available

**Test Steps**:
1. Identify incorrect transaction
2. Contact bank to verify transaction
3. Bank confirms transaction is incorrect
4. Request bank to reverse the transaction
5. Bank processes reversal
6. Verify reversal appears in next bank statement
7. Update reconciliation accordingly

**Test Data**:
- Incorrect Transaction Date: 09/20/2025
- Incorrect Transaction Amount: $10,000.00
- Bank Confirmation: Transaction is incorrect
- Reversal Request Date: 09/25/2025
- Reversal Processed Date: 09/26/2025

**Expected Results**:
- Bank confirms transaction is incorrect
- Reversal requested
- Bank processes reversal
- Reversal appears in bank statement
- Reconciliation updated
- Test passes

**Priority**: Medium
**Category**: Exception Handling

---

### TC-033: Bank Statement Correction Process
**Objective**: Verify the complete process for handling bank statement corrections.

**Prerequisites**:
- Incorrect bank statement entry
- Bank relationship established

**Test Steps**:
1. Identify incorrect entry in bank statement
2. Document the incorrect entry
3. Contact bank to report incorrect entry
4. Bank investigates and confirms error
5. Bank issues corrected statement
6. Process corrected statement
7. Re-run reconciliation with corrected statement
8. Verify reconciliation now matches

**Test Data**:
- Original Incorrect Entry: $10,000.00 debit
- Corrected Entry: $0.00 (reversed)
- Correction Date: 09/26/2025
- Corrected Statement Date: 09/30/2025

**Expected Results**:
- Incorrect entry identified and documented
- Bank issues correction
- Corrected statement received
- Reconciliation updated with corrected data
- Balances now match
- Test passes

**Priority**: Medium
**Category**: Exception Handling

---

## 7. Data Validation Test Cases

### TC-034: Validate Position Report Date Matches Quarter End
**Objective**: Verify that position report date is validated to ensure it matches the expected quarter-end date.

**Prerequisites**:
- Position report for Q3 2025

**Test Steps**:
1. Position report is processed by workflow tool
2. Extract report date from position report
3. Verify report date is 09/30/2025 (Q3 2025 quarter-end)
4. Verify system accepts correct quarter-end date
5. Verify system rejects position report with incorrect date (e.g., 09/29/2025)

**Test Data**:
- Selected Quarter: Q3 2025
- Expected Quarter-End Date: 09/30/2025
- Position Report Date: 09/30/2025 (Valid)
- Invalid Date Test: 09/29/2025 (Should be rejected)

**Expected Results**:
- Correct quarter-end date accepted
- Incorrect date rejected
- Validation error message displayed for invalid date
- Test passes

**Priority**: High
**Category**: Data Validation

---

### TC-035: Validate Fund Name Matches Between Position Report and NAV Pack
**Objective**: Verify that fund name in position report matches fund name in NAV Pack.

**Prerequisites**:
- Position report for Q3 2025
- NAV Pack data for Q3 2025

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. Extract fund name from position report: "AP WINDSOR CO-INVEST, L.P."
3. NAV Pack for Q3 2025 is processed by workflow tool
4. Extract fund name from NAV Pack: "AP Windsor Co-Invest L.P."
5. Compare fund names (case-insensitive)
6. Verify system accepts matching fund names
7. Verify system rejects non-matching fund names

**Test Data**:
- Position Report Fund Name: "AP WINDSOR CO-INVEST, L.P."
- NAV Pack Fund Name: "AP Windsor Co-Invest L.P."
- Match: Yes (case-insensitive)

**Expected Results**:
- Matching fund names accepted (case-insensitive)
- Non-matching fund names rejected
- Validation error for mismatched names
- Test passes

**Priority**: High
**Category**: Data Validation

---

### TC-036: Validate Cash Account Currency Code (USD)
**Objective**: Verify that cash account currency code is validated to ensure it is USD for account 10010.

**Prerequisites**:
- Position report with cash accounts

**Test Steps**:
1. Position report is processed by workflow tool
2. Search for account 10010-Cash-Custody
3. Extract currency code for account 10010
4. Verify currency code is "USD"
5. Verify system accepts USD currency code
6. Verify system rejects non-USD currency codes for account 10010

**Test Data**:
- Account: 10010-Cash-Custody
- Expected Currency Code: USD
- Position Report Currency Code: USD (Valid)
- Invalid Currency Test: EUR (Should be rejected for account 10010)

**Expected Results**:
- USD currency code accepted
- Non-USD currency codes rejected for account 10010
- Validation error for incorrect currency
- Test passes

**Priority**: High
**Category**: Data Validation

---

### TC-037: Validate Account Number Format
**Objective**: Verify that account numbers are validated for correct format.

**Prerequisites**:
- Position report with account numbers

**Test Steps**:
1. Position report is processed by workflow tool
2. Extract account numbers from position report
3. Verify account number format (e.g., FFK30, FFF70, P 13961)
4. Verify system accepts valid account number formats
5. Verify system rejects invalid account number formats

**Test Data**:
- Valid Account Numbers: FFK30, FFF70, P 13961, S 18088
- Invalid Account Number Format: "INVALID123" (Should be rejected)

**Expected Results**:
- Valid account number formats accepted
- Invalid formats rejected
- Validation error for invalid format
- Test passes

**Priority**: Medium
**Category**: Data Validation

---

### TC-038: Validate Quarterly Period Selection (Q1, Q2, Q3, Q4)
**Objective**: Verify that quarterly period selection is validated to ensure only valid quarters (Q1, Q2, Q3, Q4) are accepted.

**Test Steps**:
1. Attempt to select Q1
2. Verify Q1 is accepted
3. Attempt to select Q2
4. Verify Q2 is accepted
5. Attempt to select Q3
6. Verify Q3 is accepted
7. Attempt to select Q4
8. Verify Q4 is accepted
9. Attempt to select invalid quarter (e.g., Q5)
10. Verify invalid quarter is rejected

**Test Data**:
- Valid Quarters: Q1, Q2, Q3, Q4
- Invalid Quarter: Q5 (Should be rejected)

**Expected Results**:
- Valid quarters (Q1-Q4) accepted
- Invalid quarters rejected
- Validation error for invalid quarter
- Test passes

**Priority**: High
**Category**: Data Validation

---

### TC-039: Validate Year Selection for Quarterly Reports
**Objective**: Verify that year selection is validated for quarterly reports.

**Test Steps**:
1. Select quarter: Q3
2. Attempt to select year: 2025
3. Verify 2025 is accepted
4. Attempt to select future year: 2030
5. Verify future year is rejected or requires confirmation
6. Attempt to select past year: 2020
7. Verify past year is accepted (if historical data is allowed)

**Test Data**:
- Valid Year: 2025
- Future Year: 2030 (May be rejected or require confirmation)
- Past Year: 2020 (May be accepted for historical data)

**Expected Results**:
- Valid years accepted
- Future years handled appropriately (rejected or confirmed)
- Past years handled appropriately
- Test passes

**Priority**: Medium
**Category**: Data Validation

---

### TC-040: Validate Quarter Consistency Across All Data Sources
**Objective**: Verify that quarter consistency is validated across all data sources (position report, NAV Pack, transaction report, daily cash file).

**Test Steps**:
1. Select quarter: Q3 2025
2. Q3 2025 position report is processed by workflow tool
3. Q3 2025 NAV Pack is processed by workflow tool
4. Q3 2025 transaction report is processed by workflow tool
5. Q3 2025 daily cash file is processed by workflow tool
6. Verify all data sources are validated as Q3 2025
7. Attempt to mix Q2 data with Q3 data
8. Verify system rejects mixed quarter data

**Test Data**:
- Selected Quarter: Q3 2025
- Position Report: Q3 2025 (Valid)
- NAV Pack: Q3 2025 (Valid)
- Transaction Report: Q3 2025 (Valid)
- Daily Cash File: Q3 2025 (Valid)
- Mixed Data: Q2 2025 transaction report with Q3 2025 position report (Invalid)

**Expected Results**:
- All Q3 data sources validated
- Mixed quarter data rejected
- Validation error for quarter mismatch
- Test passes

**Priority**: High
**Category**: Data Validation

---

## 8. Edge Cases

### TC-041: Zero Balance Reconciliation
**Objective**: Verify that reconciliation process works correctly when cash balance is zero.

**Prerequisites**:
- Fund with zero cash balance
- Position report showing zero balance
- NAV Pack showing zero balance

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. Identify fund with zero cash balance
3. Extract cash balance: $0.00
4. NAV Pack for Q3 2025 is processed by workflow tool
5. Extract ending balance: $0.00
6. Compare balances: $0.00 vs $0.00
7. Verify reconciliation passes

**Test Data**:
- Fund: [Fund with zero balance]
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $0.00
- NAV Pack Ending Balance: $0.00

**Expected Results**:
- Zero balances handled correctly
- Reconciliation passes with zero balance
- No errors or exceptions
- Test passes

**Priority**: Low
**Category**: Edge Cases

---

### TC-042: Very Large Balance Amounts
**Objective**: Verify that reconciliation process works correctly with very large balance amounts.

**Prerequisites**:
- Fund with very large cash balance
- Position report with large balance
- NAV Pack with large balance

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. Identify fund with large balance (e.g., MIDCAP FINANCIAL INVESTMENT CORPORATION)
3. Extract cash balance: $42,655,137.23
4. NAV Pack for Q3 2025 is processed by workflow tool
5. Extract ending balance: $42,655,137.23
6. Compare large balances
7. Verify reconciliation handles large numbers correctly

**Test Data**:
- Fund: MIDCAP FINANCIAL INVESTMENT CORPORATION
- Account Number: 32926 (P 85967)
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: $42,655,137.23
- NAV Pack Ending Balance: $42,655,137.23

**Expected Results**:
- Large balances handled correctly
- No precision errors
- Reconciliation passes
- Test passes

**Priority**: Medium
**Category**: Edge Cases

---

### TC-043: Negative Cash Balance (Overdraft Scenario)
**Objective**: Verify that reconciliation process works correctly when cash balance is negative (overdraft).

**Prerequisites**:
- Fund with negative cash balance
- Position report showing negative balance
- NAV Pack showing negative balance

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. Identify fund with negative balance
3. Extract cash balance: -$5,000.00
4. NAV Pack for Q3 2025 is processed by workflow tool
5. Extract ending balance: -$5,000.00
6. Compare negative balances
7. Verify reconciliation handles negative numbers correctly

**Test Data**:
- Fund: [Fund with overdraft]
- Quarter: Q3 2025 (09/30/2025)
- Bank Statement Balance: -$5,000.00
- NAV Pack Ending Balance: -$5,000.00

**Expected Results**:
- Negative balances handled correctly
- Reconciliation passes with negative balance
- No errors or exceptions
- Test passes

**Priority**: Low
**Category**: Edge Cases

---

### TC-044: Position Report Not Available for Quarter
**Objective**: Verify that the system handles the scenario when position report is not available for a selected quarter.

**Test Steps**:
1. Select quarter: Q3 2025
2. Attempt to process position report for Q3 2025
3. Verify position report is not available
4. Verify appropriate error message is displayed
5. Verify system allows selection of alternative quarter or manual entry (if applicable)

**Test Data**:
- Selected Quarter: Q3 2025
- Position Report Availability: Not Available
- Error Message: "Position report not available for Q3 2025"

**Expected Results**:
- System handles missing position report gracefully
- Appropriate error message displayed
- Alternative options provided (if applicable)
- Test passes

**Priority**: Medium
**Category**: Edge Cases

---

### TC-045: Fund Not Found in Position Report
**Objective**: Verify that the system handles the scenario when a fund is not found in the position report.

**Test Steps**:
1. Position report for Q3 2025 is processed by workflow tool
2. Search for fund: "NON-EXISTENT FUND, L.P."
3. Verify fund is not found in position report
4. Verify appropriate error message is displayed
5. Verify system allows manual entry or fund selection (if applicable)

**Test Data**:
- Fund Name: "NON-EXISTENT FUND, L.P."
- Position Report: Q3 2025
- Fund Found: No
- Error Message: "Fund not found in position report"

**Expected Results**:
- System handles missing fund gracefully
- Appropriate error message displayed
- Alternative options provided (if applicable)
- Test passes

**Priority**: Medium
**Category**: Edge Cases

---

### TC-046: Quarter-End Falls on Weekend/Holiday
**Objective**: Verify that the system handles quarter-end dates that fall on weekends or holidays correctly.

**Test Steps**:
1. Identify quarter where quarter-end falls on weekend (e.g., Q4 2024: 12/31/2024 is a Tuesday, but test with weekend scenario)
2. Position report for quarter-end date is processed by workflow tool
3. Verify position report date is adjusted if necessary (e.g., to last business day)
4. Verify NAV Pack date matches adjusted date
5. Verify reconciliation works correctly

**Test Data**:
- Quarter: Q4 2024
- Quarter-End Date: 12/31/2024 (Tuesday - not weekend, but test scenario)
- Adjusted Date (if weekend): Last business day before weekend
- Position Report Date: Adjusted date (if applicable)
- NAV Pack Date: Adjusted date (if applicable)

**Expected Results**:
- Weekend/holiday quarter-end handled correctly
- Dates adjusted appropriately (if applicable)
- Reconciliation works correctly
- Test passes

**Priority**: Low
**Category**: Edge Cases

---

### TC-047: Missing Quarterly Data for Selected Period
**Objective**: Verify that the system handles the scenario when quarterly data is missing for the selected period.

**Test Steps**:
1. Select quarter: Q3 2025
2. Attempt to process NAV Pack for Q3 2025
3. Verify NAV Pack is not available
4. Verify appropriate error message is displayed
5. Verify system allows selection of alternative quarter or data entry (if applicable)

**Test Data**:
- Selected Quarter: Q3 2025
- NAV Pack Availability: Not Available
- Error Message: "NAV Pack not available for Q3 2025"

**Expected Results**:
- System handles missing quarterly data gracefully
- Appropriate error message displayed
- Alternative options provided (if applicable)
- Test passes

**Priority**: Medium
**Category**: Edge Cases

---

### TC-048: Mismatched Quarter Data Across Sources (Error Case)
**Objective**: Verify that the system correctly identifies and rejects mismatched quarter data across different sources.

**Test Steps**:
1. Select quarter: Q3 2025
2. Q3 2025 position report is processed by workflow tool
3. Attempt to use Q2 2025 NAV Pack
4. Verify system detects quarter mismatch
5. Verify system rejects the reconciliation
6. Verify appropriate error message is displayed

**Test Data**:
- Selected Quarter: Q3 2025
- Position Report Quarter: Q3 2025 (Valid)
- NAV Pack Quarter: Q2 2025 (Invalid - Mismatch)
- Error Message: "Quarter mismatch detected: Position report is Q3 2025, NAV Pack is Q2 2025"

**Expected Results**:
- Quarter mismatch detected
- Reconciliation rejected
- Appropriate error message displayed
- User prompted to correct quarter mismatch
- Test passes

**Priority**: High
**Category**: Edge Cases

---

## Test Case Summary

**Total Test Cases**: 49
- Happy Path: 4 test cases
- Mismatch Detection: 5 test cases
- Valid Break Scenarios: 4 test cases (including TC-010A for cut-off time validation)
- Remediation Workflow: 4 test cases
- Quarterly Data Consistency: 10 test cases
- Multiple Bank Account Scenarios: 3 test cases
- Exception Handling: 4 test cases
- Data Validation: 7 test cases
- Edge Cases: 8 test cases

**Priority Distribution**:
- High Priority: 29 test cases
- Medium Priority: 16 test cases
- Low Priority: 4 test cases

