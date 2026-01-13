# Cash Custody MVP Architecture

## Axon Workflows for Quarterly Cash Custody Reconciliation

**Version:** 1.1 (MVP/POC)
**Date:** 2024-12-22
**Account:** 10010 - Cash - Chase Custody (USD)

---

## Design Principles

1. **No direct external system integration** — All external data (bank portal, Investran) is gathered by humans and uploaded to the workflow
2. **Two independent workflows** — Eliminates mid-workflow human input (not supported in Axon); each workflow is independently invokable and testable
3. **Delegates for deterministic code** — Calculations, comparisons, and report formatting
4. **Agentic Teams for reasoning** — Document parsing, analysis, root cause determination
5. **MVP focus** — Minimal friction, prove the concept works

---

## Architecture Overview

The cash custody reconciliation is split into **two independently invokable workflows**:

| Workflow | Name | Purpose | When to Run |
|----------|------|---------|-------------|
| **1** | Initial Check (Matching) | Extract balances, compare, detect mismatch | Every quarter for each fund |
| **2** | Mismatch Analysis | Investigate break, identify root cause, recommend remediation | Only when Workflow 1 reports a mismatch |

### Why Two Workflows?

- **No mid-workflow HITL** — Axon doesn't support human input during workflow execution
- **Independent invocation** — User can run Workflow 2 directly if they already know there's a mismatch
- **Simpler testing** — Each workflow can be tested in isolation
- **Clear handoff** — Workflow 1 outputs inform whether Workflow 2 is needed

---

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  WORKFLOW 1: INITIAL CHECK (MATCHING)                               │
├─────────────────────────────────────────────────────────────────────┤
│  [User Upload] → Position Report (PDF) + NAV Pack (Excel)           │
│        ↓                                                            │
│  [Team] Extract cash balance from Position Report                   │
│        ↓                                                            │
│  [Team] Extract trial balance from NAV Pack                         │
│        ↓                                                            │
│  [Delegate] Compare balances                                        │
│        ↓                                                            │
│  [Delegate] Generate result report                                  │
│        ↓                                                            │
│  MATCH → Done                                                       │
│  MISMATCH → Output: "Run Workflow 2 for analysis"                   │
└─────────────────────────────────────────────────────────────────────┘

        User gathers additional files, then runs Workflow 2
                              ↓

┌─────────────────────────────────────────────────────────────────────┐
│  WORKFLOW 2: MISMATCH ANALYSIS                                      │
├─────────────────────────────────────────────────────────────────────┤
│  [User Upload] → Transaction Report (PDF) + Daily Cash File (Excel) │
│        ↓                                                            │
│  [Team] Analyze transactions & identify root cause                  │
│        ↓                                                            │
│  [Delegate] Generate analysis report                                │
│        ↓                                                            │
│  Output: Remediation recommendations for Investran                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow 1: Initial Check (Matching)

### Input Variables

| Variable | Type | Description |
|----------|------|-------------|
| `position_report` | File | Bank position report PDF from JP Morgan portal |
| `nav_pack` | File | NAV Pack Excel workbook (.xlsm/.xlsx) |
| `fund_name` | String | Fund to reconcile (e.g., "AP Windsor Co-Invest, L.P.") |
| `quarter_end_date` | String | Quarter end date (e.g., "2025-09-30") |

### Output Variables

| Variable | Type | Description |
|----------|------|-------------|
| `reconciliation_status` | String | Human-readable status message |
| `is_matched` | Boolean | True if balances match |
| `variance_amount` | Float | Difference (bank - NAV Pack) |
| `bank_cash_balance` | Float | Extracted bank balance |
| `nav_pack_balance` | Float | Extracted NAV Pack balance |
| `initial_check_report` | File | Summary report |

---

### Step 1: Position Report Extraction (Team)

**Purpose:** Parse the bank position report PDF and extract the cash balance for the specified fund.

**Type:** Team (Agentic)

**Rationale:** PDF parsing requires document understanding - searching for fund name within multi-fund reports, interpreting table layouts, handling varying formats.

**Agents:**
- `speaker_selector` — Coordinates extraction workflow
- `document_reader` — Reads and parses PDF content
- `data_extractor` — Locates fund and extracts cash balance
- `validator` — Confirms extraction accuracy

**Inputs:**
- `position_report` (File)
- `fund_name` (String)

