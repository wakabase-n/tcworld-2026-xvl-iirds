import json
import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "iirds_3d_poc")


def import_atomic_data(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        for step in data.get("knowledge_graph", []):
            step_id = step["step_id"]

            # 1. Instantiate AtomicStep nodes and attach core properties
            session.run(
                """
                MERGE (s:Resource {uri: $step_id})
                SET s.prefLabel = $description,
                    s.chapter = $chapter,
                    s.targetAudience = $target_audience,
                    s.actionType = $action_type,
                    s.prohibitedAction = $prohibited_action
                """,
                step_id=step_id,
                description=step["description"],
                chapter=step["chapter"],
                target_audience=step["target_audience"],
                action_type=step["action_type"],
                prohibited_action=step["prohibited_action"],
            )

            # 2. Establish relationship to 3D geometric components
            if step.get("3d_node_binding"):
                comp_iri = step["3d_node_binding"]["iri"]
                session.run(
                    """
                    MERGE (s:Resource {uri: $step_id})
                    MERGE (c:Resource {uri: $comp_iri})
                    ON CREATE SET c.componentId = $comp_id
                    MERGE (s)-[:targets_component]->(c)
                    """,
                    step_id=step_id,
                    comp_iri=comp_iri,
                    comp_id=step["3d_node_binding"]["component_id"],
                )

            # 3. Establish relationships to required physical states (Interlocks: Pressure, Temp, Valve)
            for state in (
                step.get("preconditions", {}).get("required_physical_states", [])
            ):
                cond_uri = f"ex:Condition/{state['parameter']}_{state['condition'].replace(' ', '')}"
                session.run(
                    """
                    MERGE (s:Resource {uri: $step_id})
                    MERGE (cond:Resource {uri: $cond_uri})
                    SET cond.parameter = $param,
                        cond.condition = $cond,
                        cond.sensorType = $sensor_type
                    MERGE (s)-[:hasPhysicalState]->(cond)
                    """,
                    step_id=step_id,
                    cond_uri=cond_uri,
                    param=state["parameter"],
                    cond=state["condition"],
                    sensor_type=state["sensor_type"],
                )

            # 4. Establish relationships to supplies and tooling (Tool, Component, PPE)
            for supply in step.get("bound_supplies", []):
                supply_uri = (
                    supply.get("skos_concept_iri")
                    or f"ex:Supply/{supply['pref_label']}"
                )
                session.run(
                    """
                    MERGE (s:Resource {uri: $step_id})
                    MERGE (sup:Resource {uri: $supply_uri})
                    SET sup.prefLabel = $label,
                        sup.supplyType = $supply_type,
                        sup.partNumber = $part_number
                    MERGE (s)-[:requiresSupply]->(sup)
                    """,
                    step_id=step_id,
                    supply_uri=supply_uri,
                    label=supply["pref_label"],
                    supply_type=supply["supply_type"],
                    part_number=supply.get("part_number"),
                )

    driver.close()
    print("[SUCCESS] Batch ingestion of iiRDS Atomic Data completed successfully.")


if __name__ == "__main__":
    import_atomic_data("resources/PoC_manual_AtomicData.json")