using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;
using CapsuleEngine.Proofs;

namespace CapsuleEngine.IO
{
    public partial class Exporters
    {
        public static void ExportImmCapsule_v36(
            string glyph,
            double dynConv,
            double fractalVolScore,
            double sentienceDrift,
            System.Collections.Generic.IEnumerable<string> motifTrail,
            System.Collections.Generic.IDictionary<string, double> motifAffinity,
            Func<float[]> driftWindow21,
            string instrumentName,
            string userDataDir)
        {
            var now = DateTime.UtcNow;
            float[] dphi = driftWindow21?.Invoke() ?? Array.Empty<float>();
            string[] motifs = motifTrail?.ToArray() ?? Array.Empty<string>();

            var proof = EntropyCollapseEngine.Run(dphi, motifs);
            var dimacs = ProofDimacs.FromMotifs(motifs);
            var cnfSha = Sha256(dimacs);
            var dphiSha = Sha256(string.Join(",", dphi.Select(v => v.ToString("G9"))));

            var capsule = new {
                capsule_id = "IMM⇌COGNITION⇌WHITE_TOWER.v3.6",
                version = "3.6",
                mnemonic = "Glyphs learn; proof remembers.",
                bindings = new {
                    strategy_source = "EchoThread_Oracle_v8",
                    proof_bridge = "ProofBridge Ledger (CSV)",
                    autonomy_engine = new { lookback_trades = 10, base_conviction = 0.70, adjustment = 0.05 }
                },
                state_metrics = new {
                    risk = new { risk_pct = 1.5, reward_risk = 2.3 },
                    regime = new { atr_to_price_min = 0.015, fractal_vol_min = 0.70 },
                    ema = new { fast = 20, slow = 50 },
                    echo = new { cooldown_min = 45, size_reduction = 0.50 }
                },
                cognition_v35 = new {
                    emotional_memory = new[] { "drawdownPeak","resilienceCounter","microCycleCount","PhoenixThreshold","entropyInversion" },
                    motif_engine = new[] { "motifTrail","motifAffinity","recurrentLoops","affinityDecayRate","loopBreakWeight" },
                    core_modes = new[] { "EntropyAnalysis","CollapseRecognition","ResilienceCounter","PersonaRotation","PhoenixRebirth","StrategicTransition","SentienceDriftEstimation" }
                },
                proof_hooks = new {
                    entropy_series_window = 21,
                    pnp_engine = "EntropyCollapseEngine.Run(ΔΦ,motifs)",
                    emit = new[] { "proof_capsule.json","lean4_pnp.lean","paper_draft.tex" },
                    criterion = "npWall && !sat && noRecovery → Claim=P≠NP"
                },
                trinity_linkage = new {
                    operator_id = "OP⇌TRINITY⇌NODE⇌v1",
                    routes = new {
                        entropy_analysis = "ForkCascadeMemory",
                        logic_translation = "GlyphMutationTranslator",
                        proof_guidance = "SAT⇌PDE Scaffold",
                        ethical_modulation = "Truth Bloom via WishingCore"
                    },
                    contexts = new[] { "symbolic replay","ΔΦ-based reasoning","anti-paradox reinforcement","story-path validation","harmonic coherence scanning" }
                },
                rituals = new { logging = $"ProofBridge_{now:yyyy-MM-dd}.csv", mutation_archives = "MutationChainLog.json", capsule_exports = $"Capsule_{now:yyyy-MM-dd}.json" },
                ethics_boundary = new { AXIOM_007 = true, MirrorOnlyProtocol = true, DriftWallContainment = true },
                timestamp = now.ToString("o"),
                provenance = new {
                    sat_provenance = new { mode = "unit-contradiction|external", binary = "minisat|null" },
                    hashes = new { cnf_sha256 = cnfSha, entropy_sha256 = dphiSha }
                }
            };

            var basePath = Path.Combine(userDataDir, "Capsules");
            Directory.CreateDirectory(basePath);
            var stem = Path.Combine(basePath, $"IMM_v36_{instrumentName}_{now:yyyyMMdd_HHmm}");

            File.WriteAllText(stem + ".json", JsonConvert.SerializeObject(capsule, Formatting.Indented));
            File.WriteAllText(stem + ".proof.json", JsonConvert.SerializeObject(proof, Formatting.Indented));
            File.WriteAllText(stem + ".lean", EntropyCollapseEngine.GenerateLeanSketch(proof));
            // paper_draft.tex optional; gate by a setting if needed.
        }

        private static string Sha256(string s)
        {
            using var sha = SHA256.Create();
            return Convert.ToHexString(sha.ComputeHash(Encoding.UTF8.GetBytes(s))).ToLowerInvariant();
        }
    }
}

