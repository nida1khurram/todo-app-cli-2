"""Test runner script for Phase II verification.

This script runs all tests and reports results.

Usage:
    python scripts/run_tests.py
"""

import subprocess
import sys
from typing import List, Tuple


def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    print(output)

    return result.returncode == 0, output


def main():
    """Run all verification tests."""
    print("Phase II - Full-Stack Todo App Verification Tests")
    print("=" * 60)

    results = []

    # Backend Tests
    print("\n\n" + "=" * 60)
    print("BACKEND TESTS")
    print("=" * 60)

    # US1 Auth Tests (T058)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_models_user.py", "-v"],
        "US1: User Model Tests (T027)"
    )
    results.append(("US1: User Model Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_auth_password.py", "-v"],
        "US1: Password Tests (T028)"
    )
    results.append(("US1: Password Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_auth_jwt.py", "-v"],
        "US1: JWT Tests (T029)"
    )
    results.append(("US1: JWT Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_auth.py", "-v"],
        "US1: Auth Routes Tests (T030-T032)"
    )
    results.append(("US1: Auth Routes Tests", success))

    # US2 Task Tests (T083)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_models_task.py", "-v"],
        "US2: Task Model Tests (T062)"
    )
    results.append(("US2: Task Model Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py", "-v"],
        "US2: Task Routes Tests (T063-T064)"
    )
    results.append(("US2: Task Routes Tests", success))

    # US3 Update/Delete Tests (T111)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestUpdateTaskEndpoint", "-v"],
        "US3: Update Task Tests (T097)"
    )
    results.append(("US3: Update Task Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestDeleteTaskEndpoint", "-v"],
        "US3: Delete Task Tests (T098)"
    )
    results.append(("US3: Delete Task Tests", success))

    # US4 Completion Tests (T123)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestToggleTaskComplete", "-v"],
        "US4: Toggle Completion Tests (T114)"
    )
    results.append(("US4: Toggle Completion Tests", success))

    # US5 Priority Tests (T135)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_models_task.py::TestTaskModel::test_task_default_priority_is_medium", "-v"],
        "US5: Priority Tests (T126)"
    )
    results.append(("US5: Priority Tests", success))

    # US6 Tag Tests (T165)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_models_tag.py", "-v"],
        "US6: Tag Model Tests (T138)"
    )
    results.append(("US6: Tag Model Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tags.py", "-v"],
        "US6: Tag Routes Tests (T140)"
    )
    results.append(("US6: Tag Routes Tests", success))

    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_models_task_tag.py", "-v"],
        "US6: TaskTag Tests (T139)"
    )
    results.append(("US6: TaskTag Tests", success))

    # US7 Search Tests (T177)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestTaskFilters::test_search_tasks", "-v"],
        "US7: Search Tests (T168)"
    )
    results.append(("US7: Search Tests", success))

    # US8 Filter Tests (T195)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestTaskFilters", "-v"],
        "US8: Filter Tests (T180)"
    )
    results.append(("US8: Filter Tests", success))

    # US9 Sort Tests (T208)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_routes_tasks.py::TestTaskSorting", "-v"],
        "US9: Sort Tests (T198)"
    )
    results.append(("US9: Sort Tests", success))

    # US10 User Isolation Tests (T095)
    success, _ = run_command(
        ["python", "-m", "pytest", "backend/tests/test_user_isolation.py", "-v"],
        "US10: User Isolation Tests (T087-T089)"
    )
    results.append(("US10: User Isolation Tests", success))

    # Frontend Tests
    print("\n\n" + "=" * 60)
    print("FRONTEND TESTS")
    print("=" * 60)

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/ui/button.test.tsx", "--passWithNoTests"],
        "US1: Button Tests (T033)"
    )
    results.append(("US1: Button Tests", success))

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/ui/input.test.tsx", "--passWithNoTests"],
        "US1: Input Tests (T034)"
    )
    results.append(("US1: Input Tests", success))

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/task/task-card.test.tsx", "--passWithNoTests"],
        "US2: Task Card Tests (T065)"
    )
    results.append(("US2: Task Card Tests", success))

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/task/priority-badge.test.tsx", "--passWithNoTests"],
        "US5: Priority Badge Tests (T127)"
    )
    results.append(("US5: Priority Badge Tests", success))

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/task/search-bar.test.tsx", "--passWithNoTests"],
        "US7: Search Bar Tests (T169)"
    )
    results.append(("US7: Search Bar Tests", success))

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/components/task/tag-input.test.tsx", "--passWithNoTests"],
        "US6: Tag Input Tests (T142)"
    )
    results.append(("US6: Tag Input Tests", success))

    # E2E Tests
    print("\n\n" + "=" * 60)
    print("E2E TESTS")
    print("=" * 60)

    success, _ = run_command(
        ["npm", "test", "--", "frontend/__tests__/e2e/", "--passWithNoTests"],
        "E2E: All E2E Tests (T211-T213)"
    )
    results.append(("E2E Tests", success))

    # Summary
    print("\n\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
