# Cerberus Challenge Author Guide

> Version: Phase 7

## 1. Authoring Model

Each challenge includes:
- title
- category
- difficulty
- type
- visibility
- hierarchical unlock rule

## 2. Multi-part Challenge Design

### 2.1 Structure
- Create parent challenge.
- Add sub-challenges with deterministic order.
- Assign unique flags per part.

### 2.2 Best practices
- Part 1 should bootstrap understanding.
- Later parts should increase depth, not random complexity.
- Keep part descriptions concise and testable.

## 3. Hints

### 3.1 Hint strategy
- Provide minimal guidance before giving direct clues.
- Use progressive hints if possible.

### 3.2 Penalty tuning
- Small hints: low penalty.
- Direct hints: moderate/high penalty.
- Ensure penalty values align with challenge point weight.

## 4. Hierarchical Unlock Rules

- Use `requires_challenge_id` style prerequisites.
- Prefer explicit dependency chains over hidden conditions.
- Avoid circular unlock dependencies.

## 5. Quality Checklist

- Verify all flags before publishing.
- Validate all file artifacts and hashes.
- Ensure challenge does not require unstable third-party services.
- Add expected solve path notes for event admins.
