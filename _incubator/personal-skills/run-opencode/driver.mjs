#!/usr/bin/env node
// driver.mjs — read-only health-check / inventory harness for an OpenCode + oh-my-openagent install.
// Usage:
//   node driver.mjs            # full report (config dir, versions, agents, categories, update status)
//   node driver.mjs backup     # copy live config into agent-config-backups/<YYYY-MM-DD>/ (the only write action)
//
// Everything except `backup` is read-only. It NEVER installs, updates, or edits your config.
// Cross-platform (Windows / macOS / Linux). Requires only Node + a reachable `opencode` on PATH (optional).

import { existsSync, readFileSync, writeFileSync, readdirSync, mkdirSync, copyFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { execSync } from "node:child_process";

const C = { dim: "\x1b[2m", cyan: "\x1b[36m", yellow: "\x1b[33m", green: "\x1b[32m", red: "\x1b[31m", reset: "\x1b[0m", bold: "\x1b[1m" };
const c = (k, s) => `${C[k]}${s}${C.reset}`;

// --- locate the user-level OpenCode config dir (precedence: APPDATA on Windows, then ~/.config/opencode) ---
function findConfigDir() {
  const candidates = [];
  if (process.env.APPDATA) candidates.push(join(process.env.APPDATA, "opencode"));
  candidates.push(join(homedir(), ".config", "opencode"));
  for (const d of candidates) {
    if (existsSync(join(d, "opencode.json")) || existsSync(join(d, "oh-my-openagent.json")) || existsSync(join(d, "oh-my-openagent.jsonc"))) return d;
  }
  return candidates.find(existsSync) ?? candidates[candidates.length - 1];
}

function readJsonc(path) {
  if (!existsSync(path)) return null;
  const raw = readFileSync(path, "utf8");
  // strip UTF-8 BOM (PowerShell-written files have one) + tolerate // and /* */ comments + trailing commas (jsonc)
  const stripped = raw.replace(/^﻿/, "").replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|[^:])\/\/.*$/gm, "$1").replace(/,(\s*[}\]])/g, "$1");
  try { return { ok: true, data: JSON.parse(stripped), raw }; }
  catch (e) { return { ok: false, error: e.message, raw }; }
}

