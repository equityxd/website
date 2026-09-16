# -*- coding: utf-8 -*-
"""
CV Builder — LLM-Driven Generation Engine (Option B)
=====================================================
Turns a collected session (base CV + JD + manifest) into a full application
package by driving an LLM (pi) to generate the documents described by the
per-session manifest.

The previous pipeline relied on hard-coded, Doyen-specific text. This package
models the *intelligence* instead: it encodes the three-phase method
(Phase 1 recruiter/ATS audit → Phase 2 per-bullet rewrite → Phase 3 final CV)
and hands it to the LLM, which writes every deliverable to its folder.

Design goals:
  * Truthfulness first — the LLM is instructed to only rephrase facts already
    in the base CV plus the JD; nothing is invented.
  * Deterministic plumbing — we build the prompt and orchestrate the run; the
    creative/content decisions stay with the model.
  * Reusable for ANY JD (not a single hard-coded company).

Entry point:
    from generation.engine import run_generation
    run_generation(jd_path=..., on_progress=lambda m: ...)
"""

__all__ = ["engine"]
