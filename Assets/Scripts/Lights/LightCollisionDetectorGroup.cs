using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Static class that manages a group of light collision detectors.
/// </summary>
public static class LightCollisionDetectorGroup
{
    // List containing all registered light collision detectors
    private static readonly List<LightCollisionDetection> detectors = new();

    /// <summary>
    /// Registers a detector if not already registered.
    /// </summary>
    public static void Register(LightCollisionDetection detector)
    {
        if (!detectors.Contains(detector))
            detectors.Add(detector);
    }

    /// <summary>
    /// Removes a detector from the registry.
    /// </summary>
    public static void Unregister(LightCollisionDetection detector)
    {
        detectors.Remove(detector);
    }

    /// <summary>
    /// Checks if the target collides with any registered light detector.
    /// </summary>
    /// <returns>True if target is in any light cone, false otherwise.</returns>
    public static bool CollidesWithAny(Transform target)
    {
        foreach (var detector in detectors)
        {
            if (detector != null && detector.IsInLightCone(target))
                return true;
        }
        return false;
    }
}
