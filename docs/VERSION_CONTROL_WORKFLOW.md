# Version Control Workflow — MLOps Iris Classifier

## 1. Overview

This document describes the Git-based version control workflow used for the MLOps Iris Classifier project, developed as part of MLOps Lab Experiment 2.

* **Repository:** https://github.com/nayanchaudhari001-blip/mlops-iris-classifier
* **Primary language:** Python
* **Maintainer:** Nayan Kailash Chaudhari

## 2. Branching Strategy

| Branch            | Purpose                                        |
| ----------------- | ---------------------------------------------- |
| `main`            | Stable project code                            |
| `develop`         | Integration branch for development             |
| `feature/<name>`  | Individual feature development                 |
| `conflict-demo-*` | Demonstration of Git merge conflict resolution |

The feature development workflow used in this project was:

`feature/add-classification-report` → Pull Request → `develop` → `main`

The project also used separate conflict-demo branches to demonstrate merge conflict resolution.

## 3. Commit Convention

Commits use a short, imperative message with a type prefix:

* `feat:` — Add new functionality
* `fix:` — Correct a bug
* `docs:` — Documentation changes
* `chore:` — Tooling or configuration changes
* `refactor:` — Code changes without changing behavior

Example:

`feat: add classification report to training script`

## 4. Standard Workflow

The project followed this general workflow:

```bash
git switch develop
git pull origin develop
git switch -c feature/<short-description>

# Make changes

git add <files>
git commit -m "feat: <description>"
git push -u origin feature/<short-description>
```

A Pull Request was then created on GitHub from the feature branch into `develop`.

After review and approval, the feature was merged.

## 5. Merge Conflict Resolution Process

The project demonstrated Git merge conflict resolution using the `conflict-demo-a` and `conflict-demo-b` branches.

The general process was:

1. Attempt the merge.
2. Identify the conflicted file.
3. Open the file and locate Git conflict markers.
4. Decide which changes to keep or combine.
5. Remove the conflict markers.
6. Stage the resolved file using `git add`.
7. Complete the merge using `git commit`.
8. Verify the project by running:

```bash
python src/train.py
```

## 6. .gitignore Policy for ML Artifacts

The project excludes generated and environment-specific files from Git.

Examples include:

* Python cache files
* Virtual environments
* CSV and Parquet datasets
* Generated machine-learning models
* Jupyter checkpoints
* Environment files
* IDE configuration files

The following are ignored:

```text
.venv/
venv/
__pycache__/
*.pyc
data/*.csv
data/*.parquet
models/*.pkl
models/*.joblib
.ipynb_checkpoints/
.env
.vscode/
.idea/
```

## 7. Pull Request Checklist

* [x] Code runs successfully using `python src/train.py`
* [x] No large data or model files are accidentally staged
* [x] Commit messages follow the project convention
* [x] Feature branch is developed from `develop`
* [x] Pull Request is created for feature integration
* [x] Merge conflicts are resolved before final integration

## 8. Verification Log

| Check                                        | Status |
| -------------------------------------------- | ------ |
| Git version ≥ 2.30                           | ✅      |
| Git configuration verified                   | ✅      |
| Git Bash configured in VS Code               | ✅      |
| Repository has 3+ branches                   | ✅      |
| Feature branch created                       | ✅      |
| Feature Pull Request merged                  | ✅      |
| Merge conflict demonstrated                  | ✅      |
| `python src/train.py` runs successfully      | ✅      |
| Accuracy and classification report displayed | ✅      |
| Documentation created                        | ✅      |

## 9. Lessons Learned / Notes

This experiment demonstrated practical Git workflows for an MLOps project, including repository initialization, branch management, feature development, Pull Requests, merge conflict resolution, remote synchronization, and maintaining clean project history.

The project also demonstrated the importance of using `.gitignore` to prevent virtual environments and generated machine-learning artifacts from being committed to the repository.
