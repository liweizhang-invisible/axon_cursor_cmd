# Cash Custody MVP - Open Questions

**Date:** 2024-12-22
**Status:** Pending Clarification

---

## Critical for MVP Build

### Q1: File Formats

**Question:** Can we assume Position Report is always PDF and NAV Pack is always .xlsm/.xlsx?

**Context:** The workflow needs to know which parsing approach to use. If formats vary, we need conditional logic or format detection.

**Options:**
- [ ] A) Yes, formats are consistent
- [ ] B) Position Report can be PDF or Excel
- [ ] C) Formats vary by fund/bank

**Impact:** Affects document extraction team design

---

### Q2: Fund Identification in Position Report

**Question:** Is the fund name in the position report always searchable text, or could it be in an image/scanned document?

**Context:** From the sample (image1.png), the JP Morgan report appears to have searchable text. If some reports are scanned images, we'd need OCR capabilities.

**Options:**
- [ ] A) Always searchable text (native PDF)
- [ ] B) Sometimes scanned/image-based
- [ ] C) Varies by bank

**Impact:** Determines if OCR tools are needed for MVP

---

### Q3: NAV Pack Structure Consistency

**Question:** Is account 10010 (Cash - Chase Custody USD) always in a consistent location in the NAV Pack, or does it vary by fund?

**Context:** From the sample (image3.png), account 10010 appears in row 3 with specific columns (Opening Balance, Debit, Credit, Ending Balance). Need to confirm if this structure is consistent.

**Specific sub-questions:**
- Is the sheet name always the same?
- Is the account always identified by "10010" code?
- Are column headers consistent?

**Options:**
- [ ] A) Structure is consistent across all funds
- [ ] B) Sheet name varies but column structure is same
- [ ] C) Structure varies significantly by fund

**Impact:** Determines extraction approach - fixed location vs. search-based

---

## Important for MVP (Can Work Around)

### Q4: Multiple Bank Accounts

**Question:** For MVP, can we assume single bank account per fund, or do we need to handle multi-bank scenarios?

**Context:** Source document notes "Some coinvest funds may have multiple bank accounts requiring statement to be downloaded from more than one bank portal."

**Options:**
- [ ] A) MVP can assume single bank account
- [ ] B) Must support multiple accounts in MVP

**Impact:** If multi-bank needed, requires aggregation logic

---

### Q5: Transaction Report Format

**Question:** What is the format of the transaction report used for break investigation?

**Context:** Referenced as "All Transaction Activity - Windsor.pdf" but we haven't seen the structure.

**Specific sub-questions:**
- Is it always PDF?
- What columns/fields does it contain?
- Is it searchable text or scanned?

**Impact:** Affects break analysis team design

---

### Q6: Daily Cash File Structure

**Question:** What are the exact columns in the daily cash file?

**Context:** From image4.png, visible columns include: Date, Account, Transaction Type, Sub-Transaction Type, Investment/Deal, Strategy, Currency, Cash Flow, Balance. Need to confirm if these are standard.

**Impact:** Affects transaction matching logic

---

## Nice to Know (Future Enhancements)

### Q7: Tolerance Threshold

**Question:** Is there a materiality threshold for breaks?

**Context:** Should small differences (e.g., < $1 or < $100) be ignored?

**Current MVP approach:** Flag any variance

---

### Q8: Cut-off Time

**Question:** What is the daily cut-off time for valid timing breaks?

**Context:** Document mentions transactions after cut-off appear in next day's statement, creating "valid breaks."

**Current MVP approach:** Root cause analyst will identify timing differences manually

---

### Q9: Approval Workflow

**Question:** Is there a maker-checker or approval process for booking remediation entries?

**Context:** Not captured in current process documentation.

**Current MVP approach:** Generate recommendations only; human reviews and books entries

---

### Q10: IVP Recon Timeline

**Question:** What is the exact scope of IVP Recon (Feb 2026) and will it affect this workflow?

**Context:** Document notes "IVP Recon may replace the BAU process of preparing daily cash file."

**Impact:** May affect future state design

---

## Questions from Process Documentation Gaps

These were identified during the initial process analysis:

| # | Area | Question |
|---|------|----------|
| 11 | Access | How are bank portal credentials managed? (Not relevant for MVP - human uploads) |
| 12 | Multi-bank | What other banks besides JP Morgan are used? |
| 13 | Daily Cash File | Where is the daily cash file stored? |
| 14 | Investran | What are all valid transaction types beyond those shown? |
| 15 | Investran | What are the contra accounts used for each transaction type? |
| 16 | Exception | What is the escalation path if a break cannot be resolved? |
| 17 | Bank Contact | Who at the bank should be contacted for incorrect entries? |
| 18 | Compliance | How should breaks and resolutions be documented for audit? |
| 19 | Controls | Are there SOD controls between who downloads and who books? |
| 20 | Retention | How long are position reports and daily cash files retained? |

---

## Daily Cash File Automation Questions

### Q21: Daily Cash File - Transaction Report Mapping

**Question:** Do all fields in the Daily Cash File have a direct mapping to fields in the Bank Transaction Report?

**Context:** From image4.png, Daily Cash File columns include: Date, Account, Transaction Type, Sub-Transaction Type, Investment/Deal, Strategy, Currency, Cash Flow, Balance. Need to confirm if all of these can be derived from the transaction report or if some are manually added by controllers.

**Options:**
- [ ] A) All fields are directly extractable from transaction report
- [ ] B) Some fields require controller input/lookup (e.g., Strategy, Investment/Deal)
- [ ] C) Mapping varies by fund

**Impact:** Determines if full automation is possible or if some fields need human input

---

### Q22: Daily Cash File - Historical Value

**Question:** If we automate Daily Cash File generation, do controllers still need historical Daily Cash Files for other purposes?

**Context:** The Daily Cash File is used for:
1. Daily transaction booking to Investran
2. Break investigation during quarterly reconciliation

If we can generate it on-demand from transaction reports, historical files may not be needed.

**Options:**
- [ ] A) Historical files needed for audit/compliance
- [ ] B) Historical files needed for other reporting
- [ ] C) No need if we can regenerate from transaction reports

**Impact:** Determines if we need to store generated files or generate on-demand

---

### Q23: Daily Cash File - Frequency vs. Quarterly Reconciliation

**Question:** For the quarterly NAV Pack reconciliation, is a cumulative transaction report (full quarter) available, or must we aggregate daily reports?

**Context:** The daily process downloads one day's transactions. For Workflow 2 (break investigation), we need the full period's transactions. Need to confirm if JP Morgan provides quarterly transaction reports.

**Options:**
- [ ] A) Quarterly/period transaction report is available
- [ ] B) Must aggregate daily transaction reports
- [ ] C) Both options available

**Impact:** Affects whether Workflow 2 can work with a single file or needs aggregation logic

---

## Response Tracking

| Question | Answered | Answer | Date |
|----------|----------|--------|------|
| Q1 | [ ] | | |
| Q2 | [ ] | | |
| Q3 | [ ] | | |
| Q4 | [ ] | | |
| Q5 | [ ] | | |
| Q6 | [ ] | | |
| Q7 | [ ] | | |
| Q8 | [ ] | | |
| Q9 | [ ] | | |
| Q10 | [ ] | | |
| Q21 | [ ] | | |
| Q22 | [ ] | | |
| Q23 | [ ] | | |
