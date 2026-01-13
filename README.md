# Test Runner and Skills

## Using test_runner.py

Run multiple test cases from a JSON file.

### Command

```bash
python3 test_runner.py <test_cases_file> [options]
```

### Parameters

- `test_cases_file` (required): JSON file containing test cases
- `--result-dir` (optional): Custom directory for results (default: `result_timestamp`)
- `--no-status-check` (optional): Skip status monitoring, just trigger workflows
- `--max-wait-time` (optional): Maximum wait time in seconds (default: 3600)

### Example

```bash
python3 test_runner.py example_test_cases.json
```

### JSON Input Format

Create a JSON file with test cases:

```json
{
  "test_cases": [
    {
      "test_id": "TC-001",
      "title": "Test Case Title",
      "workflow_name": "Apollo - Cash Custody Initial Check V1",
      "namespace": "default",
      "fund_name": "AP WINDSOR CO-INVEST, L.P.",
      "quarter_end_date": "2025-09-30",
      "position_report_file": "test_cases_and_testing_data/test_data/Test-Data-Position-Report.csv",
      "navpack_file": "input_data/AP Windsor - NAV Pack.xlsm"
    }
  ]
}
```

**Required fields:**
- `workflow_name`: Name of the workflow to execute
- Workflow input parameters (e.g., `fund_name`, `position_report_file`, etc.)

**Optional fields:**
- `test_id`: Test case identifier
- `title`: Test case description
- `namespace`: Workflow namespace (default: "default")

### Input Data Files

You can specify file paths in three ways:

1. **Full relative path** (recommended): Include the folder path
   ```json
   "position_report_file": "test_cases_and_testing_data/test_data/Test-Data-Position-Report.csv",
   "navpack_file": "input_data/AP Windsor - NAV Pack.xlsm"
   ```

2. **Just filename**: The test runner will search in:
   - `test_cases_and_testing_data/test_data/`
   - `input_data/`
   ```json
   "position_report_file": "Test-Data-Position-Report.csv"
   ```

3. **Absolute path**: Use full system path
   ```json
   "position_report_file": "/full/path/to/file.csv"
   ```

### Results

Results are saved to `result_YYYYMMDD_HHMMSS/`:
- Each test case has its own folder (e.g., `TC-001/`)
- Contains: `execution_result.json`, `status_report.json`, `outputs/` folder
- Summary saved to `test_summary.json`

---

## Using Skills Directly

**Note:** These commands can be executed directly in Cursor AI chat. All commands start with a colon `:` prefix.

### 1. Trigger Workflow

**Cursor AI Command:**
```
:trigger_workflow "WorkflowName" --namespace "default" --input "param1" "value1"
```

### 2. Get Workflow Status

**Cursor AI Command:**
```
:get_workflow_status "execution-id"
:get_workflow_status "execution-id" --monitor
```

### 3. Get Workflow Outputs

**Cursor AI Command:**
```
:get_workflow_outputs "execution-id" --download --output-dir "./outputs"
```

### 4. Get All Workflows

**Cursor AI Command:**
```
:get_all_workflow
:get_all_workflow --namespace "MyNamespace"
```

---

## Workflow

1. **Trigger** → Get `execution_id`
2. **Check Status** → Wait for completion
3. **Get Outputs** → Download results (if completed)
