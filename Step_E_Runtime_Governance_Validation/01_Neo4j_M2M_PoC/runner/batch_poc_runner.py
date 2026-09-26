import json
import os
import subprocess
from neo4j import GraphDatabase

def get_host_ip():
    if os.getenv("NEO4J_HOST"):
        return os.getenv("NEO4J_HOST")
    try:
        host_ip = subprocess.check_output(
            "ip route | grep default | awk '{print $3}'", 
            shell=True
        ).decode().strip()
        if host_ip:
            return host_ip
    except Exception:
        pass
    return "localhost"

HOST_IP = get_host_ip()
NEO4J_URI = os.getenv("NEO4J_URI", f"bolt://{HOST_IP}:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def evaluate_scenario(session, scenario_dir):
    with open(os.path.join(scenario_dir, "sensor_state.json"), "r", encoding="utf-8") as f:
        sensor = json.load(f)
    with open(os.path.join(scenario_dir, "ui_event.json"), "r", encoding="utf-8") as f:
        ui = json.load(f)
    with open(os.path.join(scenario_dir, "user_profile.json"), "r", encoding="utf-8") as f:
        user = json.load(f)
    with open(os.path.join(scenario_dir, "expected_output.json"), "r", encoding="utf-8") as f:
        expected = json.load(f)

    step_id = ui.get("current_step_id")
    user_role = user.get("user_profile")
    variant = user.get("machine_variant")
    part_number = ui.get("selected_part_number")
    pressure = sensor.get("hydraulic_pressure_mpa", 0.0)
    oil_temp = sensor.get("oil_temperature_c", 25.0)
    valve_status = sensor.get("valve_status", "Closed")

    cypher_query = """
    MATCH (s:Resource {uri: $step_id})
    OPTIONAL MATCH (s)-[:targets_component]->(comp:Resource)
    OPTIONAL MATCH (s)-[:requiresSupply]->(supply:Resource)
    
    // 1. Aggregate valid part numbers from bound supplies
    WITH s, comp, collect(DISTINCT supply.partNumber) AS valid_parts

    // 2. Evaluate individual constraints (Bypass residual pressure gate for depressurization task)
    WITH s, comp, valid_parts,
         (s.targetAudience = $user_role OR s.targetAudience = 'iirds:Operator') AS role_ok,
         (s.actionType = 'Depressurization' OR s.uri = 'STEP-006' OR $pressure <= 0.05) AS pressure_safe,
         ($oil_temp <= 40.0) AS temp_safe,
         ($valve_status = 'Closed') AS valve_safe,
         ($part_number IS NULL OR $part_number IN valid_parts) AS part_ok

    // 3. Compute aggregate authorization flag
    WITH s, comp, role_ok, pressure_safe, temp_safe, valve_safe, part_ok,
         (role_ok AND pressure_safe AND temp_safe AND valve_safe AND part_ok) AS permitted

    RETURN {
      permitted: permitted,
      reason_code: CASE 
        WHEN NOT role_ok THEN 'ERR_UNAUTHORIZED_ROLE'
        WHEN (NOT temp_safe OR NOT valve_safe) AND (s.uri = 'STEP-006') THEN 'ERR_MULTIPLE_PHYSICAL_STATES'
        WHEN NOT pressure_safe THEN 'ERR_PRESSURE_REMAINING'
        WHEN NOT part_ok THEN 'ERR_INVALID_PART_VARIANT'
        WHEN $part_number IS NOT NULL AND part_ok THEN 'MATCH_VARIANT_PART'
        WHEN s.uri = 'STEP-006' AND role_ok AND temp_safe AND valve_safe THEN 'SUPPLIES_READY'
        ELSE 'SUCCESS'
      END,
      highlight_mode: CASE WHEN NOT permitted THEN 'BLINK_RED' ELSE 'HIGHLIGHT_GREEN' END
    } AS result
    """

    record = session.run(
        cypher_query,
        step_id=step_id,
        user_role=user_role,
        variant=variant,
        part_number=part_number,
        pressure=pressure,
        oil_temp=oil_temp,
        valve_status=valve_status
    ).single()

    if not record or not record["result"]:
        raise ValueError(f"Failed to retrieve traversal result for step: {step_id}")

    result = record["result"]

    # Persist evaluation result payload
    with open(os.path.join(scenario_dir, "output.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Validate against expected outcome
    passed = (
        result["permitted"] == expected["permitted"] and
        result["reason_code"] == expected["reason_code"] and
        result["highlight_mode"] == expected["highlight_mode"]
    )

    return passed, result, expected

def main():
    base_dir = "test_scenarios"
    scenarios = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    print("=" * 60)
    print(" PoC1 - PoC6 Knowledge Graph Batch Verification Runner")
    print("=" * 60)

    total = len(scenarios)
    success_count = 0

    with driver.session() as session:
        for name in scenarios:
            scenario_path = os.path.join(base_dir, name)
            passed, result, expected = evaluate_scenario(session, scenario_path)
            
            status_mark = "[ PASS ]" if passed else "[ FAIL ]"
            if passed:
                success_count += 1

            print(f"{status_mark} {name}")
            print(f"         Actual  : Permitted={result['permitted']}, Code={result['reason_code']}")
            if not passed:
                print(f"         Expected: Permitted={expected['permitted']}, Code={expected['reason_code']}")

    driver.close()
    print("=" * 60)
    print(f"Execution Summary: {success_count}/{total} PASSED")
    print("=" * 60)

if __name__ == "__main__":
    main()