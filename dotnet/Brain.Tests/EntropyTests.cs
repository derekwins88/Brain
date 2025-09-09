using Brain.Core;
using Xunit;

namespace Brain.Tests;

public class EntropyTests
{
    [Fact]
    public void Delta_Constant_ReturnsZero()
    {
        Assert.Equal(0.0, Entropy.Delta(new double[] { 1, 1, 1 }));
    }

    [Fact]
    public void Delta_Varied_InRange()
    {
        var d = Entropy.Delta(new double[] { 1, 2, 3 });
        Assert.True(d > 0.0 && d <= 1.0);
    }

    [Fact]
    public void Delta_IgnoresNaNs()
    {
        Assert.Equal(0.0, Entropy.Delta(new double[] { double.NaN, 5.0 }));
        var d = Entropy.Delta(new double[] { 1.0, double.NaN, 5.0 });
        Assert.InRange(d, 0.79, 0.81);
    }
}
