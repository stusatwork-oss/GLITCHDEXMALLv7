from rejected_consensus import (
    ConstraintSpec,
    MorphFirmware,
    MorphJob,
    ScrapPool,
    process_morph_job,
)


def test_morph_job_applies_penalties_instead_of_failing():
    pool = ScrapPool()
    first = pool.record_rejection(
        source="dialogue_branch",
        zone_id="Z4_ARCADE",
        conditions={"cloud_min": 55},
        qbit_signature={"power": 10, "charisma": 120},
        reason="player_never_selected",
        tick_recorded=10,
    )

    job = MorphJob(
        job_id="MJ_0109",
        inputs=[first.id, "RC_004310"],
        target_zone="Z4_ARCADE",
        source_entity_id="NPC_JANITOR_07",
        morph_target={"target_class": "ANCHOR_NPC", "style_tags": ["carny"]},
        snapshots={"pre_morph_state": {"inventory": {}, "qbit_vector": {}}},
        constraints=[
            ConstraintSpec(
                constraint_id="PHYSICS_LOCAL",
                type="HARD_PHYSICS",
                priority="HIGH",
                weight=1.0,
                parameters={"max_cloud_delta": 0.5},
            ),
            ConstraintSpec(
                constraint_id="LORE_CANON_HARD",
                type="LORE_CANON",
                priority="CRITICAL",
                weight=1.5,
                parameters={"min_qbit_charisma": 500},
            ),
            ConstraintSpec(
                constraint_id="PERF_FRAME_BUDGET",
                type="PERFORMANCE_BUDGET",
                priority="HIGH",
                weight=0.8,
            ),
        ],
        morph_params={
            "intensity": 0.7,
            "randomness": 0.3,
            "max_iterations": 8,
            "max_penalty_score": 25.0,
        },
        context={
            "world_tick": 1234567,
            "zone_id": "Z4_ARCADE",
            "qbit_vector": {"COHERENCE": 0.8, "WEIRDNESS": 0.4},
            "cloud_pressure": {"LOAD": 0.3},
        },
    )

    firmware = MorphFirmware()
    result = process_morph_job(pool, firmware, job)

    assert result.consumed_inputs == [first.id]
    assert result.missing_inputs == ["RC_004310"]
    assert result.base_spec["spawn_conditions"]["zone_id"] == "Z4_ARCADE"
    assert result.base_spec["qbit_vector"]["charisma"] >= 500
    assert result.base_spec["cloud_pressure_delta"] <= 0.5
    assert result.descriptor["prototype_id"].startswith("SCRAP_MORPH_MJ_0109")
    assert result.descriptor["requires_confirmation"] is True
    assert result.descriptor["suggested_spawn_class"] == result.base_spec["base_type"]
    assert result.descriptor["stability_score"] <= 1.0
    assert result.descriptor["job_type"] == "MORPH"
    assert result.descriptor["source_entity_id"] == "NPC_JANITOR_07"
    assert result.descriptor["morph_target"]["target_class"] == "ANCHOR_NPC"
    assert result.descriptor["context"]["zone_id"] == "Z4_ARCADE"
    assert set(result.descriptor["snapshots"]["pre_morph_state"].keys()) == {
        "pose",
        "inventory",
        "relationships",
        "location",
        "firmware_stack",
        "qbit_vector",
        "cloud_pressure",
    }
    assert any(p.constraint == "min_qbit_charisma" for p in result.penalties_applied)
    assert any(p.constraint == "max_cloud_delta" for p in result.penalties_applied)
    assert any(p.constraint_type == "PERFORMANCE_BUDGET" for p in result.penalties_applied)

