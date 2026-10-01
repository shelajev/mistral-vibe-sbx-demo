# Verified terminal captures

These PNGs render recorded CLI output, rather than screenshots of a native terminal window. The computer-use tool does not permit access to Terminal or Ghostty in this session.

- `01-key-placeholder.png`: actual `sbx env exec` output showing the credential sentinel and Vibe version.
- `02-vibe-fix.png`: excerpts from Vibe's actual test failure and passing rerun, with the resulting Git diff.
- The matching `.txt` files contain exactly the text rendered into each PNG.
- `vibe-task-transcript.txt` records user/assistant messages and tool results; reasoning events are excluded and trailing whitespace is trimmed.

Captured on 2026-10-01 using Docker Sandboxes 0.46.0-rc5 and the published v3 Vibe 2.25.8 kit.
