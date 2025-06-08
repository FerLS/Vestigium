using System.Threading.Tasks;
using UnityEngine;

[RequireComponent(typeof(Collider))]
public abstract class Interactable : MonoBehaviour
{
    InputSystem_Actions inputActions;
    CapsuleCollider _collider;

    [Header("Interactable Settings")]
    private bool _isPlayerInRange;
    [SerializeField] private bool oneTimeInteraction = false; // If true, interaction can only happen once

    public enum InteractionType
    {
        Read,
        PushPull,
        PickUp,
        Closable,
        Switchable,
    }

    protected InteractionType interactionType = InteractionType.Read;
    [SerializeField] private string interactionMessage = ""; // Custom message to display during interaction

    void Awake()
    {
        inputActions = new InputSystem_Actions();
        inputActions.Enable();
    }

    protected virtual void Start()
    {
        // Subscribe to input events
        inputActions.Player.Interact.started += _ => StartInteraction();
        inputActions.Player.Interact.canceled += _ => StopInteraction();

        _collider = GetComponent<CapsuleCollider>();
        if (_collider != null)
        {
            _collider.isTrigger = true;
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player") && enabled)
        {
            _isPlayerInRange = true;
            // Display appropriate interaction message based on interaction type
            switch (interactionType)
            {
                case InteractionType.Read:
                    PlayerController.Instance.ShowInteractionText(string.IsNullOrEmpty(interactionMessage) ? "Click to read" : interactionMessage);
                    break;
                case InteractionType.PushPull:
                    PlayerController.Instance.ShowInteractionText(string.IsNullOrEmpty(interactionMessage) ? "Click to push/pull" : interactionMessage);
                    break;
                case InteractionType.PickUp:
                    PlayerController.Instance.ShowInteractionText(string.IsNullOrEmpty(interactionMessage) ? "Hold Click to pick up" : interactionMessage);
                    break;
                case InteractionType.Closable:
                    PlayerController.Instance.ShowInteractionText(string.IsNullOrEmpty(interactionMessage) ? "Click to close" : interactionMessage);
                    break;
                case InteractionType.Switchable:
                    PlayerController.Instance.ShowInteractionText(string.IsNullOrEmpty(interactionMessage) ? "Click to switch" : interactionMessage);
                    break;
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            _isPlayerInRange = false;
            PlayerController.Instance.ShowInteractionText("");
        }
    }

    protected async virtual void StartInteraction()
    {
        if (_isPlayerInRange)
        {
            // Notify player controller and call the abstract implementation
            await PlayerController.Instance.OnStartInteraction(interactionType, transform);
            OnStartInteraction();
        }
    }

    protected virtual void StopInteraction()
    {
        if (_isPlayerInRange)
        {
            PlayerController.Instance.OnStopInteraction(interactionType);
            OnStopInteraction();
            // Disable the component if this is a one-time interaction
            enabled = !oneTimeInteraction;
        }
    }

    // Abstract methods to be implemented by derived classes
    public abstract void OnStartInteraction();
    public abstract void OnStopInteraction();
}
