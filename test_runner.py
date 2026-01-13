"""
Test Runner - Executes multiple test cases from a JSON file.

This class:
1. Reads a JSON file containing a list of test cases
2. For each test case, triggers the workflow
3. Saves results to result_timestamp folder with separate folders for each test case
4. Monitors execution status for running workflows
5. Downloads outputs for successful executions
6. Updates error reports for failed executions
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from skills.trigger_workflow.trigger_workflow import trigger_workflow
from skills.get_workflow_status.get_workflow_status import get_workflow_status
from skills.get_workflow_outputs.get_workflow_outputs import get_workflow_outputs


def find_test_file(filename: str, project_root: Path) -> Path:
    """Find test data file in input_data or test_data directories."""
    # Check test_data directory first
    test_data_dir = project_root / "test_cases_and_testing_data" / "test_data"
    test_file = test_data_dir / filename
    if test_file.exists():
        return test_file
    
    # Check input_data directory
    input_data_dir = project_root / "input_data"
    test_file = input_data_dir / filename
    if test_file.exists():
        return test_file
    
    # Return relative path if not found (will be handled by workflow)
    return Path(filename)


class TestRunner:
    """Test runner that executes multiple test cases from a JSON file."""
    
    def __init__(self, test_cases_file: str, result_base_dir: Optional[str] = None):
        """
        Initialize the test runner.
        
        Args:
            test_cases_file: Path to JSON file containing test cases
            result_base_dir: Base directory for results (default: result_timestamp)
        """
        self.test_cases_file = Path(test_cases_file)
        self.project_root = Path(__file__).parent
        
        # Create result directory with timestamp
        if result_base_dir:
            self.result_dir = Path(result_base_dir)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.result_dir = self.project_root / f"result_{timestamp}"
        
        self.result_dir.mkdir(parents=True, exist_ok=True)
        
        # Load test cases
        self.test_cases = self._load_test_cases()
        
        # Results tracking
        self.results = []
        
    def _load_test_cases(self) -> List[Dict]:
        """Load test cases from JSON file."""
        if not self.test_cases_file.exists():
            raise FileNotFoundError(f"Test cases file not found: {self.test_cases_file}")
        
        with open(self.test_cases_file, 'r') as f:
            data = json.load(f)
        
        # Support both list of test cases and object with test_cases key
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "test_cases" in data:
            return data["test_cases"]
        else:
            raise ValueError("JSON file must contain a list of test cases or an object with 'test_cases' key")
    
    def _resolve_file_paths(self, test_case: Dict) -> Dict:
        """Resolve file paths in test case parameters."""
        resolved = test_case.copy()
        
        # Common file parameter names
        file_params = [
            "position_report_file", "navpack_file", "transaction_report_file",
            "daily_cash_file", "navpack_file", "input_file", "file"
        ]
        
        for param in file_params:
            if param in resolved and isinstance(resolved[param], str):
                file_path = Path(resolved[param])
                
                # If it's an absolute path and exists, use it directly
                if file_path.is_absolute() and file_path.exists():
                    resolved[param] = str(file_path)
                # If it's a relative path, check if it exists relative to project root
                elif not file_path.is_absolute():
                    # Try as relative path from project root
                    full_path = self.project_root / file_path
                    if full_path.exists():
                        resolved[param] = str(full_path)
                    else:
                        # Fall back to finding by filename only
                        resolved_path = find_test_file(file_path.name, self.project_root)
                        resolved[param] = str(resolved_path)
                # If absolute path doesn't exist, keep as is (may be handled by workflow)
                else:
                    resolved[param] = str(file_path)
        
        return resolved
    
    def _save_test_result(self, test_case_id: str, result: Dict):
        """Save test result to test case folder."""
        test_case_dir = self.result_dir / test_case_id
        test_case_dir.mkdir(parents=True, exist_ok=True)
        
        # Save execution result
        result_file = test_case_dir / "execution_result.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        return test_case_dir
    
    def _save_status_report(self, test_case_id: str, status_result: Dict):
        """Save status report to test case folder."""
        test_case_dir = self.result_dir / test_case_id
        test_case_dir.mkdir(parents=True, exist_ok=True)
        
        # Save status report
        status_file = test_case_dir / "status_report.json"
        with open(status_file, 'w') as f:
            json.dump(status_result, f, indent=2)
        
        return test_case_dir
    
    def _save_error_report(self, test_case_id: str, error_info: Dict):
        """Save error report to test case folder."""
        test_case_dir = self.result_dir / test_case_id
        test_case_dir.mkdir(parents=True, exist_ok=True)
        
        # Save error report
        error_file = test_case_dir / "error_report.json"
        with open(error_file, 'w') as f:
            json.dump(error_info, f, indent=2)
        
        return test_case_dir
    
    def run_test_case(self, test_case: Dict) -> Dict:
        """
        Run a single test case.
        
        Args:
            test_case: Test case dictionary with parameters
            
        Returns:
            Dictionary with execution result
        """
        test_case_id = test_case.get("test_id") or test_case.get("id") or f"TC-{len(self.results) + 1:03d}"
        test_case_title = test_case.get("title", "Untitled Test Case")
        
        print("=" * 70)
        print(f"🧪 Test Case: {test_case_id}")
        print(f"   Title: {test_case_title}")
        print("=" * 70)
        print()
        
        result = {
            "test_case_id": test_case_id,
            "test_case_title": test_case_title,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "execution_id": None,
            "status": None,
            "error": None
        }
        
        try:
            # Extract workflow parameters
            workflow_name = test_case.get("workflow_name")
            namespace = test_case.get("namespace", "default")
            
            if not workflow_name:
                raise ValueError("workflow_name is required in test case")
            
            # Get workflow inputs (everything except metadata fields)
            metadata_fields = ["test_id", "id", "title", "workflow_name", "namespace", "category", "priority", "status"]
            workflow_inputs = {
                k: v for k, v in test_case.items() 
                if k not in metadata_fields
            }
            
            # Resolve file paths
            workflow_inputs = self._resolve_file_paths(workflow_inputs)
            
            print(f"🚀 Triggering workflow: {workflow_name}")
            print(f"   Namespace: {namespace}")
            print(f"   Inputs: {list(workflow_inputs.keys())}")
            print()
            
            # Trigger workflow
            trigger_result = trigger_workflow(
                workflow_name=workflow_name,
                namespace=namespace,
                **workflow_inputs
            )
            
            if not trigger_result.get("success"):
                result["error"] = trigger_result.get("error", "Failed to trigger workflow")
                result["status"] = "TriggerFailed"
                self._save_test_result(test_case_id, result)
                return result
            
            execution_id = trigger_result.get("execution_id")
            result["execution_id"] = execution_id
            result["status"] = "Running"
            
            # Save initial execution result
            self._save_test_result(test_case_id, {
                **result,
                "trigger_result": trigger_result
            })
            
            print(f"   ✓ Workflow triggered: {execution_id}")
            print()
            
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "Error"
            self._save_test_result(test_case_id, result)
            print(f"   ❌ Error: {str(e)}")
            print()
        
        return result
    
    def check_and_update_status(self, test_result: Dict) -> Dict:
        """
        Check workflow status and update result.
        
        Args:
            test_result: Test result dictionary with execution_id
            
        Returns:
            Updated test result dictionary
        """
        test_case_id = test_result["test_case_id"]
        execution_id = test_result.get("execution_id")
        
        if not execution_id:
            return test_result
        
        print(f"📊 Checking status for {test_case_id} (execution: {execution_id})...")
        
        try:
            # Get current status
            status_result = get_workflow_status(flow_execution_id=execution_id, monitor=False)
            
            if not status_result.get("success"):
                test_result["error"] = status_result.get("error", "Failed to get status")
                test_result["status"] = "StatusCheckFailed"
                self._save_error_report(test_case_id, {
                    "test_case_id": test_case_id,
                    "execution_id": execution_id,
                    "error": test_result["error"],
                    "timestamp": datetime.now().isoformat()
                })
                return test_result
            
            status = status_result.get("status")
            test_result["status"] = status
            test_result["status_details"] = {
                "status": status,
                "start_time": status_result.get("start_time"),
                "end_time": status_result.get("end_time"),
                "token_usage": status_result.get("token_usage", 0)
            }
            
            # Save status report
            self._save_status_report(test_case_id, status_result)
            
            # Handle terminal states
            if status == "Completed":
                print(f"   ✅ Completed - downloading outputs...")
                self._download_outputs(test_case_id, execution_id)
                test_result["success"] = True
            elif status == "Failed":
                print(f"   ❌ Failed")
                failure_reason = status_result.get("failure_reason", "Unknown failure")
                failure_detail = status_result.get("failure_detail", "")
                test_result["error"] = failure_reason
                test_result["failure_detail"] = failure_detail
                self._save_error_report(test_case_id, {
                    "test_case_id": test_case_id,
                    "execution_id": execution_id,
                    "status": "Failed",
                    "failure_reason": failure_reason,
                    "failure_detail": failure_detail,
                    "timestamp": datetime.now().isoformat()
                })
            elif status in ["Cancelled", "Killed"]:
                print(f"   ⚠️  {status}")
                test_result["error"] = f"Workflow was {status.lower()}"
                self._save_error_report(test_case_id, {
                    "test_case_id": test_case_id,
                    "execution_id": execution_id,
                    "status": status,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                print(f"   ⏳ Still running...")
            
        except Exception as e:
            test_result["error"] = f"Error checking status: {str(e)}"
            print(f"   ❌ Error: {str(e)}")
        
        return test_result
    
    def _download_outputs(self, test_case_id: str, execution_id: str):
        """Download output files for a completed workflow."""
        try:
            test_case_dir = self.result_dir / test_case_id
            output_dir = test_case_dir / "outputs"
            
            print(f"   📥 Downloading outputs to: {output_dir}")
            
            outputs_result = get_workflow_outputs(
                flow_execution_id=execution_id,
                download=True,
                output_dir=str(output_dir)
            )
            
            if outputs_result.get("success"):
                file_count = outputs_result.get("output_files_count", 0)
                print(f"   ✓ Downloaded {file_count} file(s)")
            else:
                print(f"   ⚠️  Failed to download outputs: {outputs_result.get('error')}")
            
        except Exception as e:
            print(f"   ⚠️  Error downloading outputs: {str(e)}")
    
    def run_all(self, check_status: bool = True, max_wait_time: int = 3600):
        """
        Run all test cases.
        
        Args:
            check_status: Whether to check status for running workflows
            max_wait_time: Maximum time to wait for workflows to complete (seconds)
        """
        print("=" * 70)
        print("🚀 Test Runner")
        print("=" * 70)
        print(f"📁 Test Cases File: {self.test_cases_file}")
        print(f"📁 Results Directory: {self.result_dir}")
        print(f"📊 Total Test Cases: {len(self.test_cases)}")
        print("=" * 70)
        print()
        
        # Phase 1: Trigger all workflows
        print("Phase 1: Triggering workflows...")
        print()
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"[{i}/{len(self.test_cases)}] ", end="")
            result = self.run_test_case(test_case)
            self.results.append(result)
        
        print()
        print("=" * 70)
        print("Phase 1 Complete: All workflows triggered")
        print("=" * 70)
        print()
        
        # Phase 2: Check status for running workflows
        if check_status:
            print("Phase 2: Checking workflow status...")
            print()
            
            start_time = time.time()
            running_tests = [r for r in self.results if r.get("status") == "Running" and r.get("execution_id")]
            
            while running_tests and (time.time() - start_time) < max_wait_time:
                for test_result in running_tests[:]:  # Copy list to allow modification
                    updated_result = self.check_and_update_status(test_result)
                    
                    # Update in results list
                    idx = self.results.index(test_result)
                    self.results[idx] = updated_result
                    
                    # Remove from running list if terminal state
                    if updated_result.get("status") in ["Completed", "Failed", "Cancelled", "Killed", "Error", "StatusCheckFailed"]:
                        running_tests.remove(test_result)
                
                if running_tests:
                    print(f"   ⏳ {len(running_tests)} workflow(s) still running, waiting 30 seconds...")
                    time.sleep(30)
            
            if running_tests:
                print(f"   ⚠️  {len(running_tests)} workflow(s) still running after {max_wait_time}s timeout")
            
            print()
            print("=" * 70)
            print("Phase 2 Complete: Status checks finished")
            print("=" * 70)
            print()
        
        # Save summary report
        self._save_summary_report()
        
        # Print summary
        self._print_summary()
    
    def _save_summary_report(self):
        """Save summary report of all test results."""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "result_dir": str(self.result_dir),
            "total_tests": len(self.results),
            "summary": {
                "completed": len([r for r in self.results if r.get("status") == "Completed"]),
                "failed": len([r for r in self.results if r.get("status") == "Failed"]),
                "running": len([r for r in self.results if r.get("status") == "Running"]),
                "error": len([r for r in self.results if r.get("status") in ["Error", "TriggerFailed", "StatusCheckFailed"]]),
                "cancelled": len([r for r in self.results if r.get("status") in ["Cancelled", "Killed"]])
            },
            "results": self.results
        }
        
        summary_file = self.result_dir / "test_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
    
    def _print_summary(self):
        """Print summary of test results."""
        print("=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print()
        
        completed = [r for r in self.results if r.get("status") == "Completed"]
        failed = [r for r in self.results if r.get("status") == "Failed"]
        running = [r for r in self.results if r.get("status") == "Running"]
        errors = [r for r in self.results if r.get("status") in ["Error", "TriggerFailed", "StatusCheckFailed"]]
        cancelled = [r for r in self.results if r.get("status") in ["Cancelled", "Killed"]]
        
        print(f"Total Tests: {len(self.results)}")
        print(f"  ✅ Completed: {len(completed)}")
        print(f"  ❌ Failed: {len(failed)}")
        print(f"  ⏳ Running: {len(running)}")
        print(f"  ⚠️  Errors: {len(errors)}")
        print(f"  🚫 Cancelled/Killed: {len(cancelled)}")
        print()
        
        if failed:
            print("Failed Tests:")
            for r in failed:
                print(f"  - {r['test_case_id']}: {r.get('error', 'Unknown error')}")
            print()
        
        if errors:
            print("Error Tests:")
            for r in errors:
                print(f"  - {r['test_case_id']}: {r.get('error', 'Unknown error')}")
            print()
        
        print(f"📁 Results saved to: {self.result_dir}")
        print(f"📄 Summary report: {self.result_dir / 'test_summary.json'}")
        print("=" * 70)


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run test cases from JSON file")
    parser.add_argument("test_cases_file", help="JSON file containing test cases")
    parser.add_argument("--result-dir", type=str, default=None,
                       help="Base directory for results (default: result_timestamp)")
    parser.add_argument("--no-status-check", action="store_true",
                       help="Don't check status for running workflows")
    parser.add_argument("--max-wait-time", type=int, default=3600,
                       help="Maximum time to wait for workflows (seconds, default: 3600)")
    
    args = parser.parse_args()
    
    # Create and run test runner
    runner = TestRunner(
        test_cases_file=args.test_cases_file,
        result_base_dir=args.result_dir
    )
    
    runner.run_all(
        check_status=not args.no_status_check,
        max_wait_time=args.max_wait_time
    )


if __name__ == "__main__":
    main()
