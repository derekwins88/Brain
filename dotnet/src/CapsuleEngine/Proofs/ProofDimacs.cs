using System.Linq;

namespace CapsuleEngine.Proofs
{
    public static class ProofDimacs
    {
        // Minimal CNF generator matching your motif chain pattern (no contradiction by default).
        public static string FromMotifs(string[] motifs)
        {
            var n = (motifs?.Length ?? 0);
            if (n <= 1) return "p cnf 1 1\n1 0\n";
            var header = $"p cnf {n} {n}\n";
            var body = string.Join("", Enumerable.Range(1, n).Select(i =>
            {
                var a = i;
                var b = (i % n) + 1;
                return $"{a} -{b} 0\n";
            }));
            return header + body;
        }
    }
}

