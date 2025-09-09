namespace Brain.Core;

public static class Entropy
{
    public static double Delta(double[] series)
    {
        if (series == null)
            return 0.0;

        double lo = double.MaxValue, hi = double.MinValue;
        var count = 0;
        foreach (var v in series)
        {
            if (double.IsNaN(v))
                continue;
            count++;
            if (v < lo) lo = v;
            if (v > hi) hi = v;
        }
        if (count < 2 || hi == lo)
            return 0.0;
        var maxAbs = Math.Max(Math.Abs(hi), 1e-9);
        return (hi - lo) / maxAbs;
    }
}
