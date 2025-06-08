using UnityEngine;

public class Sardine : MonoBehaviour
{
    public CatWalk cat;

    [Header("Audio")]
    [SerializeField] private AudioClip clip;

    private void Start()
    {
        // Creates a 3D looping sound effect for the fish
        AudioManager.Instance.PlayLoopSFX3D("fish", clip, transform);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("DogBowl"))
        {
            // Activates the cat when sardine enters dog bowl
            cat.Activate(); // Changed from Activar to Activate
        }
    }
}
