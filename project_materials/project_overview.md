# Spectrum — project overview

## Problem

Many parental-control products emphasize monitoring and restriction. Teens may respond by hiding activity, which can make it harder to ask for help when they encounter grooming, cyberbullying, coercion, or other harmful behavior.

## Solution

Spectrum is a teen-first AI conversation companion. A young person voluntarily pastes a text exchange. An LLM looks for evidence of grooming patterns, cyberbullying, emotional manipulation, and age-inappropriate requests, then returns a rough risk indicator and specific excerpts. Each flag gets a plain-language explanation and an optional boundary suggestion. A teen may prepare and edit a support summary for a trusted adult; nothing is sent automatically.

## Target users

- **Primary:** Teenagers who want a private, low-friction way to make sense of a concerning online interaction.
- **Support network:** Parents, counselors, educators, or other trusted adults whom a teen chooses to involve.
- **Demo audience:** Child-safety practitioners and judges evaluating youth-centered AI safety tools.

## MVP

- Streamlit interface for pasted conversation text.
- Structured LLM output with risk score, evidence-backed red flags, explanations, boundaries, and optional next steps.
- Synthetic grooming, cyberbullying, and benign scenarios for demonstration.
- Editable, user-controlled summary draft and digital-literacy guidance.
- No account monitoring, database, or automatic escalation.

## Intended impact

Spectrum aims to make safety guidance easier to understand and help-seeking easier to initiate. It treats a teen as the decision-maker and frames safety as literacy and support rather than surveillance. The demo’s benign case also makes false-positive restraint visible.

## Success measures for a pilot

- Teens can explain why a flagged message may be concerning and identify at least one next step.
- Teens report that the tone feels respectful and that they understand what will be shared.
- In scenario evaluations, high-risk examples receive evidence-based flags while benign conversations remain low concern.
- A trusted adult can use a teen-approved summary to begin a supportive conversation.

These are intended pilot measures, not results already demonstrated. A real deployment would need youth co-design, privacy review, safeguarding expertise, model evaluation across diverse language and contexts, and careful handling of urgent situations.