function tryExec(cmd, args) {
  // args are all hardcoded literals (no user input) -> safe to build a command string and avoid the
  // child_process shell-args deprecation warning while still resolving .cmd shims on Windows.
  try { return execSync([cmd, ...args].join(" "), { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(); }
  catch { return null; }
}

function pickModel(entry) {
  if (!entry || typeof entry !== "object") return "—";
  const eff = entry.variant ? `(${entry.variant})` : entry.reasoningEffort ? `[${entry.reasoningEffort}]` : "";
  return `${entry.model ?? "?"} ${eff}`.trim();
}
function fb(entry) {
  const a = entry?.fallback_models;
  if (!Array.isArray(a) || !a.length) return "";
  return a.map((m) => (typeof m === "string" ? m : pickModel(m))).join(" → ");
}

const CFG = findConfigDir();
const OMA_JSON = existsSync(join(CFG, "oh-my-openagent.jsonc")) ? join(CFG, "oh-my-openagent.jsonc") : join(CFG, "oh-my-openagent.json");

// --- profile action: swap agents+categories blocks between saved profiles (openai | cheap) ---
if (process.argv[2] === "profile") {
  const name = process.argv[3];
  const profPath = name && join(CFG, "profiles", `${name}.json`);
  if (!name || !existsSync(profPath)) {
    const avail = existsSync(join(CFG, "profiles")) ? readdirSync(join(CFG, "profiles")).filter((f) => f.endsWith(".json")).map((f) => f.replace(/\.json$/, "")) : [];
    const cur = readJsonc(OMA_JSON)?.data;
    const sis = cur?.agents?.sisyphus?.model ?? "?";
    console.log(c("bold", "OpenCode config profiles"));
    console.log(`  current sisyphus primary: ${c("cyan", sis)}  ${/openai/.test(sis) ? c("yellow", "(looks like: openai)") : c("green", "(looks like: cheap/non-openai)")}`);
    console.log(`  available: ${c("cyan", avail.join(", ") || "(none — run build-profiles.mjs)")}`);
    console.log(c("dim", `  switch with: node driver.mjs profile <name>`));
    process.exit(name ? 1 : 0);
  }
  // backup first
  const d = new Date().toISOString().slice(0, 10);
  const dest = join(CFG, "agent-config-backups", d);
  mkdirSync(dest, { recursive: true });
  if (existsSync(OMA_JSON)) copyFileSync(OMA_JSON, join(dest, `oh-my-openagent.pre-${name}.json`));
  const prof = JSON.parse(readFileSync(profPath, "utf8").replace(/^﻿/, ""));
  const cur = readJsonc(OMA_JSON)?.data ?? {};
  cur.agents = prof.agents;       // swap whole blocks
  cur.categories = prof.categories;
  writeFileSync(OMA_JSON, JSON.stringify(cur, null, 2) + "\n", { encoding: "utf8" }); // no BOM
  console.log(c("green", `✓ switched to profile "${name}" — ${Object.keys(prof.agents).length} agents, ${Object.keys(prof.categories).length} categories. Restart the OpenCode TUI to load it.`));
  process.exit(0);
}

// --- backup action (the only write path) ---
if (process.argv[2] === "backup") {
  const d = new Date().toISOString().slice(0, 10);
  const dest = join(CFG, "agent-config-backups", d);
  mkdirSync(dest, { recursive: true });
  let n = 0;
  for (const f of ["oh-my-openagent.json", "oh-my-openagent.jsonc", "opencode.json"]) {
    const src = join(CFG, f);
    if (existsSync(src)) { copyFileSync(src, join(dest, f.replace(/\.json[c]?$/, ".snapshot$&"))); n++; }
  }
  console.log(c("green", `✓ backed up ${n} file(s) → ${dest}`));
  process.exit(0);
}

// --- report ---
console.log(c("bold", "\nOpenCode / oh-my-openagent — install health & inventory"));
console.log(c("dim", "─".repeat(58)));
console.log(`config dir: ${c("cyan", CFG)}`);

// CLI version vs latest
const cliVer = tryExec("opencode", ["--version"]) ?? c("red", "opencode not on PATH");
const cliLatest = tryExec("npm", ["view", "opencode-ai", "version"]);
console.log(`\n${c("bold", "OpenCode CLI")} (pkg opencode-ai)`);
console.log(`  installed: ${c("cyan", cliVer)}${cliLatest ? `   latest: ${c("cyan", cliLatest)}${cliVer !== cliLatest ? c("yellow", "  (update available → opencode upgrade)") : c("green", "  ✓ current")}` : ""}`);

// pinned plugin versions from config-dir package.json
const pkg = readJsonc(join(CFG, "package.json"));
const pinnedOma = pkg?.data?.dependencies?.["oh-my-openagent"];
const pinnedPlug = pkg?.data?.dependencies?.["@opencode-ai/plugin"];
const omaLatest = tryExec("npm", ["view", "oh-my-openagent", "version"]);
const plugLatest = tryExec("npm", ["view", "@opencode-ai/plugin", "version"]);
// CRITICAL: the TUI loads the plugin from ~/.cache/opencode/packages, NOT from CFG/node_modules.
// CFG/node_modules is a DECOY — editing/version-checking it is a no-op for what actually runs.
const CACHE = join(homedir(), ".cache", "opencode", "packages");
const cacheOma = readJsonc(join(CACHE, "oh-my-openagent@latest", "node_modules", "oh-my-openagent", "package.json"))?.data?.version
  ?? readJsonc(join(CACHE, "node_modules", "oh-my-openagent", "package.json"))?.data?.version;
const cacheAlias = readJsonc(join(CACHE, "node_modules", "oh-my-opencode", "package.json"))?.data?.version; // legacy alias, same code
const decoyOma = readJsonc(join(CFG, "node_modules", "oh-my-openagent", "package.json"))?.data?.version;
console.log(`\n${c("bold", "Plugin layer")}`);
console.log(`  ${c("bold", "LOADED by TUI")} (~/.cache/opencode/packages): oh-my-openagent ${c("cyan", cacheOma ?? "?")}${cacheAlias ? c("dim", `  [oh-my-opencode alias: ${cacheAlias}]`) : ""}  latest ${c("cyan", omaLatest ?? "?")}${cacheOma && omaLatest && cacheOma !== omaLatest ? c("yellow", "  (update available)") : c("green", "  ✓")}`);
console.log(`  ${c("dim", "decoy (CFG/node_modules, NOT loaded):")} oh-my-openagent ${c("dim", decoyOma ?? "?")}  pinned ${c("dim", pinnedOma ?? "?")}`);
console.log(`  @opencode-ai/plugin: pinned ${c("cyan", pinnedPlug ?? "?")}  latest ${c("cyan", plugLatest ?? "?")}`);

// opencode.json sanity
const oc = readJsonc(join(CFG, "opencode.json"));
const plugins = oc?.data?.plugin;
console.log(`\n${c("bold", "opencode.json")}  ${oc?.ok ? c("green", "✓ parses") : c("red", "✗ INVALID: " + oc?.error)}`);
console.log(`  plugin array: ${c("cyan", JSON.stringify(plugins ?? "(none)"))}${Array.isArray(plugins) && plugins.includes("oh-my-openagent") ? c("green", "  ✓ oh-my-openagent registered") : c("yellow", "  ⚠ oh-my-openagent NOT registered")}`);

// oh-my-openagent.json inventory
const oma = readJsonc(OMA_JSON);
console.log(`\n${c("bold", "oh-my-openagent config")} (${OMA_JSON.split(/[\\/]/).pop()})  ${oma ? (oma.ok ? c("green", "✓ parses") : c("red", "✗ INVALID: " + oma.error)) : c("yellow", "missing")}`);
if (oma?.ok) {
  const agents = oma.data.agents ?? {};
  const cats = oma.data.categories ?? {};
  console.log(c("dim", "\n  Agents:"));
  for (const [name, e] of Object.entries(agents)) {
    const tail = fb(e);
    console.log(`    ${name.padEnd(18)} ${c("cyan", pickModel(e))}${tail ? c("dim", "   ↳ " + tail) : ""}`);
  }
  console.log(c("dim", "\n  Categories:"));
  for (const [name, e] of Object.entries(cats)) {
    const tail = fb(e);
    console.log(`    ${name.padEnd(18)} ${c("cyan", pickModel(e))}${tail ? c("dim", "   ↳ " + tail) : ""}`);
  }
}

// backups present — date-folders (from `backup`) vs flat timestamped files (from switch.mjs)
const bkDir = join(CFG, "agent-config-backups");
if (existsSync(bkDir)) {
  const ents = readdirSync(bkDir, { withFileTypes: true });
  const dirs = ents.filter((e) => e.isDirectory()).map((e) => e.name).sort();
  const flat = ents.filter((e) => e.isFile()).length;
  console.log(c("dim", `\n  Backups: ${dirs.length ? dirs.join(", ") : "(no date folders)"}${flat ? ` + ${flat} flat snapshot(s) from switch.mjs` : ""}`));
}
console.log(c("dim", "\nRun `node driver.mjs backup` before any edit. This script never installs/updates/edits.\n"));
