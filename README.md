# Mistral Vibe in Docker Sandboxes

A small, deliberately broken FastAPI application for trying Mistral Vibe in Docker
Sandboxes. Vibe runs inside a microVM, works on the `app/` workspace, and authenticates
through the Docker Sandboxes host proxy. The real `MISTRAL_API_KEY` stays on the host.

## Prerequisites

- Docker Sandboxes 0.45.0 or newer (v3 kit support)
- A Mistral API key from <https://console.mistral.ai/>
- An active Mistral completion allowance; enable pay-as-you-go if the account's
  free allowance does not permit requests

Docker Sandboxes kits and environment files are experimental. Their syntax may change.

## Run the demo

The environment uses the published v3 kit
`docker.io/olegselajev241/sbx-kit-vibe:2.25.8`. Docker Hub is allowed by default;
there is no Git kit source to add to the allowlist.

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

The first run reads `sbxenv.yaml`, pulls the kit with Vibe 2.25.8 already installed,
mounts `app/` as the workspace, and opens Vibe in `mistral-vibe-demo-v3`. Later runs
reattach to the same environment. The kit starts `vibe --trust`, so Vibe loads
`app/.vibe/config.toml` without a separate trust prompt.

The environment file uses schema version 1; the kit uses schema version 3. These
are independent formats. Older `.sbxenv.yaml` files must be named explicitly or
renamed to `sbxenv.yaml` for current `sbx env` commands to discover them.

To run the published kit directly without the environment file:

```bash
sbx run --name mistral-vibe-direct docker.io/olegselajev241/sbx-kit-vibe:2.25.8 ./app
```

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

## If Vibe seems stuck

Check the model request before starting the coding task:

```bash
sbx env exec -- bash -c \
  'vibe --trust -p "Reply with exactly: sbx-ok" --output text --max-turns 1 </dev/null'
```

Expected output: `sbx-ok`. Closing stdin matters for programmatic mode.

Repeated `HTTP 429` warnings in `~/.vibe/logs/vibe.log` mean Mistral rejected
the request and Vibe is retrying. Check the key's organization/workspace in
<https://admin.mistral.ai/plateforme/limits>. A response header such as
`X-Ratelimit-Limit-Req-Minute: 0` indicates zero request allowance. Activating
pay-as-you-go resolved that condition in the verified demo run.

For authentication failures, check `sbx secret ls` for `mistral`. For blocked
network requests, inspect `sbx policy log mistral-vibe-demo-v3`.

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

The project selects Vibe's built-in `mistral-medium-3.5` alias in `app/.vibe/config.toml`
and explicitly adds the `zai-glm-5-2` model to the menu. Use `/model` inside
Vibe and select `zai-glm-5-2` to run the same agent with GLM 5.2 hosted by Mistral. This
repository does not benchmark the two models; it only makes the switch easy to try.

## Remove the environment

```bash
sbx env rm --force
```
