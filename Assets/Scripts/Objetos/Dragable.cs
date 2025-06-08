using UnityEngine;

public class Dragable : Interactable
{
    Rigidbody rb;

    protected override void Start()
    {
        rb = GetComponent<Rigidbody>();
        interactionType = InteractionType.PushPull;
        base.Start();
    }

    public override void OnStartInteraction()
    {
        Debug.Log("Dragable interaction started.");

        // Disable physics when object is grabbed
        rb.isKinematic = true;
    }

    public override void OnStopInteraction()
    {
        // Enable physics when object is released
        rb.isKinematic = false;

        // Unlink object from player
        transform.SetParent(null);
    }
}
