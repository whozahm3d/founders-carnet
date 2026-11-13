# Accessibility

Founders Carnet helps founders, talent, mentors and investors get compliance guidance, find matches, browse jobs and practice their pitch. Everyone should be able to use it and contribute to it, including people who use a keyboard instead of a mouse, a screen reader, magnification or voice control, and people who find dense text hard to read.

This document explains what we are aiming for, what we expect from contributors, how to tell us about a barrier, and what we already know is not working. If you have just hit a barrier, go straight to [Reporting accessibility issues](#reporting-accessibility-issues).

## Priorities

We want people to be able to do these things without a mouse, without relying on colour, and without needing anyone's help:

- Register, sign in, and complete a profile.
- Ask the compliance assistant a question and read the answer, including its citations, in plain language.
- Take part in pitch practice. It is written text only, so no audio or video is needed.
- Fill in forms where every field has a clear label and every error says what went wrong and how to fix it.
- Upload a resume and read the suggestions as text.
- Use the product at 200% zoom and on a small screen.

Our aspirational target is WCAG 2.2 Level AA. This is a goal, not a claim. We have not yet had the product evaluated, so we do not claim that it conforms. If we ever make a conformance claim, we will state what was evaluated, when, how, and by whom.

Right now the product is in English only. Urdu is not supported.

## Contributor expectations

Anyone changing something a user sees or hears should check the following before opening a pull request:

- Every interactive element can be reached and used with the keyboard, in a sensible order, with a visible focus indicator.
- Every form field has a label, and errors are shown in text and tied to the field they belong to.
- Meaning is never carried by colour alone, and text has enough contrast to read comfortably.
- Images that carry information have text alternatives, and decorative images are hidden from screen readers.
- The page still works at 200% zoom without scrolling sideways.
- Backend contributors: error messages returned by the API are shown to users, so write them as clear sentences, not codes alone.
- Text produced by AI features (compliance answers, readiness and pitch feedback) should be structured and in plain language.

**Evidence to include.** In the pull request description, say which screens you changed and how you checked them, for example "walked through with keyboard only" or "tested with a screen reader" (name which one). If a check does not apply, say why. Screenshots are optional.

**Automated checks.** Our CI runs frontend checks on every pull request. [TODO: name the accessibility lint or test tool here once the project adopts one.] Automated tools find only some problems, so a green check does not mean a change is accessible.

## Reporting accessibility issues

If something in Founders Carnet is hard or impossible to use, please tell us. You do not need to explain why, and you do not need to share anything about yourself.

- **GitHub:** open an issue in this repository and add the `accessibility` label.
- **Email:** [TODO: add a project contact address].

It helps if you can tell us:

- What you were trying to do.
- The page or URL where it happened.
- What happened, and what you expected instead.
- Your browser and operating system.
- Any assistive technology you use, if you want to mention it.

Screenshots or recordings are welcome but never required. A short description is enough.

### Severity

Maintainers choose the severity when they triage an issue. You do not need to.

- **Blocker:** a core task cannot be completed at all. For example, the sign-in button cannot be reached with the keyboard, or a pitch answer cannot be submitted.
- **Major:** the task can be completed, but only with great effort or a workaround. For example, form errors are not announced by a screen reader, so you have to hunt for them.
- **Minor:** an inconvenience that does not stop the task. For example, a secondary label is hard to read because of low contrast.

### How we respond

- We acknowledge a report within [TODO: confirm, for example 5 working days].
- We confirm the severity and say what we plan to do.
- Blockers are prioritised ahead of new features.
- If there is a workaround, we share it in the issue while we work on the fix.
- We post updates on the issue. If we cannot fix something soon, we say so and explain why.
- When a fix is ready, we may ask you to check it. This is optional.

## Ownership and maintenance

[TODO: name the person or role responsible for accessibility.] Until someone is named, the code owners listed in `CODEOWNERS` are responsible.

The owner:

- Triages accessibility issues.
- Checks accessibility in pull request reviews.
- Keeps this document and the known limitations below up to date.
- Reviews this document [TODO: choose a cadence, for example at each release].

When ownership changes, the outgoing owner updates this section in the same pull request and hands over any open accessibility issues.

## Supported environments

We have not yet formally tested any combination of browser, device or assistive technology. We aim for the product to work in the current versions of Chrome, Edge, Firefox and Safari, on desktop and mobile, with keyboard-only use.

We have not tested any screen reader yet. When we do, we will list each combination here, for example the screen reader, browser and operating system, along with the version and the date.

## Known limitations

We have not had an accessibility evaluation yet, so there are probably barriers we do not know about. [TODO: replace this with what has been tested once testing happens.]

Barriers we already know about:

- **Source documents.** Compliance answers cite official documents, such as laws and circulars from SECP and FBR. Answers cite the document, section and page. The source files are PDFs published by those bodies, and we do not control how accessible they are. Some may not work well with a screen reader. If you cannot read a cited passage, report it and we will try to help.
- **Resume upload.** Only PDF resumes are accepted. Scanned resumes with no selectable text may not produce suggestions. [TODO: link a tracked issue.]
- **AI-written text.** Answers and feedback are generated, so their length and structure vary and may sometimes be hard to follow. If you find an example, please report it.
- **Pitch practice is text-only.** Voice input is not available.

## Feedback and improvements

If you have ideas for improving this document or our accessibility practices, open an issue with the `accessibility` label or send a pull request. If you are reporting a barrier you have run into right now, use the [reporting process](#reporting-accessibility-issues) instead, so it is handled as a bug.
