---
name: advisor-launch
description: Run the Anywhere Advisor interview-to-asset pipeline for one financial-advisor client. Use when the user says "run advisor-launch for <client>", "start a new advisor", "build the next stage for <client>", or asks to turn an advisor interview into a knowledge base, offer, assessments, webinars, website, funnel, book, or KDP files.
---

# Advisor Launch

Builds an advisor's marketing assets one stage at a time, from their interview to a published book. Every asset exists to **book appointments**.

## Layout
- `stages/NN-name/`: master instructions and templates for each stage. **Read the stage's README.md before building it.**
- `clients/<slug>/NN-name/`: that client's outputs for the stage.
- `compliance/checklist.md`: run on every public-facing output.

## Procedure
1. **Find the client.** If `clients/<slug>/` doesn't exist, copy `clients/_example/` to it and ask for the interview transcript.
2. **Check progress.** A stage is done when its client folder holds the outputs its README lists. Report a one-line status for each stage.
3. **Build the next stage only**, unless the user names a different one. Earlier stages must be done first. If a required input is missing, say which one.
4. If a stage's README says **Not built yet**, tell the user that its template still needs designing and offer to design it with them before producing client output.
5. **Write in the advisor's voice**, using their verbatim phrases from the profile and knowledge base. Never invent credentials, numbers, client stories, or testimonials. Mark anything you inferred.
6. **Compliance pass:** for public-facing assets, check against `compliance/checklist.md` and list any flags at the end of the output file. Remind the user the advisor's compliance approver must sign off.
7. Finish by stating what was produced, what's open (`gaps.md`), and the next stage.
