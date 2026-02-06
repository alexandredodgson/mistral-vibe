# Project Tracking and Standards

Mistral Vibe uses specific files to track task progress, state, and architectural decisions. These files are managed by the Orchestrator's Planning and Architect modules.

## Task Tracking Files

- **`brainfile.md`**: Used for high-level planning and task tracking. The agent updates this file to keep track of what has been done and what remains to be done.
- **`STATE.md`**: Maintains the current state of the project from the agent's perspective. It helps the agent resume work effectively.
- **`DECISION_LOG.md`**: Records key technical decisions made during the project, providing a history of "why" certain paths were taken.

## Architectural Standards

Vibe encourages documenting the project's architecture using:

- **`SPEC.md`**: Contains the technical specifications and requirements. Vibe's Architect module can validate the codebase against the specs and will issue warnings if inconsistencies are found or if the file is missing/empty.
- **`ARCHITECTURE.md`**: Used for high-level architectural diagrams, often using [Mermaid](https://mermaid.js.org/) syntax.

## Orchestrator Context and Tags

The `OrchestratorMiddleware` injects special context into the agent's prompt to guide its behavior and maintain project standards. This information is wrapped in the following tags:

- **`<orchestrator_context>`**: Contains information about the current phase (e.g., `init`, `plan`, `implement`), progress percentage, and the active task.
- **`<warning>`**: Used within the context to highlight issues, such as a missing `SPEC.md`.

The agent is also instructed to use specific XML-like tags in its responses to interact with the orchestrator modules:

- **`<ai_plan>`**: Used to update the project plan in `brainfile.md`.
- **`<ai_notes>`**: Used to log observations or notes.
- **`<ai_review>`**: Used to provide a review of the completed work.

## Automated Validation

The Architect module monitors the project and can provide feedback or warnings based on the contents of these files, ensuring that development remains aligned with the intended design.
