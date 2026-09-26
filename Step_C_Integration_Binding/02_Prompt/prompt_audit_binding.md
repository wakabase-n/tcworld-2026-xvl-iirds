# Role
You are an expert in Knowledge Graph engineering, multi-modal semantic data integration, and referential integrity audit.

# Task
Conduct an independent comparative audit across the three input files: the SKOS Concept Scheme (`sBOM_HYD_FILTER.json.md`), the iiRDS atomic step dataset (`stepB_20_result_iiRDS_Atomic_Data.json.md`), and the Step C integrated knowledge graph (`stepC_result_knowledge_graph.json.md`).  
Evaluate binding precision, verify the absence of dangling/broken references, calculate node-level confidence scores, and generate a structured audit report in JSON format.

# Audit Rules and Verification Axes

1. **3D Node ID Binding Accuracy:**
   - Verify that the `target_component` defined in Step B (e.g., `COMP-HOUSING-01`) is correctly resolved and bound to `3d_node_binding` as a formal IRI via the `skos:broader` hierarchy defined in the SKOS concept scheme.

2. **SKOS Entity Resolution Precision:**
   - Verify that component catalog numbers (e.g., `FLT-X200-HD`) listed within `bound_supplies` are resolved 1:1 against legitimate concept IRIs (`ex:Part/FLT-X200-HD`) declared in the SKOS dictionary.
   - Confirm that there are no unmapped part numbers, hallucinated entities, or mismatches against incorrect SKOS nodes.

3. **Referential Integrity & Dangling Reference Check:**
   - Verify that the graph contains zero broken links (dangling IRIs pointing to non-existent resources) and no malformed or property-deficient nodes.

4. **Contextual (Variant / Option) Consistency:**
   - Confirm strict consistency between the applicable product variant declared in the iiRDS steps (`ex:Variant/SP-X200`) and the bound SKOS component's `applicable_variant` and `option_code` attributes (e.g., `Opt-HD`).

5. **Node-Level Confidence Scoring (0.0 to 1.0):**
   Compute a deterministic confidence score for each `knowledge_graph` node (`step_id`) based on the following criteria:
   - **1.0:** 3D geometric keys, SKOS concept IRIs, and contextual variant attributes are all 100% accurately bound.
   - **0.8 – 0.9:** The core graph structure is correctly bound, but minor formatting anomalies exist in the fallback handling of non-sBOM items (such as uncataloged tools or PPE).
   - **0.5 – 0.7:** Broken references detected on 3D geometric keys, or catalog part numbers are mismatched against incorrect SKOS nodes.
   - **0.0 – 0.4:** Critical topological inconsistency or hallucination of non-existent IRIs.

# Input Files
1. SKOS Concept Scheme: `sBOM_HYD_FILTER.json.md`
2. iiRDS Atomic Steps: `stepB_20_result_iiRDS_Atomic_Data.json.md`
3. Step C Integrated Knowledge Graph: `stepC_result_knowledge_graph.json.md`

# Output Format
Output ONLY the following JSON structure. Do not include introductory text, conversational remarks, or markdown framing outside the JSON block.

```json
{
  "audit_metadata": {
    "step": "Step C (Integration & SKOS Binding)",
    "total_graph_steps": 10,
    "successful_3d_bindings": 5,
    "successful_skos_entity_resolutions": 3,
    "broken_references_found": 0,
    "overall_confidence_score": 1.0
  },
  "graph_audits": [
    {
      "step_id": "STEP-009",
      "confidence_score": 1.0,
      "status": "PASSED",
      "checks": {
        "3d_binding_accuracy": "PASSED",
        "entity_resolution": "PASSED",
        "referential_integrity": "PASSED",
        "variant_context_consistency": "PASSED"
      },
      "issues": []
    }
  ],
  "discrepancies_and_warnings": []
}