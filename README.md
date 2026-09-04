# Mistral Vibe in Docker Sandboxes

A small, deliberately broken FastAPI application for trying Mistral Vibe in Docker
Sandboxes. Vibe runs inside a microVM, works on the `app/` workspace, and authenticates
through the Docker Sandboxes host proxy. The real `MISTRAL_API_KEY` stays on the host.

## Prerequisites

- Docker Sandboxes 0.39.0 or newer
- A Mistral API key from <https://console.mistral.ai/>

Docker Sandboxes kits and environment files are experimental. Their syntax may change.

## Run the demo

Allow kits from this GitHub account. This setting replaces the complete source allowlist,
so the command keeps Docker Hub too:

```bash
sbx settings set kit.allowedSources '["docker.io/","github.com/shelajev/"]'
```

Store the Mistral key on the host. The command prompts for the value and saves it in the
host secret store:

```bash
sbx secret set mistral
```

Clone this repository and start the declared environment:

```bash
git clone https://github.com/shelajev/mistral-vibe-sbx-demo.git
cd mistral-vibe-sbx-demo
sbx env run
```

The first run creates the `mistral-vibe-demo` sandbox, installs Vibe from its official
installer, mounts `app/` as the workspace, and opens Vibe. Later runs reattach to the same
environment. Approve Vibe's trust prompt on the first launch so it loads the project-level
`.vibe/config.toml`.

## Verify that the key stayed outside

At the Vibe prompt, run this shell command:

```text
!printf 'MISTRAL_API_KEY=%s\n' "$MISTRAL_API_KEY"
```

The value inside the sandbox is a sentinel:

```text
MISTRAL_API_KEY=proxy-managed
```

The Docker Sandboxes proxy replaces that sentinel with the stored key only when Vibe sends
an allowed request to the declared Mistral API, account, or managed-config hosts.

## Give Vibe a real task

Paste this prompt into Vibe:

```text
Run the test suite and diagnose the failure. Fix the application code without changing
the tests or the public API contract. Run the full test suite again and summarize the
cause and your change.
```

The application has a small bug in its `completed` query filter. A correct fix ends with:

```text
3 passed
```

To reset the exercise after Vibe fixes it:

```bash
git restore app/main.py
```

## Try another Mistral-hosted model

The project selects `mistral-medium-latest` in `app/.vibe/config.toml`. Use `/model` inside
Vibe and select `zai-glm-5-2` to run the same agent with GLM 5.2 hosted by Mistral. This
repository does not benchmark the two models; it only makes the switch easy to try.

## Remove the environment

```bash
sbx env rm --force
```
