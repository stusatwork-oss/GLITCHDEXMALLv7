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
// Helper: normalize file path (basic checks only)
// NOTE: This does NOT enforce a base directory or prevent path traversal.
// Callers must implement additional security checks as needed.
// -----------------------------
function normalizeFilePath(filePath) {
  // Reject null bytes (injection technique)
  if (filePath.includes('\0')) {
    throw new Error(`Invalid path (null byte detected): ${filePath}`);
  }
  // Resolve to absolute path
  return path.resolve(filePath);
}

// -----------------------------
// Helper: read JSON file safely
// -----------------------------
function loadJSON(filePath) {
  const safePath = normalizeFilePath(filePath);
  // Only allow reading .json files
  if (!safePath.endsWith('.json')) {
    throw new Error(`Refusing to read non-JSON file: ${safePath}`);
  }
  try {
    const raw = fs.readFileSync(safePath, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error(`❌ Error reading JSON file: ${safePath}`);
    throw err;
  }
}

// -----------------------------
// Helper: write JSON pretty
// -----------------------------
function saveJSON(filePath, data) {
  const safePath = normalizeFilePath(filePath);
  // Only allow writing to .json files
  if (!safePath.endsWith('.json')) {
    throw new Error(`Refusing to write to non-JSON file: ${safePath}`);
  }
  try {
    const formatted = JSON.stringify(data, null, 2);
    fs.writeFileSync(safePath, formatted, 'utf-8');
  } catch (err) {
    console.error(`❌ Error writing JSON file: ${safePath}`);
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
// Helper: validate path is within base directory (prevent traversal)
// -----------------------------
function isPathWithinBase(basePath, filePath) {
  const resolvedBase = path.resolve(basePath) + path.sep;
  const resolvedPath = path.resolve(basePath, filePath);
  return resolvedPath.startsWith(resolvedBase);
}

// -----------------------------
// If path is folder → score all JSON files inside
// -----------------------------
function scoreFolder(folderPath) {
  const safeFolderPath = normalizeFilePath(folderPath);
  console.log(`📁 Scoring all entity JSONs in folder: ${safeFolderPath}`);

  const files = fs.readdirSync(safeFolderPath);

  const jsonFiles = files.filter(f => f.endsWith('.json'));
  if (jsonFiles.length === 0) {
    console.log(`⚠️ No JSON files found in: ${safeFolderPath}`);
    return;
  }

  jsonFiles.forEach(file => {
    // Security: reject filenames with path traversal attempts
    if (file.includes('..') || path.isAbsolute(file)) {
      console.error(`❌ Rejected unsafe filename: ${file}`);
      return;
    }
    const fullPath = path.resolve(safeFolderPath, file);
    // Security: verify resolved path stays within base folder
    if (!isPathWithinBase(safeFolderPath, file)) {
      console.error(`❌ Path traversal detected, skipping: ${file}`);
      return;
    }
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