**Outputs:**
- `bank_cash_balance` (Float)
- `bank_balance_date` (String)

---

### Step 2: NAV Pack Extraction (Team)

**Purpose:** Parse the NAV Pack Excel workbook and extract the trial balance ending balance for account 10010.

**Type:** Team (Agentic)

**Rationale:** Excel interpretation requires understanding workbook structure, finding the correct sheet, locating account 10010 row, and extracting the ending balance column.

**Agents:**
- `speaker_selector` — Coordinates extraction workflow
- `excel_reader` — Reads workbook structure and content
- `data_extractor` — Locates account 10010 and extracts balance
- `validator` — Confirms extraction accuracy

**Inputs:**
- `nav_pack` (File)
- `fund_name` (String)

**Outputs:**
- `nav_pack_balance` (Float)
- `nav_pack_date` (String)

---

### Step 3: Balance Comparison (Delegate)

**Purpose:** Compare the bank balance to the NAV Pack balance and determine if there's a variance.

**Type:** Delegate (Deterministic)

**Rationale:** Simple arithmetic comparison - no reasoning required.

**Logic:**
```python
variance = bank_cash_balance - nav_pack_balance
is_matched = abs(variance) < 0.01  # Tolerance for floating point
```

**Inputs:**
- `bank_cash_balance` (Float)
- `nav_pack_balance` (Float)

**Outputs:**
- `is_matched` (Boolean)
- `variance_amount` (Float)

---

### Step 4: Generate Result (Delegate)

**Purpose:** Generate a result report with match/mismatch status.

**Type:** Delegate (Deterministic)

**Rationale:** Template-based output generation.

**Logic:**
- If matched: "Reconciliation complete. Bank balance matches NAV Pack."
- If mismatched: "MISMATCH DETECTED. Variance: $X. Please run Workflow 2 (Mismatch Analysis) with transaction report and daily cash file."

**Inputs:**
- `is_matched` (Boolean)
- `variance_amount` (Float)
- `fund_name` (String)
- `quarter_end_date` (String)
- `bank_cash_balance` (Float)
- `nav_pack_balance` (Float)

**Outputs:**
- `reconciliation_status` (String)
- `initial_check_report` (File)

---

## Workflow 2: Mismatch Analysis

### Input Variables

| Variable | Type | Description |
|----------|------|-------------|
| `transaction_report` | File | Bank transaction report PDF from JP Morgan portal |
| `daily_cash_file` | File | Daily cash file Excel |
| `variance_amount` | Float | Variance amount from Workflow 1 |
| `fund_name` | String | Fund being analyzed |
| `quarter_end_date` | String | Quarter end date |

### Output Variables

| Variable | Type | Description |
|----------|------|-------------|
| `root_cause_summary` | String | Summary of break cause |
| `missing_entries` | String | JSON list of unrecorded transactions |
| `is_valid_break` | Boolean | True if timing difference (no action needed) |
| `remediation_entries` | String | JSON list of recommended Investran entries |
| `analysis_report` | File | Comprehensive analysis report |

---

### Step 1: Transaction Analysis (Team)

**Purpose:** Analyze the break by comparing transaction report entries against daily cash file to identify missing/unrecorded transactions and determine root cause.

**Type:** Team (Agentic)

**Rationale:** Requires reasoning about transaction patterns, matching entries between two sources, categorizing discrepancies, and determining root cause (missing entry, timing difference, or unknown bank entry).

**Agents:**
- `speaker_selector` — Coordinates analysis
- `transaction_parser` — Parses transaction report PDF
- `cash_file_parser` — Parses daily cash file Excel
- `reconciliation_analyst` — Compares entries and identifies gaps
- `root_cause_analyst` — Determines cause of each discrepancy

**Inputs:**
- `transaction_report` (File)
- `daily_cash_file` (File)
- `variance_amount` (Float)
- `fund_name` (String)

**Outputs:**
- `root_cause_summary` (String)
- `missing_entries` (String)
- `is_valid_break` (Boolean)
- `remediation_entries` (String)

---

### Step 2: Generate Analysis Report (Delegate)

**Purpose:** Compile all findings into a structured analysis report.

**Type:** Delegate (Deterministic)

**Rationale:** Structured output generation from collected variables.

**Inputs:**
- All output variables from Step 1
- `fund_name` (String)
- `quarter_end_date` (String)
- `variance_amount` (Float)

**Outputs:**
- `analysis_report` (File)

