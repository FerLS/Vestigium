using UnityEngine;

public class InteractionTrigger : MonoBehaviour
{
    private Closable interactable;
    private bool hasBeenTriggered = false;

    private void Awake()
    {
        // Get the Closable component from the parent object
        interactable = GetComponentInParent<Closable>();
    }

    public void Trigger()
    {
        // Return if already triggered or if interactable is null
        if (hasBeenTriggered || interactable == null) return;

        // Start the interaction and mark as triggered
        interactable.OnStartInteraction();
        hasBeenTriggered = true;
    }
}
