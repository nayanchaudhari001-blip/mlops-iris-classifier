
# CI Pipeline Documentation

## 1. Overview

This project uses GitHub Actions to implement a Continuous Integration (CI) pipeline for the MLOps Iris project.

The workflow is defined in `.github/workflows/ci.yml`.

The pipeline automatically runs when code is pushed to the main or develop branches and when a pull request targets either of these branches.

The CI pipeline checks Python code quality, executes automated tests, generates test and coverage reports, and validates model accuracy against a predefined threshold.

## 2. CI Jobs

The workflow consists of three jobs.

### 2.1 Build and Lint

**Job name:** `build-and-lint`

**Purpose:** Verify that the Python source code compiles successfully and follows the configured linting standards.

**Main steps:**
- Check out the repository.
- Set up Python 3.11.
- Install project dependencies, Flake8, and testing tools.
- Compile the Python files in `src` and `tests`.
- Run Flake8 on the source code.

**Success condition:** Python compilation and linting complete without errors.

### 2.2 Test Suite

**Job name:** `test-suite`

**Dependency:** `needs: build-and-lint`

**Purpose:** Execute automated tests to verify the correctness of the data-processing pipeline and related functionality.

**Main steps:**
- Check out the repository and set up Python 3.11.
- Install project dependencies and testing tools.
- Create the required data directories.
- Collect the Iris dataset.
- Preprocess the dataset.
- Engineer features.
- Execute tests using pytest.
- Generate test results and code coverage reports.
- Upload reports as a GitHub Actions artifact named `test-and-coverage-reports`.

The artifact contains `test-results.xml` and `coverage.xml` when both files are generated successfully.

**Success condition:** All tests pass.

### 2.3 Model Quality Gate

**Job name:** `model-quality-gate`

**Dependency:** `needs: test-suite`

**Purpose:** Verify that the model satisfies the minimum acceptable accuracy requirement.

**Main steps:**
- Check out the repository and set up Python 3.11.
- Install the required dependencies.
- Prepare the Iris dataset by running collection, preprocessing, and feature engineering.
- Execute `tests/test_model_quality.py`.

The normal minimum accuracy threshold is **0.90 (90%)**.

**Success condition:** The model-quality tests pass, including the minimum accuracy assertion.

## 3. Job Dependency Order

The jobs are configured with the following dependency sequence:

```text
build-and-lint
      |
      v
  test-suite
      |
      v
model-quality-gate
```

The dependency configuration uses the `needs` keyword:

- `test-suite` requires `build-and-lint` to succeed.
- `model-quality-gate` requires `test-suite` to succeed.

Consequently, a failure in an upstream job causes downstream jobs to be skipped by default unless the workflow explicitly overrides this behavior.

## 4. Branch Protection Ruleset

A GitHub branch ruleset named **Protect main - CI checks** was configured to protect the `main` branch.

The ruleset includes:

- Requiring changes through a pull request.
- Requiring configured CI status checks to pass before merging.

The required status checks are:

- `build-and-lint`
- `test-suite`
- `model-quality-gate`

## 5. Pull Request Verification

A feature branch named `feature/ci-verification-test` was created with a harmless README change.

A pull request was opened into `main`. All three CI jobs passed successfully, and the pull request was merged.

This verified that the CI workflow runs correctly on pull requests.

## 6. Model-Quality Regression Demonstration

A temporary branch named `feature/simulate-regression` was created.

The accuracy threshold in `tests/test_model_quality.py` was temporarily changed from `0.90` to `0.999`.

Observed results:

- Build and Lint: Passed.
- Test Suite: Failed.
- Model Quality Gate: Skipped.

The test-suite failure demonstrated that the CI pipeline detects a model-quality threshold violation.

Pull Request #6 was closed without merging. The temporary branch was deleted, and the original threshold of `0.90` was verified on `main`.

## 7. Conclusion

The GitHub Actions CI pipeline automates code compilation, linting, testing, report generation, and model-quality validation.

Pull-request checks and branch protection help prevent unsuccessful changes from being merged into `main`.

The successful normal pipeline run and regression demonstration verify that the CI pipeline works correctly.
