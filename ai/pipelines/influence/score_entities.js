/**
 * score_entities.js
 *
 * Command-line script to score one or more entity JSON files using
 * the QBIT Influence Engine (engine.js).
 *
 * Usage:
 *   node score_entities.js path/to/entity.json
 *   node score_entities.js path/to/folder/
 *
 * Output:
 *   Updates each entity JSON with computed:
 *     - power
 *     - charisma
 *     - overall
 *     - rarity
 *
 * NOTE:
 *   This script overwrites the JSON files IN PLACE.
 *   Make sure you're in a committed state before running!
 */

const fs = require('fs');
const path = require('path');

// Import the QBIT influence engine
const {
  scoreEntity
} = require('./engine.js');

// -----------------------------
// Helper: read JSON file safely
// -----------------------------
function loadJSON(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`❌ Error reading JSON file: ${filePath}`);
    throw err;
  }
}

// -----------------------------
// Helper: write JSON pretty
// -----------------------------
function saveJSON(filePath, data) {
  try {
    const formatted = JSON.stringify(data, null, 2);
    fs.writeFileSync(filePath, formatted, 'utf-8');
  } catch (err) {
    console.error(`❌ Error writing JSON file: ${filePath}`);
    throw err;
  }
}

// -----------------------------
// Score a single entity file
// -----------------------------
function scoreSingleFile(filePath) {
  console.log(`🔍 Scoring entity: ${filePath}`);

  const entitySpine = loadJSON(filePath);
  const scored = scoreEntity(entitySpine);

  saveJSON(filePath, scored);

  console.log(`✅ Updated: ${filePath}`);
}

// -----------------------------
// If path is folder → score all JSON files inside
// -----------------------------
function scoreFolder(folderPath) {
  console.log(`📁 Scoring all entity JSONs in folder: ${folderPath}`);

  const files = fs.readdirSync(folderPath);

  const jsonFiles = files.filter(f => f.endsWith('.json'));
  if (jsonFiles.length === 0) {
    console.log(`⚠️ No JSON files found in: ${folderPath}`);
    return;
  }

  jsonFiles.forEach(file => {
    const fullPath = path.join(folderPath, file);
    scoreSingleFile(fullPath);
  });

  console.log('📦 Folder scoring complete.');
}

// -----------------------------
// Main Execution
// -----------------------------
function main() {
  const target = process.argv[2];

  if (!target) {
    console.log("Usage:");
    console.log("  node score_entities.js path/to/entity.json");
    console.log("  node score_entities.js path/to/folder/");
    process.exit(1);
  }

  const resolved = path.resolve(target);
  const stats = fs.statSync(resolved);

  if (stats.isFile()) {
    scoreSingleFile(resolved);
  } else if (stats.isDirectory()) {
    scoreFolder(resolved);
  } else {
    console.error(`❌ Invalid target: ${resolved}`);
    process.exit(1);
  }
}

main();
