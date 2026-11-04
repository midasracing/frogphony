# Contributing to Frogphony

Frogphony is an early-stage educational project. Contributions that make lessons clearer, the code easier to maintain or the interface more accessible are especially useful.

## Before you start

- Check existing issues before opening a new one.
- For large features or changes to lesson structure, open an issue first to discuss the approach.
- Keep pull requests focused. Explain the problem, what changed and how you tested it.
- Do not include copyrighted recordings, illustrations or learning materials unless you have permission to contribute them under the applicable license.

## Local development

Use Node.js 22.13+.

```bash
npm install
npm run dev
```

Before requesting review, verify the production build:

```bash
npm run build
```

The project does not yet have an automated test suite. If a PR changes the lesson flow, please also describe which lessons and interactions you tested manually.

## Lesson contributions

For a new exercise, provide:

1. **Learning goal** — what the learner should understand or hear.
2. **Question and answers** — including the correct option.
3. **Explanation** — a short, accurate reason why that option is correct.
4. **Audio requirements** — whether generated tones are sufficient or a verified recording is needed.

Please use clear Polish suitable for learners. Musical accuracy and readable explanations take priority over gamification.

## Code and accessibility

- Follow the existing React and TypeScript patterns.
- Prefer accessible native controls over custom interaction where possible.
- Ensure focus states and keyboard use still work.
- Check the layout on a narrow mobile viewport.
- Keep external dependencies and bundled assets to a minimum.

## Reporting a problem

Include the page or lesson, steps to reproduce, expected behavior, actual behavior and browser/device information where relevant. For incorrect music questions, explain the theoretical issue.

## Licensing

By contributing code, you agree to license your contribution under the repository's MIT license. Visual assets and any third-party material have separate terms; read [ASSETS.md](ASSETS.md). Do not submit material you do not have the right to share.
