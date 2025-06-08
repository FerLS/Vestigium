using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.UI;

/// <summary>
/// Manages all audio playback and volume settings in the game
/// </summary>
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance;

    [Header("Audio Mixer & Groups")]
    [SerializeField] private AudioMixer mixer;
    [SerializeField] private AudioMixerGroup musicGroup;
    [SerializeField] private AudioMixerGroup sfxGroup;

    [Header("Fixed Audio Sources")]
    [SerializeField] private AudioSource sfxSource;
    [SerializeField] private AudioSource bgmSource;

    [Header("Volume Sliders")]
    [SerializeField] private Slider musicSlider;
    [SerializeField] private Slider sfxSlider;

    // Dictionary to track and manage looping 3D sounds
    private Dictionary<string, AudioSource> looped3DSounds = new();

    void Awake()
    {
        Instance = this;

        // Set mixer groups for audio sources
        if (sfxSource != null) sfxSource.outputAudioMixerGroup = sfxGroup;
        if (bgmSource != null) bgmSource.outputAudioMixerGroup = musicGroup;
    }

    public void Start()
    {
        // Load saved volume settings or set defaults
        if (PlayerPrefs.HasKey("MusicVolume"))
        {
            LoadVolume();
        }
        else
        {
            musicSlider.value = 1f;
            sfxSlider.value = 1f;
            SetMusicVolume();
            SetEffectVolume();
        }
    }

    // =========================================================================
    // MUSIC
    // =========================================================================

    /// <summary>
    /// Plays a music track through the background music source
    /// </summary>
    public void PlayMusic(AudioClip clip, bool loop = true)
    {
        if (clip == null || bgmSource == null) return;

        bgmSource.clip = clip;
        bgmSource.loop = loop;
        bgmSource.Play();
    }

    /// <summary>
    /// Stops the currently playing music
    /// </summary>
    public void StopMusic()
    {
        if (bgmSource != null) bgmSource.Stop();
    }

    // =========================================================================
    // SFX - 2D
    // =========================================================================

    /// <summary>
    /// Plays a non-positional sound effect
    /// </summary>
    public void PlaySFX(AudioClip clip, float volume = 1f)
    {
        if (clip == null || sfxSource == null) return;
        sfxSource.PlayOneShot(clip, volume);
    }

    // =========================================================================
    // SFX - 3D POSITIONAL
    // =========================================================================

    /// <summary>
    /// Plays a positional one-shot sound effect in 3D space
    /// </summary>
    public void PlaySFX3D(AudioClip clip, Transform transform)
    {
        if (clip == null) return;

        GameObject tempGO = new GameObject("SFX3D_" + clip.name);
        tempGO.transform.parent = transform;

        AudioSource source = tempGO.AddComponent<AudioSource>();
        source.clip = clip;
        source.spatialBlend = 1f;
        source.minDistance = 1f;
        source.maxDistance = 15f;
        source.rolloffMode = AudioRolloffMode.Logarithmic;
        source.outputAudioMixerGroup = sfxGroup;
        source.playOnAwake = false;

        source.Play();
        Destroy(tempGO, clip.length);
    }

    // =========================================================================
    // LOOP 3D
    // =========================================================================

    /// <summary>
    /// Plays a looping 3D sound attached to a specific transform
    /// </summary>
    public void PlayLoopSFX3D(string name, AudioClip clip, Transform anchor)
    {
        if (clip == null || anchor == null) return;

        // Don't create duplicate looping sounds with the same name
        if (looped3DSounds.ContainsKey(name) && looped3DSounds[name] != null)
            return;

        GameObject loopGO = new GameObject("Loop3D_" + name);
        loopGO.transform.parent = anchor;
        loopGO.transform.localPosition = Vector3.zero;

        AudioSource source = loopGO.AddComponent<AudioSource>();
        source.clip = clip;
        source.loop = true;
        source.spatialBlend = 1f;
        source.minDistance = 1f;
        source.maxDistance = 15f;
        source.rolloffMode = AudioRolloffMode.Logarithmic;
        source.outputAudioMixerGroup = sfxGroup;
        source.playOnAwake = false;

        source.Play();
        looped3DSounds[name] = source;
    }

    /// <summary>
    /// Stops a looping sound by name and cleans up its resources
    /// </summary>
    public void StopLoopSound(string name)
    {
        if (looped3DSounds.TryGetValue(name, out var source) && source != null)
        {
            source.Stop();
            Destroy(source.gameObject);
            looped3DSounds.Remove(name);
        }
    }

    // =========================================================================
    // VOLUME
    // =========================================================================

    /// <summary>
    /// Loads volume settings from PlayerPrefs
    /// </summary>
    private void LoadVolume()
    {
        musicSlider.value = PlayerPrefs.GetFloat("MusicVolume");
        sfxSlider.value = PlayerPrefs.GetFloat("SFXVolume");

        SetMusicVolume();
        SetEffectVolume();
    }

    /// <summary>
    /// Updates the SFX volume based on slider value
    /// </summary>
    public void SetEffectVolume()
    {
        float volume = Mathf.Max(sfxSlider.value, 0.0001f);
        mixer.SetFloat("SFXVolume", Mathf.Log10(volume) * 20f);
        PlayerPrefs.SetFloat("SFXVolume", volume);
    }

    /// <summary>
    /// Updates the music volume based on slider value
    /// </summary>
    public void SetMusicVolume()
    {
        float volume = Mathf.Max(musicSlider.value, 0.0001f);
        mixer.SetFloat("MusicVolume", Mathf.Log10(volume) * 20f);
        PlayerPrefs.SetFloat("MusicVolume", volume);
    }
}
