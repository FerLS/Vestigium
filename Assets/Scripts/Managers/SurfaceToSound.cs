using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public class SurfaceAudioClips
{
    public string surfaceName;
    public List<AudioClip> clips;
}

public class SurfaceToSound : MonoBehaviour
{
    public static SurfaceToSound Instance { get; private set; }

    [Header("Surface and sound list")]
    [SerializeField] private List<SurfaceAudioClips> surfaceClipList;

    private Dictionary<string, List<AudioClip>> surfaceClipDict;

    void Awake()
    {
        // Singleton pattern
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject); // Optional: make it persistent between scenes
            InitializeDictionary();
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void InitializeDictionary()
    {
        // Case-insensitive dictionary for surface names
        surfaceClipDict = new Dictionary<string, List<AudioClip>>(StringComparer.OrdinalIgnoreCase);

        foreach (var entry in surfaceClipList)
        {
            if (!string.IsNullOrEmpty(entry.surfaceName) && entry.clips != null && entry.clips.Count > 0)
            {
                surfaceClipDict[entry.surfaceName] = entry.clips;
            }
        }
    }

    public AudioClip GetSurfaceSound(string surfaceName)
    {
        // Return a random clip for the given surface
        if (surfaceClipDict.TryGetValue(surfaceName, out var clips) && clips.Count > 0)
        {
            int index = UnityEngine.Random.Range(0, clips.Count);
            return clips[index];
        }

        Debug.LogWarning($"No clips found for surface: {surfaceName}");
        return null;
    }
}
