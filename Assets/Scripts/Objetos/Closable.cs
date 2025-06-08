using UnityEngine;

public class Closable : Interactable
{
    private Animator anim;

    [Header("Audio")]
    [SerializeField] private AudioClip constant_sound_clip; // Background sound for the closable object
    [SerializeField] private AudioClip close_sound_clip;    // Sound played when closing the object

    protected override void Start()
    {
        // Start looping background sound
        AudioManager.Instance.PlayLoopSFX3D("refrigerator", constant_sound_clip, transform);
        anim = GetComponent<Animator>();
        anim.ResetTrigger("OpenDoor");

        interactionType = InteractionType.Closable;
        base.Start();
    }

    public override void OnStartInteraction()
    {
        // Turn off the light and play animation/sound when interacted with
        GameObject lightObject = GameObject.Find("FridgeLight1");
        lightObject.SetActive(false);
        anim.SetTrigger("OpenDoor");
        AudioManager.Instance.PlaySFX3D(close_sound_clip, transform);
    }

    public override void OnStopInteraction()
    {
        // Optional logic when interaction ends.
    }
}
