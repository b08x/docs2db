```markdown
# docs2db Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `docs2db` TypeScript codebase. You'll learn about file naming, import/export styles, commit message conventions, and how to write and run tests. While no specific automation workflows were detected, this guide provides suggested commands and step-by-step instructions to help you work efficiently within this repository.

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `parseDocument.ts`, `dataLoader.ts`

### Import Style
- Use **relative imports** for modules within the project.
  - Example:
    ```typescript
    import { parseDocument } from './parseDocument';
    ```

### Export Style
- Use **named exports** rather than default exports.
  - Example:
    ```typescript
    // In parseDocument.ts
    export function parseDocument(doc: string): ParsedDoc { ... }

    // In another file
    import { parseDocument } from './parseDocument';
    ```

### Commit Messages
- Follow **conventional commit** style.
- Use prefixes such as `fix`.
- Keep commit messages concise (average ~50 characters).
  - Example:
    ```
    fix: handle null values in dataLoader
    ```

## Workflows

### Running Tests
**Trigger:** When you want to verify code correctness or after making changes.
**Command:** `/run-tests`

1. Identify test files (pattern: `*.test.*`).
2. Use the project's test runner (framework unknown; try `npm test` or `ts-node`).
3. Review test results and fix any failures.

### Adding a New Module
**Trigger:** When you need to add new functionality.
**Command:** `/add-module`

1. Create a new file using camelCase (e.g., `myNewModule.ts`).
2. Use named exports for all functions/types.
3. Import other modules using relative paths.
4. Write corresponding test files (e.g., `myNewModule.test.ts`).

### Writing a Commit
**Trigger:** When committing code changes.
**Command:** `/commit`

1. Write a concise, conventional commit message.
2. Use a prefix like `fix`, followed by a short description.
   - Example: `fix: update parsing logic for edge cases`

## Testing Patterns

- Test files follow the pattern: `*.test.*` (e.g., `parseDocument.test.ts`).
- The testing framework is not explicitly specified; check for scripts in `package.json` or use common TypeScript test runners like Jest or Mocha.
- Example test file structure:
  ```typescript
  import { parseDocument } from './parseDocument';

  describe('parseDocument', () => {
    it('should parse a valid document', () => {
      const result = parseDocument('...');
      expect(result).toBeDefined();
    });
  });
  ```

## Commands
| Command      | Purpose                                         |
|--------------|-------------------------------------------------|
| /run-tests   | Run all test files in the project               |
| /add-module  | Create a new module following conventions       |
| /commit      | Make a commit using the conventional style      |
```
