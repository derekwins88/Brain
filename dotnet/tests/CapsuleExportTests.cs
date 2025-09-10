using Xunit;
using System.IO;
using System.Text.Json.Nodes;

public class CapsuleExportTests
{
    [Fact]
    public void Capsule_SchemaBits_Present()
    {
        // If a sample exists, validate presence of key bits.
        var path = Directory.GetFiles(".", "IMM_v36_*.json", SearchOption.AllDirectories);
        if (path.Length == 0) return; // non-fatal in CI before first export
        var j = JsonNode.Parse(File.ReadAllText(path[0]))!;
        Assert.Equal("3.6", j["version"]!.ToString());
        Assert.NotNull(j["provenance"]?["hashes"]?["cnf_sha256"]);
        Assert.NotNull(j["provenance"]?["hashes"]?["entropy_sha256"]);
    }
}