---

## Teams vs Delegates Summary

| Workflow | Component | Type | Rationale |
|----------|-----------|------|-----------|
| 1 | Position Report Extraction | **Team** | PDF parsing requires document understanding |
| 1 | NAV Pack Extraction | **Team** | Excel interpretation, finding account 10010 |
| 1 | Balance Comparison | **Delegate** | Simple arithmetic comparison |
| 1 | Generate Result | **Delegate** | Template-based output |
| 2 | Transaction Analysis | **Team** | Reasoning about transaction patterns |
| 2 | Generate Analysis Report | **Delegate** | Structured output generation |

---

## User Journey

| Step | User Action | System Response |
|------|-------------|-----------------|
| 1 | Download Position Report from JP Morgan | — |
| 2 | Download NAV Pack from Box | — |
| 3 | Run Workflow 1 with files | Extracts balances, compares |
| 4a | (If match) Review confirmation | Done |
| 4b | (If mismatch) Note variance amount | Instructed to run Workflow 2 |
| 5 | Download Transaction Report from JP Morgan | — |
| 6 | Gather Daily Cash File | — |
| 7 | Run Workflow 2 with files | Analyzes break, generates remediation |
| 8 | Review analysis report | Book entries in Investran |

---

## MVP Simplifications

| Simplification | MVP Approach | Future Enhancement |
|----------------|--------------|-------------------|
| Fund scope | Single fund per run | Batch processing with Map |
| Bank accounts | Single bank account | Multi-bank consolidation |
| System integration | Manual file upload | API integration with JP Morgan, Investran |
| Tolerance | Any variance is flagged | Configurable materiality threshold |
| Audit trail | Output files only | Persistent audit log database |
| Valid breaks | Manual identification | Automated cut-off time checking |
| Workflow chaining | Manual invocation | Auto-trigger Workflow 2 |
| Daily Cash File | Manual input required | Auto-generate from transaction report |

---

## Future Automation Opportunity: Daily Cash File Generation

### Current State (Manual BAU Process)

Controllers currently perform a **daily** manual process to maintain the Daily Cash File:

1. Log in to bank portal (JP Morgan)
2. Download that day's transaction report
3. Copy-paste transaction details into Daily Cash File (Excel)
4. Use this file to book transactions in Investran and track activity

This is a repetitive, error-prone process performed every business day.

### Automation Opportunity

The Daily Cash File could be **automatically generated** by parsing the Bank Transaction Report, potentially eliminating:
- Daily manual download and copy-paste work
- Data entry errors from manual transcription
- The need to request/maintain historical Daily Cash Files

### Proposed Enhancement

Add an optional **Workflow 0: Daily Cash File Generation**:

```
┌─────────────────────────────────────────────────────────────────────┐
│  WORKFLOW 0: DAILY CASH FILE GENERATION (Future)                    │
├─────────────────────────────────────────────────────────────────────┤
│  [User Upload] → Bank Transaction Report (PDF)                      │
│        ↓                                                            │
│  [Team] Parse transaction report, extract all transactions          │
│        ↓                                                            │
│  [Delegate] Generate Daily Cash File Excel in standard format       │
│        ↓                                                            │
│  Output: Generated Daily Cash File ready for Workflow 2             │
└─────────────────────────────────────────────────────────────────────┘
```

### Impact on Current Architecture

- **Workflow 2** currently requires `daily_cash_file` as input
- With this enhancement, Workflow 2 could either:
  - Accept the auto-generated file from Workflow 0
  - Parse the transaction report directly (eliminating Daily Cash File dependency)

### Open Questions

See [Open Questions](./cash_custody_open_questions.md) — Q21-Q23 for Daily Cash File automation questions

---

## Output Artifacts

### Workflow 1 Output
- **Initial Check Report** — Match/Mismatch status with extracted balances

### Workflow 2 Output
- **Analysis Report** — Comprehensive document including:
  - Fund and period details
  - Variance amount and direction
  - Root cause analysis
  - Missing transaction details
  - Recommended remediation entries for Investran
  - Valid break flag (if timing difference)

---

## Related Documents

- [Cash Custody Process Flowchart](./cash_custody_flowchart.md) — Detailed current-state process
- [Axon Workflow Diagrams](./cash_custody_axon_workflow.md) — Mermaid diagrams for both workflows
- [Open Questions](./cash_custody_open_questions.md) — Items requiring clarification
