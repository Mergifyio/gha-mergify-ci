# Project conventions

## Git / PRs: always use `mergify stack`

Push and manage all branches and pull requests with the Mergify Stack workflow.

- **Push** with `mergify stack push` — never `git push`.
- **Create PRs** through `mergify stack push` — never `gh pr create`.
- **Fix a commit** by amending it (`git commit --amend`) — don't pile on "fix" commits.
- The PR title/body come from the commit message, so write commit messages as PR descriptions.
- PRs stay as drafts; the human takes them out of draft.
- Branch names must use the `devs/**` prefix — the repo ruleset rejects other prefixes.
