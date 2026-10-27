󠀁󠁃󠁏󠁃󠁟󠁈󠁄󠁒␂ # Contributing to VDE

First off, thank you for considering contributing to **[VDE](https://github.com/VicRodger27/VDE)**! It is people like you who make open source such a great place to build, learn, and create.

All contributors are expected to uphold our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). For questions or sensitive inquiries, check [CONTACT.md](CONTACT.md).

---

## Getting Started

1. **Check Existing Issues:** Before opening a new issue or PR, search our [Issue Tracker](https://github.com/VicRodger27/VDE/issues) to see if someone else has already reported or addressed it.
2. **First Contributions:** Look for issues tagged `good first issue` or `help wanted` if you are new to the project.

---

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/VicRodger27/VDE.git
   cd VDE
   ```
2. Install dependencies:
   ```bash
   quadro install
   ```
3. Run verification / tests locally:
   ```bash
   quadro test
   quadro lint
   ```

---

## How to Report Bugs

When filing a bug report, please include:
- A clear, descriptive title.
- Steps to reproduce the behavior (minimal reproduction).
- Expected vs. actual behavior.
- Operating system, browser, or runtime version.
- Any relevant logs, stack traces, or screenshots.

---

## Pull Request Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-new-feature
   ```
2. Write clean, documented code that follows the existing project conventions.
3. Verify tests and lint checks pass before pushing:
   ```bash
   quadro lint
   ```
4. Open a Pull Request against `main`. Include a concise summary of what changes were made and why.

### Pull Request Checklist
- [ ] Code follows existing formatting and style conventions.
- [ ] Tests and linter pass locally.
- [ ] Documentation has been updated for any user-facing changes.
- [ ] Related issue numbers are referenced (e.g. `Fixes #123`).

---

## Code of Conduct

Participation in this project is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). By contributing, you agree to abide by its terms. ␃
