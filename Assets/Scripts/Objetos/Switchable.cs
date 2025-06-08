using UnityEngine;

public class Switchable : Interactable
{
    private Light[] lightsToToggle;
    private bool isOn = true;

    [Header("Audio")]
    [SerializeField] private AudioClip clip;

    protected override void Start()
    {
        // Search recursively for lights in this object and its children
        lightsToToggle = GetComponentsInChildren<Light>(includeInactive: true);
        interactionType = InteractionType.Switchable;

        base.Start();
    }

    public override void OnStartInteraction()
    {
        // Only allow interaction if player is on the ground
        if (!PlayerController.Instance.IsGrounded()) return;

        if (lightsToToggle != null)
        {
            // Toggle the lights state
            isOn = !isOn;
            AudioManager.Instance.PlaySFX3D(clip, transform);

            // Update all lights
            foreach (Light light in lightsToToggle)
            {
                light.enabled = isOn;
            }
        }
    }

    public override void OnStopInteraction()
    {
        // Optional logic when interaction ends.
    }
}
