# Integrating 3D (XVL), iiRDS, and Knowledge Graphs: Deterministic Runtime Governance PoC

**Repository:** [https://github.com/wakabase-n/tcworld-2026-xvl-iirds](https://github.com/wakabase-n/tcworld-2026-xvl-iirds?utm_source=gemini)

This repository provides the reference implementation for an end-to-end data pipeline that integrates **3D CAD/geometric models (XVL)**, the international technical documentation standard **iiRDS**, and **service bills of materials (sBOM / SKOS)** into a unified knowledge graph. It demonstrates **Deterministic Runtime Governance** dynamically coupled with real-time IoT sensor telemetry and operator role entitlements.

This work directly accompanies the technical article series published in _tcworld online magazine_ (2026) and the presentation at _tcworld conference 2026_ (Stuttgart, Germany).


## 1. Overview and Architecture: Transforming Manuals from "Passive Documents" into "Executable Control Engines"

In maintenance and field service operations, role-based access control (differentiating operators from qualified service engineers) and active physical interlocks (e.g., preventing disassembly during high-temperature or residual-pressure states) are safety-critical imperatives.

Traditionally, such business rules and safety gates have been hard-coded into procedural application logic (`if-else` blocks). This tight coupling introduces severe maintenance bottlenecks and compliance risks, as any technical manual revision or safety threshold update necessitates software code modifications, testing, and redeployment.

This project resolves this fundamental friction by establishing a **deterministic governance architecture that eliminates procedural if-else branching**, utilizing two complementary deployment tracks:

1. **M2M (Machine-to-Machine) Deterministic Control**: Graph-native pattern traversal via Neo4j and Cypher, returning single-millisecond boolean and status signals (Validated: **6/6 PASSED**).
2. **HMI (Human-Machine Interface) Dynamic Guidance**: A zero-setup, zero-hallucination interactive playground powered by Google Notebook (formerly NotebookLM), leveraging structural graph guardrails for conversational verification (Validated: **10/10 PASSED**).

<img width="1252" height="921" alt="image" src="https://github.com/user-attachments/assets/b13b0a3e-cb12-48eb-97fb-a4aa6a1dffd0" />


## 2. Repository Layout

The pipeline is organized into two stages: **Knowledge Pipeline & Foundation (Steps A–D)** and **Runtime Governance Validation (Steps E-1 & E-2)**.


```
.
├── Step_A_sBOM_to_SKOS/                 # Step A: Transform CSV sBOM into W3C SKOS Concept Scheme (JSON-LD)
│   ├── 01_Input/
│   ├── 02_Prompt/
│   ├── 03_Output/
│   ├── 04_Audit/                        # Independent deterministic audit (Score: 1.0)
│   └── README.md
├── Step_B_Manual_to_iiRDS/              # Step B: Decompose narrative manual into iiRDS Atomic Step JSON
│   ├── 01_Input/
│   ├── 02_Prompt/
│   ├── 03_Output/
│   ├── 04_Audit/                        # Independent 5-axis audit (Score: 1.0)
│   └── README.md
├── Step_C_Integration_Binding/          # Step C: SKOS-centric semantic binding (3D XVL ✕ iiRDS)
│   ├── 01_Input/
│   ├── 02_Prompt/
│   ├── 03_Output/
│   ├── 04_Audit/                        # Independent referential integrity audit (Score: 1.0)
│   └── README.md
├── Step_D_Graph_Engine_Setup/           # Step D: Neo4j Graph DB setup & deployment (TBox/ABox integration)
│   ├── 01_Input/
│   ├── 02_TBox_Setup/                   # neosemantics initialization & official ontology import
│   ├── 03_ABox_Import/                  # ABox instance data ingestion scripts (Python / Cypher)
│   ├── 04_Verification/                 # Graph structural integrity Cypher queries
│   └── README.md
└── Step_E_Runtime_Governance_Validation/ # Step E: Dual-track runtime validation
    ├── 01_Neo4j_M2M_PoC/                # M2M deterministic batch test runner (6/6 PASSED)
    │   ├── scenarios/
    │   ├── runner/
    │   └── README.md
    └── 02_GoogleNotebook_ZeroSetup/     # HMI zero-setup interactive playground (10/10 PASSED)
        ├── inputs/                      # Source texts & SPO triple datasets
        ├── prompts/                     # System instructions (Constitutional guardrails)
        ├── docs/                        # Complete transcripts of all 10 verified test cases
        └── README.md
```


## 3. End-to-End Pipeline Overview

### Part 1: Knowledge Pipeline & Foundation (Steps A–D)

- **[Step A: sBOM Transformation to SKOS Concept Scheme](./Step_A_sBOM_to_SKOS/)**
    Converts flat CSV spare parts catalogs into a W3C-compliant SKOS Concept Scheme (JSON-LD). Automatically derives `skos:altLabel` aliases to capture field jargon and establishes `skos:broader` hierarchical links to 3D geometry nodes.
    
    _Audit Validation:_ **Score: 1.0 (PASSED)**
    
- **[Step B: Manual Decomposition into iiRDS Atomic Steps](./Step_B_Manual_to_iiRDS/)**
    Disassembles unstructured documentation into self-contained "one-operation, one-assertion" execution nodes. Structures operator entitlement constraints (`iirds:TargetAudience`), sensor prerequisites (`ext:PhysicalState`), and prohibition directives (`prohibited_action`).
    
    _Audit Validation:_ **Score: 1.0 (PASSED)**
    
- **[Step C: Multi-Modal Semantic Binding via SKOS Hub](./Step_C_Integration_Binding/)**
    Employs the SKOS concept dictionary as a semantic hub to resolve textual part mentions into qualified URIs (`ex:Part/FLT-X200-HD`) and binds procedural actions directly to 3D geometric node IDs (`COMP-HOUSING-01`) without mutating source assets.
    
    _Audit Validation:_ **Score: 1.0 (PASSED, 0 broken references)**
    
- **[Step D: Graph Engine Deployment (Neo4j & neosemantics)](./Step_D_Graph_Engine_Setup/)**
    Deploys the schema layer (TBox: 380 nodes, 532 relationships) using `neosemantics (n10s)` and instantiates the compiled ABox instance data. Replaces RDB relational JOIN overhead with constant-time Index-Free Adjacency traversals.

### Part 2: Runtime Governance Validation (Step E)

The unified graph substrate is subjected to rigorous validation across two operational paradigms:
#### 1. [M2M Deterministic Execution (Neo4j / Cypher)](./Step_E_Runtime_Governance_Validation/01_Neo4j_M2M_PoC/)
Evaluates dynamic inputs across three decoupled telemetry streams (live IoT sensor states, UI viewport picking events, and user entitlement profiles). Cypher pattern traversals execute all safety, variant, and authorization logic without application-level if-statements.

_Batch Test Result:_ **6/6 PASSED**

- **Stage 1: Core Safety Governance (Featured in _tcworld online magazine_)**
    
    - **PoC1 (Entitlement Interlock - Negative):** Rejects unauthorized operator disassembly with `ERR_UNAUTHORIZED_ROLE` and triggers a 3D red flash signal (`BLINK_RED`).
    - **PoC2 (Sensor Interlock - Negative):** Prevents technician execution while line pressure remains at 0.5 MPa (`ERR_PRESSURE_REMAINING`), routing to the depressurization procedure.
    - **PoC3 (Safety Clearance - Positive):** Verifies safe conditions (residual pressure $\le$ 0.02 MPa), returning `SUCCESS` and highlighting the target component (`HIGHLIGHT_GREEN`).
        
- **Stage 2: Enterprise Complexity & Physical Multi-Interlocks (Featured at _tcworld conference_)**
    
    - **PoC4 (Variant-Specific Part Resolution):** Deterministically isolates the exact filter replacement element (`FLT-STD-01`) for the base `SP-X100` model.
    - **PoC5 (Prerequisite Tooling & PPE Gate):** Validates mandatory specialty tools (`TOOL-A`) and personal protective equipment prior to task initiation.
    - **PoC6 (Compound Physical Interlock):** Identifies multiple hazard states concurrently (0.5 MPa pressure and 65°C oil temperature), generating an aggregate safety override (`ERR_MULTIPLE_PHYSICAL_STATES`).

#### 2. [Zero-Setup Conversational Verification (Google Notebook / GraphRAG)](./Step_E_Runtime_Governance_Validation/02_GoogleNotebook_ZeroSetup/)
Provides browser-native reproduction of conversational governance without requiring local database or runtime infrastructure.

_Benchmark Result:_ **10/10 PASSED**

- **Complete Hallucination Suppression:** Rejects procedures and unverified substitute tooling (e.g., standard adjustable wrenches) described in narrative prose if explicit graph relationships do not exist in the triple dataset (Cases 1-2, 4-1, 4-2).
- **Dynamic Sensor Evaluation:** Evaluates natural language telemetry inputs (e.g., "current temperature is 55°C, pressure is 0.02 MPa") as dynamic conditional statements, identifying temperature threshold violations and withholding clearance (Cases 6-1 through 6-3).


## 4. Verification and Reproduction

### Track A: Zero-Setup Interactive Verification (Recommended)

Verify semantic governance in under five minutes directly within your browser via Google Notebook (formerly NotebookLM):

1. Access <a href="https://notebook.google.com/">Google Notebook</a> and create a new project notebook.
    
2. Upload the two provided dataset files from `Step_E_Runtime_Governance_Validation/02_GoogleNotebook_ZeroSetup/inputs/`:
    - `Source1_PoC_manual_AtomicData.txt` (Narrative procedural text)
    - `Source2_PoC_manual_KnowledgeGraph.txt` (Structured Subject-Predicate-Object triples)
3. Copy the system prompt from `prompts/notebook_system_instructions.md` into the Notebook Guide settings.
4. Execute test prompts from `docs/test_cases_and_dialog_logs.md` (e.g., _"As an operator, can I disassemble the housing?"_) to observe immediate, evidence-grounded responses governed by graph constraints.

### Track B: Full-Stack M2M Batch Execution (Reference Implementation)

Access the deterministic execution scripts and batch runner configured for integration with PLCs and Web3D (XVL) runtimes.
- **Audit Logs & Execution Traces:**
    The full console log verifying complete test execution (6/6 PASSED) is available at:
`Step_E_Runtime_Governance_Validation/01_Neo4j_M2M_PoC/Evidence/batch_test_results.log`
    
- **Local Reproduction Prerequisites:**
    Running the live Cypher runner locally requires standard graph database infrastructure:
    - Neo4j Database (v5.x)
    - APOC and neosemantics (n10s) plugins enabled
    - Active Bolt protocol endpoint (Port 7687)
    - Python virtual environment configured with the official `neo4j` driver


## 5. References and Conference Presentations

### LinkedIn Technical Series

For architectural rationales, theoretical foundations, and implementation methodologies, consult the accompanying three-part article series:

1. **Part 1: [The Boundary between Dynamic Guidance and Machine Safety: Defining Constitutional Controls for AI in Technical Documentation](https://www.linkedin.com/pulse/boundary-between-dynamic-guidance-machine-safety-defining-%E5%A4%8F%E6%A8%B9-%E8%8B%A5%E6%9E%97-jxmdf/?utm_source=gemini)**
    
    - Defining the demarcation line between dynamic user assistance and deterministic machine safety via constitutional graph controls.
        
2. **Part 2: [Mediating the Boundary between Reality and Inference: What Layer Bridges the Physical-Digital Gap?](https://www.linkedin.com/pulse/mediating-boundary-between-reality-inference-what-layer-%E5%A4%8F%E6%A8%B9-%E8%8B%A5%E6%9E%97-ms4jc/?utm_source=gemini)**
    
    - Reconciling physical IoT telemetry with generative inference through a decoupled, three-tier architecture (Data, Evaluation, Action).
        
3. **Part 3: [From Document-Centric IA to Asset-Aligned Determinism: Implementing Knowledge Graphs with iiRDS and Neo4j](https://www.linkedin.com/pulse/from-document-centric-ia-asset-aligned-determinism-implementing-%E5%A4%8F%E6%A8%B9-%E8%8B%A5%E6%9E%97-wntcc/?utm_source=gemini)**
        

### Conference Presentations

- **tcworld conference 2026 (Stuttgart, Germany)**:
    - **Session:** [iiRDS-Based Agents: Steered Timing of Safety-Related Information Delivery](https://tcworldconference.tekom.de/program/detail/iirds-based-agents-steered-timing-of-safety-related-information-delivery?utm_source=gemini)
    - **Presenters:** Natsuki Wakabayashi (ISE), Dr. Harald Stadlbauer (Ninefeb Technical Communication GmbH)
        
- **JTCA TC Symposium 2026 (Tokyo, Japan)**:
    -  **[26-SSD01] Synchronizing 3D Geometry with Technical Knowledge: Breathing New Life into Static Documentation**
       _Transforming Content into Actionable Field Data via XVL and iiRDS Integration_ [https://jtca.org/sessions/2026/37829/](https://jtca.org/sessions/2026/37829/?utm_source=gemini)
   

## 🏷️ Trademarks & Acknowledgments

- **Project Collaboration:** The proof-of-concept and architectural implementations presented in this repository were conducted in close collaboration with **Lattice Technology Co., Ltd.**, who provided the foundational XVL 3D lightweight models and technical domain insights.
- **About XVL:** XVL is a 3D lightweight data technology developed by Lattice Technology Co., Ltd. with world-class 3D performance. XVL is a registered trademark of Lattice Technology Co., Ltd.
## 📜 License & Citation

This repository, along with all its structural assets, prompts, ontology models, Cypher scripts, and sample verification payloads, is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

### 🚀 Hands-on Sandbox Policy: Feel Free to Clone and Experiment!

We enthusiastically encourage engineers, information architects, researchers, and technical communicators to freely clone, adapt, and run these assets within your local development sandboxes and research environments. 

If this end-to-end implementation helps advance your practical understanding of **iiRDS**, **W3C SKOS**, **3D-driven technical documentation (XVL)**, and **GraphRAG governance**, this repository has achieved its primary goal. Concrete prototyping is the fastest path toward next-generation intelligent information architectures.

---

### ⚠️ Critical Disclaimer for Industrial and Commercial Deployment

While local experimentation and educational research are fully encouraged, please note that all datasets, graph bindings, and Cypher evaluation rules in this repository are provided **strictly as proof-of-concept (PoC) references**. They are constructed to demonstrate architectural feasibility with deep respect for:
- The **iiRDS Standard** managed by the [iiRDS Consortium / tekom](https://iirds.org/).
- The **W3C SKOS (Simple Knowledge Organization System)** recommendation.
- 3D manufacturing communication architectures utilizing lightweight 3D formats (such as XVL).

If your organization intends to engineer or deploy 3D-integrated knowledge graphs, automated interlocks, or digital twins in production, commercial, or safety-critical industrial environments, you must:

1. **Consult Official Specifications:** Always refer to the definitive standards, schemas, and governance rules published by the official standards bodies.
2. **Architect Independent Safety Interlocks:** Do not copy-paste these sample SP-X series payloads, threshold values (e.g., pressure, temperature limits), or graph traversal queries directly into production machinery. Safety-critical interlocks must always be engineered and validated in accordance with rigorous product safety regulations, ISO/IEC standards, and institutional product liability (PL) compliance protocols.
3. **No Warranty:** This software and documentation are provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or operational safety.

---

### 📖 How to Cite

If you reference, build upon, or utilize this architecture in your research, academic publications, or conference presentations, please use the following citation format:

```bibtex
@misc{wakabayashi2026_xvl_iirds,
  author       = {Natsuki Wakabayashi},
  title        = {Bridging 3D Geometry and Standardized Knowledge Graphs: Deterministic Safety Interlocks and Dynamic Guidance via XVL and iiRDS},
  year         = {2026},
  publisher    = {GitHub},
　howpublished = {\url{https://github.com/wakabase-n/tcworld-2026-xvl-iirds}},
  note         = {Presented at tcworld conference 2026 / JTCA TC Symposium 2026}
}
