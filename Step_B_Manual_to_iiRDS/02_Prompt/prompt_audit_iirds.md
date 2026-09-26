
# Role
You are an expert in the iiRDS specification, structured technical documentation, and deterministic safety quality assurance for industrial cyber-physical systems.

# Task
Perform an independent comparative audit between the source manual (`MAN-HYD-2026-01.md`) and the generated structured output (`iirds_atomic_data.json`). Evaluate the validity of atomic decomposition, the precision of attribute extraction, and compute confidence scores formatted as an audit report in JSON.

# Audit Criteria and Verification Axes

1. **TargetAudience Entitlement Verification:**
   - Verify whether classification between `iirds:Operator` and `iirds:ServiceTechnician` aligns with the source text with zero ambiguity.

2. **PhysicalState Extraction Accuracy:**
   - Confirm that all physical safety interlocks (fluid temperature, line pressure, valve position) stated in the manual are extracted into `required_physical_states` with exact numerical limits and relational operators (no omitted or hallucinated conditions).

3. **Prohibition Assertion (`prohibited_action`):**
   - Ensure that all explicit safety prohibitions and negative warnings (e.g., "strictly prohibited", "must not") are flagged with `prohibited_action: true`.

4. **Atomic Granularity Evaluation:**
   - Confirm that each node reflects atomic granularity ("one action or one decision per node") without conflating parallel operations.

5. **Node-Level Confidence Scoring (0.0 to 1.0):**
   Evaluate each `atomic_step` node against the following rubric:
   - **1.0:** All attributes (Audience, PhysicalState, ActionType, TargetComponent, Supplies) are extracted with complete fidelity.
   - **0.8 - 0.9:** Core structure is correct, but minor phrasing verbosity or slight granularity sub-optimality is detected.
   - **0.5 - 0.7:** Non-critical omissions in `required_physical_states` or slight categorization misalignment in `target_audience`.
   - **0.0 - 0.4:** Critical safety omission, misclassified role entitlement (privilege escalation hazard), or ungrounded hallucination.

# Input Files
1. Source Manual: `MAN-HYD-2026-01.md`
2. Generated Structured JSON: `iirds_atomic_data.json`

# Output Format
Output ONLY the JSON object. Do not include commentary, explanations, or conversational framing.

```json
{
  "audit_metadata": {
    "step": "Step B (Manual to iiRDS Atomic Steps)",
    "total_source_chapters": 2,
    "generated_atomic_steps": 10,
    "safety_critical_issues_found": 0,
    "overall_confidence_score": 1.0
  },
  "step_audits": [
    {
      "step_id": "STEP-006",
      "target_audience": "iirds:ServiceTechnician",
      "confidence_score": 1.0,
      "status": "PASSED",
      "checks": {
        "audience_accuracy": "PASSED",
        "physical_state_extraction": "PASSED",
        "prohibited_action_logic": "PASSED",
        "atomic_granularity": "PASSED"
      },
      "issues": []
    }
  ],
  "discrepancies_and_warnings": []
}
````