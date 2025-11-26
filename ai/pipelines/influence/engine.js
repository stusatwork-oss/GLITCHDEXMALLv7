/**
 * QBIT Influence Engine (Neutralized)
 *
 * Portable scoring engine for any entity that needs:
 *  - power        → structural / systemic leverage
 *  - charisma     → attention / resonance / engagement
 *  - overall      → combined influence score
 *  - rarity       → tier label based on overall
 *
 * Expected input shape:
 *
 *  entity = {
 *    id: "leisurely-leon",
 *    name: "Leisurely Leon",
 *    role: "Primary" | "Secondary",
 *    type: "npc" | "zone" | "artifact" | "anomaly" | "org" | ...,
 *    metrics: {
 *      resonanceScore:   Number,  // 0–100
 *      grassrootsSupport:Number,  // count (0+)
 *      audienceSize:     Number,  // 0+
 *      deepViewCount:    Number,  // 0+
 *      engagementScore:  Number,  // 0–100
 *      referenceCount:   Number,  // 0+
 *      trustScore:       Number,  // 0–100
 *
 *      backingVolume:    Number,  // "big leverage", e.g., budget / feed
 *      resourcePool:     Number,  // mass, inventory, stored energy
 *      networkReach:     Number   // # of zones / systems affected
 *    }
 *  }
 *
 * All metrics are optional; sensible defaults are applied.
 */

/**
 * Calculate the Charisma score for an entity.
 * Charisma ≈ how much attention / emotional pull / narrative gravity it has.
 *
 * @param {Object} metrics
 * @returns {number} charisma score in [0, 3000]
 */
function calculateCharisma(metrics = {}) {
  // Neutral baseline if metrics are unusable
  if (metrics.error) return 500;

  let charisma = 0;

  const resonanceScore   = metrics.resonanceScore   ?? 30;     // 0–100
  const grassrootsSupport= metrics.grassrootsSupport?? 10_000; // 0–10M
  const audienceSize     = metrics.audienceSize     ?? 1_000;  // >0
  const deepViewCount    = metrics.deepViewCount    ?? 100_000;// 0–50M
  const engagementScore  = metrics.engagementScore  ?? 20;     // 0–100
  const referenceCount   = metrics.referenceCount   ?? 50;     // 0–5000
  const trustScore       = metrics.trustScore       ?? 50;     // 0–100

  // 1) Resonance / approval (0–100 → 0–600, capped)
  charisma += Math.min((resonanceScore / 100) * 600, 600);

  // 2) Grassroots support (0–10M → 0–600, capped)
  charisma += Math.min((grassrootsSupport / 10_000_000) * 600, 600);

  // 3) Audience size (log10 scaling to avoid huge follower inflation, capped)
  charisma += Math.min(Math.log10(audienceSize) * 70, 450);

  // 4) Deep attention / time spent (0–50M → 0–600, capped at 450)
  charisma += Math.min((deepViewCount / 50_000_000) * 600, 450);

  // 5) Engagement (0–100 → 0–400, capped at 300)
  charisma += Math.min((engagementScore / 100) * 400, 300);

  // 6) References + trust combined
  const referenceComponent = (referenceCount / 5000) * 300;
  const trustComponent     = (trustScore / 100) * 300;
  charisma += Math.min(referenceComponent + trustComponent, 300);

  // Global cap
  return Math.round(Math.min(charisma, 3000));
}

/**
 * Calculate the Power score for an entity.
 * Power ≈ structural leverage, systemic weight, ability to move things.
 *
 * @param {Object} entity  - must include .role ("Primary" | "Secondary")
 * @param {Object} metrics
 * @returns {number} power score in [0, 3000]
 */
function calculatePower(entity = {}, metrics = {}) {
  if (metrics.error) return 500;

  const role = entity.role || "Secondary";

  let power = 0;

  const backingVolume = metrics.backingVolume ?? 100_000;       // 0–100M
  const resourcePool  = metrics.resourcePool  ?? 1_000_000;     // 0–250B
  const networkReach  = metrics.networkReach  ?? 10;            // 0–100

  if (role === "Primary") {
    // Primary actors: bosses, prime anomalies, major zones, major NPCs.
    power += Math.min((backingVolume / 100_000_000) * 600, 600);

    // Seniority / legacy fuzz – placeholder for “been here a long time”.
    power += Math.random() * 1000;

    // Rare leadership spark (+500 about 20% of the time).
    if (Math.random() > 0.8) {
      power += 500;
    }
  } else {
    // Secondary actors: artifacts, support entities, background anomalies.
    power += Math.min((resourcePool / 250_000_000_000) * 1500, 1500);
    power += Math.min((networkReach / 100) * 1000, 1000);
  }

  return Math.round(Math.min(power, 3000));
}

/**
 * Determine rarity band from overall influence.
 *
 * @param {number} overall - expected range [0, 6000]
 * @returns {"Legendary"|"Epic"|"Rare"|"Common"}
 */
function determineRarity(overall) {
  if (overall >= 5200) return "Legendary";
  if (overall >= 4400) return "Epic";
  if (overall >= 3600) return "Rare";
  return "Common";
}

/**
 * Score a single entity spine.
 *
 * @param {Object} entitySpine - includes .metrics and .role
 * @returns {Object} new entity object with .computed = { power, charisma, overall, rarity }
 */
function scoreEntity(entitySpine) {
  if (!entitySpine || typeof entitySpine !== "object") {
    throw new Error("scoreEntity: entitySpine must be an object");
  }

  const metrics = entitySpine.metrics || {};

  const power    = calculatePower(entitySpine, metrics);
  const charisma = calculateCharisma(metrics);
  const overall  = power + charisma;
  const rarity   = determineRarity(overall);

  return {
    ...entitySpine,
    computed: {
      power,
      charisma,
      overall,
      rarity
    }
  };
}

/**
 * Score an array of entity spines.
 *
 * @param {Array<Object>} entities
 * @returns {Array<Object>} scored entities
 */
function scoreEntities(entities) {
  if (!Array.isArray(entities)) {
    throw new Error("scoreEntities: entities must be an array");
  }
  return entities.map(scoreEntity);
}

// CommonJS export (Node, tooling)
module.exports = {
  calculateCharisma,
  calculatePower,
  determineRarity,
  scoreEntity,
  scoreEntities
};

// If you ever want ESM style instead, you can swap to:
// export { calculateCharisma, calculatePower, determineRarity, scoreEntity, scoreEntities };
